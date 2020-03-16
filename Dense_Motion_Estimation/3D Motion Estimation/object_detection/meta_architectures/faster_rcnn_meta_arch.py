from abc import abstractmethod
from functools import partial
import tensorflow as tf

from object_detection.anchor_generators import multiple_grid_anchor_generator
from object_detection.core import balanced_positive_negative_sampler as sampler
from object_detection.core import box_list
from object_detection.core import box_list_ops
from object_detection.core import box_predictor
from object_detection.core import losses
from object_detection.core import model
from object_detection.core import post_processing
from object_detection.core import standard_fields as fields
from object_detection.core import target_assigner
from object_detection.utils import ops
from object_detection.utils import shape_utils
from object_detection.utils import motion_util

slim = tf.contrib.slim


class FasterRCNNFeatureExtractor(object):
    """Faster R-CNN Feature Extractor definition."""

    def __init__(self,
                 is_training,
                 first_stage_features_stride,
                 reuse_weights=None,
                 weight_decay=0.0):
        """Constructor.
        Args:
          is_training: A boolean indicating whether the training version of the
            computation graph should be constructed.
          first_stage_features_stride: Output stride of extracted RPN feature map.
          reuse_weights: Whether to reuse variables. Default is None.
          weight_decay: float weight decay for feature extractor (default: 0.0).
        """
        self._is_training = is_training
        self._first_stage_features_stride = first_stage_features_stride
        self._reuse_weights = reuse_weights
        self._weight_decay = weight_decay

    @abstractmethod
    def preprocess(self, resized_inputs):
        """Feature-extractor specific preprocessing (minus image resizing)."""
        pass

    def extract_proposal_features(self, preprocessed_inputs, scope):
        """Extracts first stage RPN features.
        This function is responsible for extracting feature maps from preprocessed
        images.  These features are used by the region proposal network (RPN) to
        predict proposals.
        Args:
          preprocessed_inputs: A [batch, height, width, channels] float tensor
            representing a batch of images.
          scope: A scope name.
        Returns:
          rpn_feature_map: A tensor with shape [batch, height, width, depth]
        """
        with tf.variable_scope(scope, values=[preprocessed_inputs]):
            return self._extract_proposal_features(preprocessed_inputs, scope)

    @abstractmethod
    def _extract_proposal_features(self, preprocessed_inputs, scope):
        """Extracts first stage RPN features, to be overridden."""
        pass

    def extract_box_classifier_features(self, proposal_feature_maps, scope,
                                        reuse=None):
        """Extracts second stage box classifier features.
        Args:
          proposal_feature_maps: A 4-D float tensor with shape
            [batch_size * self.max_num_proposals, crop_height, crop_width, depth]
            representing the feature map cropped to each proposal.
          scope: A scope name.
        Returns:
          proposal_classifier_features: A 4-D float tensor with shape
            [batch_size * self.max_num_proposals, height, width, depth]
            representing box classifier features for each proposal.
        """
        with tf.variable_scope(scope, values=[proposal_feature_maps],
                               reuse=reuse):
            return self._extract_box_classifier_features(proposal_feature_maps, scope)

    @abstractmethod
    def _extract_box_classifier_features(self, proposal_feature_maps, scope):
        """Extracts second stage box classifier features, to be overridden."""
        pass

    def restore_from_classification_checkpoint_fn(
            self,
            first_stage_feature_extractor_scope,
            second_stage_feature_extractor_scope):
        """Returns a map of variables to load from a foreign checkpoint.
        Args:
          first_stage_feature_extractor_scope: A scope name for the first stage
            feature extractor.
          second_stage_feature_extractor_scope: A scope name for the second stage
            feature extractor.
        Returns:
          A dict mapping variable names (to load from a checkpoint) to variables in
          the model graph.
        """
        variables_to_restore = {}
        for variable in tf.global_variables():
            for scope_name in [first_stage_feature_extractor_scope,
                               second_stage_feature_extractor_scope]:
                if variable.op.name.startswith(scope_name):
                    var_name = variable.op.name.replace(scope_name + '/', '')
                    if not 'conv1_adapted' in var_name and not 'pyramid' in var_name:
                        variables_to_restore[var_name] = variable
        return variables_to_restore


class FasterRCNNMetaArch(model.DetectionModel):
    """Faster R-CNN Meta-architecture definition."""

    def __init__(self,
                 is_training,
                 num_classes,
                 image_resizer_fn,
                 feature_extractor,
                 first_stage_only,
                 first_stage_anchor_generator,
                 first_stage_atrous_rate,
                 first_stage_box_predictor_arg_scope,
                 first_stage_box_predictor_kernel_size,
                 first_stage_box_predictor_depth,
                 first_stage_minibatch_size,
                 first_stage_positive_balance_fraction,
                 first_stage_nms_score_threshold,
                 first_stage_nms_iou_threshold,
                 first_stage_max_proposals,
                 first_stage_localization_loss_weight,
                 first_stage_objectness_loss_weight,
                 initial_crop_size,
                 maxpool_kernel_size,
                 maxpool_stride,
                 second_stage_mask_rcnn_box_predictor,
                 second_stage_batch_size,
                 second_stage_balance_fraction,
                 second_stage_non_max_suppression_fn,
                 second_stage_score_conversion_fn,
                 second_stage_localization_loss_weight,
                 second_stage_classification_loss_weight,
                 second_stage_mask_loss_weight,
                 second_stage_motion_loss_weight,
                 hard_example_miner,
                 first_stage_predict_camera_motion,
                 first_stage_camera_motion_loss_weight,
                 first_stage_camera_motion_arg_scope,
                 second_stage_motion_loss_from_flow,
                 first_stage_camera_motion_loss_from_flow,
                 parallel_iterations=16):
        """FasterRCNNMetaArch Constructor.
        Args:
          is_training: A boolean indicating whether the training version of the
            computation graph should be constructed.
          num_classes: Number of classes.  Note that num_classes *does not*
            include the background category, so if groundtruth labels take values
            in {0, 1, .., K-1}, num_classes=K (and not K+1, even though the
            assigned classification targets can range from {0,... K}).
          image_resizer_fn: A callable for image resizing.  This callable always
            takes a rank-3 image tensor (corresponding to a single image) and
            returns a rank-3 image tensor, possibly with new spatial dimensions.
            See builders/image_resizer_builder.py.
          feature_extractor: A FasterRCNNFeatureExtractor object.
          first_stage_only:  Whether to construct only the Region Proposal Network
            (RPN) part of the model.
          first_stage_anchor_generator: An anchor_generator.AnchorGenerator object.
          first_stage_atrous_rate: A single integer indicating the atrous rate for
            the single convolution op which is applied to the `rpn_features_to_crop`
            tensor to obtain a tensor to be used for box prediction. Some feature
            extractors optionally allow for producing feature maps computed at
            denser resolutions.  The atrous rate is used to compensate for the
            denser feature maps by using an effectively larger receptive field.
            (This should typically be set to 1).
          first_stage_box_predictor_arg_scope: Slim arg_scope for conv2d,
            separable_conv2d and fully_connected ops for the RPN box predictor.
          first_stage_box_predictor_kernel_size: Kernel size to use for the
            convolution op just prior to RPN box predictions.
          first_stage_box_predictor_depth: Output depth for the convolution op
            just prior to RPN box predictions.
          first_stage_minibatch_size: The "batch size" to use for computing the
            objectness and location loss of the region proposal network. This
            "batch size" refers to the number of anchors selected as contributing
            to the loss function for any given image within the image batch and is
            only called "batch_size" due to terminology from the Faster R-CNN paper.
          first_stage_positive_balance_fraction: Fraction of positive examples
            per image for the RPN. The recommended value for Faster RCNN is 0.5.
          first_stage_nms_score_threshold: Score threshold for non max suppression
            for the Region Proposal Network (RPN).  This value is expected to be in
            [0, 1] as it is applied directly after a softmax transformation.  The
            recommended value for Faster R-CNN is 0.
          first_stage_nms_iou_threshold: The Intersection Over Union (IOU) threshold
            for performing Non-Max Suppression (NMS) on the boxes predicted by the
            Region Proposal Network (RPN).
          first_stage_max_proposals: Maximum number of boxes to retain after
            performing Non-Max Suppression (NMS) on the boxes predicted by the
            Region Proposal Network (RPN).
          first_stage_localization_loss_weight: A float
          first_stage_objectness_loss_weight: A float
          initial_crop_size: A single integer indicating the output size
            (width and height are set to be the same) of the initial bilinear
            interpolation based cropping during ROI pooling.
          maxpool_kernel_size: A single integer indicating the kernel size of the
            max pool op on the cropped feature map during ROI pooling.
          maxpool_stride: A single integer indicating the stride of the max pool
            op on the cropped feature map during ROI pooling.
          second_stage_mask_rcnn_box_predictor: Mask R-CNN box predictor to use for
            the second stage.
          second_stage_batch_size: The batch size used for computing the
            classification and refined location loss of the box classifier.  This
            "batch size" refers to the number of proposals selected as contributing
            to the loss function for any given image within the image batch and is
            only called "batch_size" due to terminology from the Faster R-CNN paper.
          second_stage_balance_fraction: Fraction of positive examples to use
            per image for the box classifier. The recommended value for Faster RCNN
            is 0.25.
          second_stage_non_max_suppression_fn: batch_multiclass_non_max_suppression
            callable that takes `boxes`, `scores`, optional `clip_window` and
            optional (kwarg) `mask` inputs (with all other inputs already set)
            and returns a dictionary containing tensors with keys:
            `detection_boxes`, `detection_scores`, `detection_classes`,
            `num_detections`, and (optionally) `detection_masks`. See
            `post_processing.batch_multiclass_non_max_suppression` for the type and
            shape of these tensors.
          second_stage_score_conversion_fn: Callable elementwise nonlinearity
            (that takes tensors as inputs and returns tensors).  This is usually
            used to convert logits to probabilities.
          second_stage_localization_loss_weight: A float
          second_stage_classification_loss_weight: A float
          second_stage_mask_loss_weight: A float
          second_stage_motion_loss_weight: A float
          hard_example_miner:  A losses.HardExampleMiner object (can be None).
          first_stage_predict_camera_motion: Whether to predict a global camera motion
          first_stage_camera_motion_loss_weight: A float
          first_stage_camera_motion_arg_scope: Slim arg_scope for camera motion fc layers.
          second_stage_motion_loss_from_flow: True if optical flow based 2D motion loss
            should be used for supervision of instance motions (if predicted).
          first_stage_camera_motion_loss_from_flow: True if optical flow based 2D motion
            loss should be used for supervision of camera motions (if predicted).
          parallel_iterations: (Optional) The number of iterations allowed to run
            in parallel for calls to tf.map_fn.
        Raises:
          ValueError: If `second_stage_batch_size` > `first_stage_max_proposals`
        """
        super(FasterRCNNMetaArch, self).__init__(num_classes=num_classes)

        if second_stage_batch_size > first_stage_max_proposals:
            raise ValueError('second_stage_batch_size should be no greater than '
                             'first_stage_max_proposals.')

        self._is_training = is_training
        self._image_resizer_fn = image_resizer_fn
        self._feature_extractor = feature_extractor
        self._first_stage_only = first_stage_only

        # The first class is reserved as background.
        unmatched_cls_target = tf.constant(
            [1] + self._num_classes * [0], dtype=tf.float32)
        self._proposal_target_assigner = target_assigner.create_target_assigner(
            'FasterRCNN', 'proposal')
        self._detector_target_assigner = target_assigner.create_target_assigner(
            'FasterRCNN', 'detection', unmatched_cls_target=unmatched_cls_target)
        # Both proposal and detector target assigners use the same box coder
        self._box_coder = self._proposal_target_assigner.box_coder

        # (First stage) Region proposal network parameters
        self._first_stage_anchor_generator = first_stage_anchor_generator
        self._first_stage_atrous_rate = first_stage_atrous_rate
        self._first_stage_box_predictor_arg_scope = (
            first_stage_box_predictor_arg_scope)
        self._first_stage_box_predictor_kernel_size = (
            first_stage_box_predictor_kernel_size)
        self._first_stage_box_predictor_depth = first_stage_box_predictor_depth
        self._first_stage_minibatch_size = first_stage_minibatch_size
        self._first_stage_sampler = sampler.BalancedPositiveNegativeSampler(
            positive_fraction=first_stage_positive_balance_fraction)
        self._first_stage_box_predictor = box_predictor.ConvolutionalBoxPredictor(
            self._is_training, num_classes=1,
            conv_hyperparams=self._first_stage_box_predictor_arg_scope,
            min_depth=0, max_depth=0, num_layers_before_predictor=0,
            use_dropout=False, dropout_keep_prob=1.0, kernel_size=1,
            box_code_size=self._box_coder.code_size)

        self._first_stage_nms_score_threshold = first_stage_nms_score_threshold
        self._first_stage_nms_iou_threshold = first_stage_nms_iou_threshold
        self._first_stage_max_proposals = first_stage_max_proposals

        self._first_stage_localization_loss = (
            losses.WeightedSmoothL1LocalizationLoss(anchorwise_output=True))
        self._first_stage_objectness_loss = (
            losses.WeightedSoftmaxClassificationLoss(anchorwise_output=True))
        self._first_stage_loc_loss_weight = first_stage_localization_loss_weight
        self._first_stage_obj_loss_weight = first_stage_objectness_loss_weight

        # Per-region cropping parameters
        self._initial_crop_size = initial_crop_size
        self._maxpool_kernel_size = maxpool_kernel_size
        self._maxpool_stride = maxpool_stride

        self._mask_rcnn_box_predictor = second_stage_mask_rcnn_box_predictor

        self._second_stage_batch_size = second_stage_batch_size
        self._second_stage_sampler = sampler.BalancedPositiveNegativeSampler(
            positive_fraction=second_stage_balance_fraction)

        self._second_stage_nms_fn = second_stage_non_max_suppression_fn
        self._second_stage_score_conversion_fn = second_stage_score_conversion_fn

        self._second_stage_localization_loss = (
            losses.WeightedSmoothL1LocalizationLoss(anchorwise_output=True))
        self._second_stage_classification_loss = (
            losses.WeightedSoftmaxClassificationLoss(anchorwise_output=True))
        self._second_stage_mask_loss = (
            losses.WeightedSigmoidClassificationLoss(anchorwise_output=True))
        self._second_stage_loc_loss_weight = second_stage_localization_loss_weight
        self._second_stage_cls_loss_weight = second_stage_classification_loss_weight
        self._second_stage_mask_loss_weight = second_stage_mask_loss_weight
        self._second_stage_motion_loss_weight = second_stage_motion_loss_weight
        self._hard_example_miner = hard_example_miner
        self._first_stage_predict_camera_motion = first_stage_predict_camera_motion
        self._first_stage_camera_motion_loss_weight = first_stage_camera_motion_loss_weight
        self._first_stage_camera_motion_arg_scope = first_stage_camera_motion_arg_scope
        self._second_stage_motion_loss_from_flow = second_stage_motion_loss_from_flow
        self._first_stage_camera_motion_loss_from_flow = first_stage_camera_motion_loss_from_flow
        self._parallel_iterations = parallel_iterations

    @property
    def first_stage_feature_extractor_scope(self):
        return 'FirstStageFeatureExtractor'

    @property
    def second_stage_feature_extractor_scope(self):
        return 'SecondStageFeatureExtractor'

    @property
    def first_stage_box_predictor_scope(self):
        return 'FirstStageBoxPredictor'

    @property
    def second_stage_box_predictor_scope(self):
        return 'SecondStageBoxPredictor'

    @property
    def max_num_proposals(self):
        """Max number of proposals (to pad to) for each image in the input batch.
        At training time, this is set to be the `second_stage_batch_size` if hard
        example miner is not configured, else it is set to
        `first_stage_max_proposals`. At inference time, this is always set to
        `first_stage_max_proposals`.
        Returns:
          A positive integer.
        """
        if self._is_training and not self._hard_example_miner:
            return self._second_stage_batch_size
        return self._first_stage_max_proposals

    def preprocess(self, inputs):
        """Feature-extractor specific preprocessing.
        See base class.
        For Faster R-CNN, we perform image resizing in the base class --- each
        class subclassing FasterRCNNMetaArch is responsible for any additional
        preprocessing (e.g., scaling pixel values to be in [-1, 1]).
        Args:
          inputs: a [batch, height_in, width_in, channels] float tensor representing
            a batch of images with values between 0 and 255.0.
        Returns:
          preprocessed_inputs: a [batch, height_out, width_out, channels] float
            tensor representing a batch of images.
        Raises:
          ValueError: if inputs tensor does not have type tf.float32
        """
        if inputs.dtype is not tf.float32:
            raise ValueError('`preprocess` expects a tf.float32 tensor')
        with tf.name_scope('Preprocessor'):
            resized_inputs = tf.map_fn(self._image_resizer_fn,
                                       elems=inputs,
                                       dtype=tf.float32,
                                       parallel_iterations=self._parallel_iterations)
            return self._feature_extractor.preprocess(resized_inputs)

    def predict(self, preprocessed_inputs):
        """Predicts unpostprocessed tensors from input tensor.
        This function takes an input batch of images and runs it through the
        forward pass of the network to yield "raw" un-postprocessed predictions.
        If `first_stage_only` is True, this function only returns first stage
        RPN predictions (un-postprocessed).  Otherwise it returns both
        first stage RPN predictions as well as second stage box classifier
        predictions.
        Other remarks:
        + Anchor pruning vs. clipping: following the recommendation of the Faster
        R-CNN paper, we prune anchors that venture outside the image window at
        training time and clip anchors to the image window at inference time.
        + Proposal padding: as described at the top of the file, proposals are
        padded to self._max_num_proposals and flattened so that proposals from all
        images within the input batch are arranged along the same batch dimension.
        Args:
          preprocessed_inputs: a [batch, height, width, channels] float tensor
            representing a batch of images.
        Returns:
          prediction_dict: a dictionary holding "raw" prediction tensors:
            1) rpn_box_predictor_features: A list of 4-D float32 tensors with shape
              [batch_size, height, width, depth] to be used for predicting proposal
              boxes and corresponding objectness scores.
            2) rpn_features_to_crop: A list of 4-D float32 tensors with shape
              [batch_size, height, width, depth] representing image features to crop
              using the proposal boxes predicted by the RPN.
            3) image_shape: a 1-D tensor of shape [4] representing the input
              image shape.
            4) rpn_box_encodings:  3-D float tensor of shape
              [batch_size, num_anchors, self._box_coder.code_size] containing
              predicted boxes.
            5) rpn_objectness_predictions_with_background: 3-D float tensor of shape
              [batch_size, num_anchors, 2] containing class
              predictions (logits) for each of the anchors.  Note that this
              tensor *includes* background class predictions (at class index 0).
            6) anchors: A 2-D tensor of shape [num_anchors, 4] representing anchors
              for the first stage RPN (in absolute coordinates).  Note that
              `num_anchors` can differ depending on whether the model is created in
              training or inference mode.
            (and if first_stage_only=False):
            7) refined_box_encodings: a 3-D tensor with shape
              [total_num_proposals, num_classes, 4] representing predicted
              (final) refined box encodings, where
              total_num_proposals=batch_size*self._max_num_proposals
            8) class_predictions_with_background: a 3-D tensor with shape
              [total_num_proposals, num_classes + 1] containing class
              predictions (logits) for each of the anchors, where
              total_num_proposals=batch_size*self._max_num_proposals.
              Note that this tensor *includes* background class predictions
              (at class index 0).
            9) num_proposals: An int32 tensor of shape [batch_size] representing the
              number of proposals generated by the RPN.  `num_proposals` allows us
              to keep track of which entries are to be treated as zero paddings and
              which are not since we always pad the number of proposals to be
              `self.max_num_proposals` for each image.
            10) proposal_boxes: A float32 tensor of shape
              [batch_size, self.max_num_proposals, 4] representing
              decoded proposal bounding boxes (in absolute coordinates).
            11) mask_predictions: (optional) a 4-D tensor with shape
              [total_num_padded_proposals, num_classes, mask_height, mask_width]
              containing instance mask predictions.
            12) motion_predictions: (optional) a 4-D tensor with shape
              [total_num_padded_proposals, num_classes, num_motion_params]
              containing instance mask predictions.
        """
        (rpn_box_predictor_features, rpn_features_to_crop, anchors_boxlist,
         image_shape, rpn_bottleneck_features
         ) = self._extract_rpn_feature_maps(preprocessed_inputs)
        (rpn_box_encodings, rpn_objectness_predictions_with_background
         ) = self._predict_rpn_proposals(rpn_box_predictor_features)

        # The Faster R-CNN paper recommends pruning anchors that venture outside
        # the image window at training time and clipping at inference time.
        clip_window = tf.to_float(
            tf.stack([0, 0, image_shape[1], image_shape[2]]))
        clip = False  # TODO add param to proto
        if self._is_training and clip:
            (rpn_box_encodings, rpn_objectness_predictions_with_background,
             anchors_boxlist) = self._remove_invalid_anchors_and_predictions(
                 rpn_box_encodings, rpn_objectness_predictions_with_background,
                 anchors_boxlist, clip_window)
        else:
            anchors_boxlist = box_list_ops.clip_to_window(
                anchors_boxlist, clip_window)

        anchors = anchors_boxlist.get()
        prediction_dict = {
            'rpn_box_predictor_features': rpn_box_predictor_features,
            'rpn_features_to_crop': rpn_features_to_crop,
            'image_shape': image_shape,
            'rpn_box_encodings': rpn_box_encodings,
            'rpn_objectness_predictions_with_background':
            rpn_objectness_predictions_with_background,
            'anchors': anchors
        }

        if self._first_stage_predict_camera_motion:
            prediction_dict.update(self._predict_camera_motion(
                rpn_bottleneck_features))

        if not self._first_stage_only:
            prediction_dict.update(self._predict_second_stage(
                rpn_box_encodings,
                rpn_objectness_predictions_with_background,
                rpn_features_to_crop,
                anchors, image_shape))
        return prediction_dict

    def _predict_camera_motion(self, rpn_bottleneck_features):
        camera_features = self._feature_extractor._extract_camera_features(
            rpn_bottleneck_features, scope='CameraFeatures')
        with slim.arg_scope(self._first_stage_camera_motion_arg_scope):
            camera_features_conv = slim.conv2d(
                camera_features,
                512,
                kernel_size=[1, 1],
                activation_fn=tf.nn.relu)
            #camera_features_resized = tf.reduce_mean(camera_features, [1, 2], keep_dims=True)
            camera_features_resized = tf.image.resize_bilinear(
                camera_features_conv, [7, 7])
            camera_features_flat = slim.flatten(camera_features_resized)
            for _ in range(2):
                camera_features_flat = slim.fully_connected(
                    camera_features_flat, 1024)
                # camera_features_flat = slim.dropout(
                #    camera_features_flat,
                #    keep_prob=0.5,
                #    is_training=self._is_training)
            camera_motion = slim.fully_connected(
                camera_features_flat,
                7,  # self._num_camera_motion_params, # TODO
                weights_initializer=tf.truncated_normal_initializer(
                    0.0, 0.0001),
                activation_fn=None,
                scope='CameraMotionPredictor')
        prediction_dict = {
            'camera_motion': camera_motion}
        return prediction_dict

    def _predict_second_stage(self, rpn_box_encodings,
                              rpn_objectness_predictions_with_background,
                              rpn_features_to_crop,
                              anchors,
                              image_shape):
        """Predicts the output tensors from second stage of Faster R-CNN.
        Args:
          rpn_box_encodings: 4-D float tensor of shape
            [batch_size, num_valid_anchors, self._box_coder.code_size] containing
            predicted boxes.
          rpn_objectness_predictions_with_background: 2-D float tensor of shape
            [batch_size, num_valid_anchors, 2] containing class
            predictions (logits) for each of the anchors.  Note that this
            tensor *includes* background class predictions (at class index 0).
          rpn_features_to_crop: A list of 4-D float32 tensors with shapes
            [batch_size, height, width, depth] representing image features at multiple
            resolutions to crop using the proposal boxes predicted by the RPN.
          anchors: 2-D float tensor of shape
            [num_anchors, self._box_coder.code_size].
          image_shape: A 1D int32 tensors of size [4] containing the image shape.
        Returns:
          prediction_dict: a dictionary holding "raw" prediction tensors:
            1) refined_box_encodings: a 3-D tensor with shape
              [total_num_proposals, num_classes, 4] representing predicted
              (final) refined box encodings, where
              total_num_proposals=batch_size*self._max_num_proposals
            2) class_predictions_with_background: a 3-D tensor with shape
              [total_num_proposals, num_classes + 1] containing class
              predictions (logits) for each of the anchors, where
              total_num_proposals=batch_size*self._max_num_proposals.
              Note that this tensor *includes* background class predictions
              (at class index 0).
            3) num_proposals: An int32 tensor of shape [batch_size] representing the
              number of proposals generated by the RPN.  `num_proposals` allows us
              to keep track of which entries are to be treated as zero paddings and
              which are not since we always pad the number of proposals to be
              `self.max_num_proposals` for each image.
            4) proposal_boxes: A float32 tensor of shape
              [batch_size, self.max_num_proposals, 4] representing
              decoded proposal bounding boxes (in absolute coordinates).
            5) mask_predictions: (optional) a 4-D tensor with shape
              [total_num_padded_proposals, num_classes, mask_height, mask_width]
              containing instance mask predictions.
            6) motion_predictions: (optional) a 4-D tensor with shape
              [total_num_padded_proposals, num_classes, num_motion_params]
              containing instance mask predictions.
        """
        proposal_boxes_normalized, _, num_proposals = self._postprocess_rpn(
            rpn_box_encodings, rpn_objectness_predictions_with_background,
            anchors, image_shape)

        absolute_proposal_boxes = ops.normalized_to_image_coordinates(
            proposal_boxes_normalized, image_shape, self._parallel_iterations)

        flattened_proposal_feature_maps = (
            self._compute_second_stage_input_feature_maps(
                rpn_features_to_crop,
                proposal_boxes_normalized, absolute_proposal_boxes))

        box_classifier_features = (
            self._feature_extractor.extract_box_classifier_features(
                flattened_proposal_feature_maps,
                scope=self.second_stage_feature_extractor_scope))

        box_predictions = self._mask_rcnn_box_predictor.predict(
            box_classifier_features,
            num_predictions_per_location=1,
            scope=self.second_stage_box_predictor_scope)
        refined_box_encodings = tf.squeeze(
            box_predictions[box_predictor.BOX_ENCODINGS], axis=1)
        class_predictions_with_background = tf.squeeze(box_predictions[
            box_predictor.CLASS_PREDICTIONS_WITH_BACKGROUND], axis=1)

        prediction_dict = {
            'refined_box_encodings': refined_box_encodings,
            'class_predictions_with_background':
            class_predictions_with_background,
            'num_proposals': num_proposals,
            'proposal_boxes': absolute_proposal_boxes,
        }

        if box_predictor.MASK_PREDICTIONS in box_predictions:
            mask_predictions = tf.squeeze(
                box_predictions[box_predictor.MASK_PREDICTIONS], axis=1)
            prediction_dict['mask_predictions'] = mask_predictions

        if box_predictor.MOTION_PREDICTIONS in box_predictions:
            motion_predictions = tf.squeeze(
                box_predictions[box_predictor.MOTION_PREDICTIONS], axis=1)
            prediction_dict['motion_predictions'] = motion_predictions

        return prediction_dict

    def _extract_rpn_feature_maps(self, preprocessed_inputs):
        """Extracts RPN features.
        This function extracts two feature maps: a feature map to be directly
        fed to a box predictor (to predict location and objectness scores for
        proposals) and a feature map from which to crop regions which will then
        be sent to the second stage box classifier.
        Args:
          preprocessed_inputs: a [batch, height, width, channels] image tensor.
        Returns:
          rpn_box_predictor_features: A list of 4-D float32 tensors with shapes
            [batch, height, width, depth] to be used for predicting proposal boxes
            and corresponding objectness scores.
          rpn_features_to_crop: A list of 4-D float32 tensors with shapes
            [batch, height, width, depth] representing image features at multiple
            resolutions to crop using the proposals boxes.
          anchors: A BoxList representing anchors (for the RPN) in
            absolute coordinates.
          image_shape: A 1-D tensor representing the input image shape.
          rpn_bottleneck_features: A 4-D float32 tensor representing the bottleneck
            features of the feature extractor.
        """
        image_shape = tf.shape(preprocessed_inputs)
        rpn_features_to_crop, rpn_bottleneck_features = (
            self._feature_extractor.extract_proposal_features(
                preprocessed_inputs, scope=self.first_stage_feature_extractor_scope))

        if not isinstance(rpn_features_to_crop, list):
            rpn_features_to_crop = [rpn_features_to_crop]
        feature_map_sizes = []
        for feature_map in rpn_features_to_crop:
            feature_map_shape = tf.shape(feature_map)
            feature_map_sizes.append(
                (feature_map_shape[1], feature_map_shape[2]))

        if isinstance(self._first_stage_anchor_generator,
                      multiple_grid_anchor_generator.
                      MultipleGridAnchorGenerator):
            anchors = self._first_stage_anchor_generator.generate(
                feature_map_sizes,
                anchor_strides=(self._feature_extractor.
                                extracted_proposal_features_strides))
        else:
            anchors = self._first_stage_anchor_generator.generate(
                feature_map_sizes)

        with slim.arg_scope(self._first_stage_box_predictor_arg_scope):
            rpn_box_predictor_features = []
            kernel_size = self._first_stage_box_predictor_kernel_size
            for feature_map in rpn_features_to_crop:
                rpn_box_predictor_feature_map = slim.conv2d(
                    feature_map,
                    self._first_stage_box_predictor_depth,
                    kernel_size=[kernel_size, kernel_size],
                    rate=self._first_stage_atrous_rate,
                    activation_fn=tf.nn.relu6)
                rpn_box_predictor_features.append(
                    rpn_box_predictor_feature_map)
        return (rpn_box_predictor_features, rpn_features_to_crop,
                anchors, image_shape, rpn_bottleneck_features)

    def _predict_rpn_proposals(self, rpn_box_predictor_features):
        """Adds box predictors to RPN feature map to predict proposals.
        Note resulting tensors will not have been postprocessed.
        Args:
          rpn_box_predictor_features: A list of 4-D float32 tensors with shapes
            [batch, height, width, depth] to be used for predicting proposal boxes
            and corresponding objectness scores.
        Returns:
          box_encodings: 3-D float tensor of shape
            [batch_size, num_anchors, self._box_coder.code_size] containing
            predicted boxes.
          objectness_predictions_with_background: 3-D float tensor of shape
            [batch_size, num_anchors, 2] containing class
            predictions (logits) for each of the anchors.  Note that this
            tensor *includes* background class predictions (at class index 0).
        Raises:
          RuntimeError: if the anchor generator does not generates anchors for
            each of the feature maps.
        """
        num_anchors_per_location = (
            self._first_stage_anchor_generator.num_anchors_per_location())
        if len(num_anchors_per_location) != len(rpn_box_predictor_features):
            raise RuntimeError('anchor_generator is expected to generate anchors '
                               'corresponding to a each feature map.')

        box_encodings_list = []
        objectness_predictions_with_background_list = []
        for i, feature_map in enumerate(rpn_box_predictor_features):
            box_predictions = self._first_stage_box_predictor.predict(
                feature_map,
                num_anchors_per_location[i],
                scope=self.first_stage_box_predictor_scope + str(i))
            box_encodings_list.append(
                box_predictions[box_predictor.BOX_ENCODINGS])
            objectness_predictions_with_background_list.append(
                box_predictions[box_predictor.CLASS_PREDICTIONS_WITH_BACKGROUND])
        box_encodings = tf.concat(box_encodings_list, axis=1)
        objectness_predictions_with_background = tf.concat(
            objectness_predictions_with_background_list, axis=1)

        return (tf.squeeze(box_encodings, axis=2),
                objectness_predictions_with_background)

    def _remove_invalid_anchors_and_predictions(
            self,
            box_encodings,
            objectness_predictions_with_background,
            anchors_boxlist,
            clip_window):
        """Removes anchors that (partially) fall outside an image.
        Also removes associated box encodings and objectness predictions.
        Args:
          box_encodings: 3-D float tensor of shape
            [batch_size, num_anchors, self._box_coder.code_size] containing
            predicted boxes.
          objectness_predictions_with_background: 3-D float tensor of shape
            [batch_size, num_anchors, 2] containing class
            predictions (logits) for each of the anchors.  Note that this
            tensor *includes* background class predictions (at class index 0).
          anchors_boxlist: A BoxList representing num_anchors anchors (for the RPN)
            in absolute coordinates.
          clip_window: a 1-D tensor representing the [ymin, xmin, ymax, xmax]
            extent of the window to clip/prune to.
        Returns:
          box_encodings: 4-D float tensor of shape
            [batch_size, num_valid_anchors, self._box_coder.code_size] containing
            predicted boxes, where num_valid_anchors <= num_anchors
          objectness_predictions_with_background: 2-D float tensor of shape
            [batch_size, num_valid_anchors, 2] containing class
            predictions (logits) for each of the anchors, where
            num_valid_anchors <= num_anchors.  Note that this
            tensor *includes* background class predictions (at class index 0).
          anchors: A BoxList representing num_valid_anchors anchors (for the RPN) in
            absolute coordinates.
        """
        pruned_anchors_boxlist, keep_indices = box_list_ops.prune_outside_window(
            anchors_boxlist, clip_window)

        def _batch_gather_kept_indices(predictions_tensor):
            return tf.map_fn(
                partial(tf.gather, indices=keep_indices),
                elems=predictions_tensor,
                dtype=tf.float32,
                parallel_iterations=self._parallel_iterations,
                back_prop=True)
        return (_batch_gather_kept_indices(box_encodings),
                _batch_gather_kept_indices(
                    objectness_predictions_with_background),
                pruned_anchors_boxlist)

    def _flatten_first_two_dimensions(self, inputs):
        """Flattens `K-d` tensor along batch dimension to be a `(K-1)-d` tensor.
        Converts `inputs` with shape [A, B, ..., depth] into a tensor of shape
        [A * B, ..., depth].
        Args:
          inputs: A float tensor with shape [A, B, ..., depth].  Note that the first
            two and last dimensions must be statically defined.
        Returns:
          A float tensor with shape [A * B, ..., depth] (where the first and last
            dimension are statically defined.
        """
        combined_shape = shape_utils.combined_static_and_dynamic_shape(inputs)
        flattened_shape = tf.stack([combined_shape[0] * combined_shape[1]] +
                                   combined_shape[2:])
        return tf.reshape(inputs, flattened_shape)

    def postprocess(self, prediction_dict):
        """Convert prediction tensors to final detections.
        This function converts raw predictions tensors to final detection results.
        See base class for output format conventions.  Note also that by default,
        scores are to be interpreted as logits, but if a score_converter is used,
        then scores are remapped (and may thus have a different interpretation).
        If first_stage_only=True, the returned results represent proposals from the
        first stage RPN and are padded to have self.max_num_proposals for each
        image; otherwise, the results can be interpreted as multiclass detections
        from the full two-stage model and are padded to self._max_detections.
        Args:
          prediction_dict: a dictionary holding prediction tensors (see the
            documentation for the predict method.  If first_stage_only=True, we
            expect prediction_dict to contain `rpn_box_encodings`,
            `rpn_objectness_predictions_with_background`, `rpn_features_to_crop`,
            `image_shape`, and `anchors` fields.  Otherwise we expect
            prediction_dict to additionally contain `refined_box_encodings`,
            `class_predictions_with_background`, `num_proposals`,
            `proposal_boxes` and, optionally, `mask_predictions` fields.
        Returns:
          detections: a dictionary containing the following fields
            detection_boxes: [batch, max_detection, 4]
            detection_scores: [batch, max_detections]
            detection_classes: [batch, max_detections]
              (this entry is only created if rpn_mode=False)
            num_detections: [batch]
        """
        with tf.name_scope('FirstStagePostprocessor'):
            image_shape = prediction_dict['image_shape']
            if self._first_stage_only:
                proposal_boxes, proposal_scores, num_proposals = self._postprocess_rpn(
                    prediction_dict['rpn_box_encodings'],
                    prediction_dict['rpn_objectness_predictions_with_background'],
                    prediction_dict['anchors'],
                    image_shape)
                return {
                    'detection_boxes': proposal_boxes,
                    'detection_scores': proposal_scores,
                    'num_detections': num_proposals
                }
        with tf.name_scope('SecondStagePostprocessor'):
            detections_dict = self._postprocess_box_classifier(
                prediction_dict['refined_box_encodings'],
                prediction_dict['class_predictions_with_background'],
                prediction_dict['proposal_boxes'],
                prediction_dict['num_proposals'],
                image_shape,
                prediction_dict['rpn_features_to_crop'])

            if 'camera_motion' in prediction_dict:
                detections_dict['camera_motion'] = prediction_dict['camera_motion']

            return detections_dict

    def _postprocess_rpn(self,
                         rpn_box_encodings_batch,
                         rpn_objectness_predictions_with_background_batch,
                         anchors,
                         image_shape):
        """Converts first stage prediction tensors from the RPN to proposals.
        This function decodes the raw RPN predictions, runs non-max suppression
        on the result.
        Note that the behavior of this function is slightly modified during
        training --- specifically, we stop the gradient from passing through the
        proposal boxes and we only return a balanced sampled subset of proposals
        with size `second_stage_batch_size`.
        Args:
          rpn_box_encodings_batch: A 3-D float32 tensor of shape
            [batch_size, num_anchors, self._box_coder.code_size] containing
            predicted proposal box encodings.
          rpn_objectness_predictions_with_background_batch: A 3-D float tensor of
            shape [batch_size, num_anchors, 2] containing objectness predictions
            (logits) for each of the anchors with 0 corresponding to background
            and 1 corresponding to object.
          anchors: A 2-D tensor of shape [num_anchors, 4] representing anchors
            for the first stage RPN.  Note that `num_anchors` can differ depending
            on whether the model is created in training or inference mode.
          image_shape: A 1-D tensor representing the input image shape.
        Returns:
          proposal_boxes: A float tensor with shape
            [batch_size, max_num_proposals, 4] representing the (potentially zero
            padded) proposal boxes for all images in the batch.  These boxes are
            represented as normalized coordinates.
          proposal_scores:  A float tensor with shape
            [batch_size, max_num_proposals] representing the (potentially zero
            padded) proposal objectness scores for all images in the batch.
          num_proposals: A Tensor of type `int32`. A 1-D tensor of shape [batch]
            representing the number of proposals predicted for each image in
            the batch.
        """
        rpn_box_encodings_batch = tf.expand_dims(
            rpn_box_encodings_batch, axis=2)
        rpn_encodings_shape = shape_utils.combined_static_and_dynamic_shape(
            rpn_box_encodings_batch)
        tiled_anchor_boxes = tf.tile(
            tf.expand_dims(anchors, 0), [rpn_encodings_shape[0], 1, 1])
        proposal_boxes = self._batch_decode_boxes(rpn_box_encodings_batch,
                                                  tiled_anchor_boxes)
        proposal_boxes = tf.squeeze(proposal_boxes, axis=2)
        rpn_objectness_softmax_without_background = tf.nn.softmax(
            rpn_objectness_predictions_with_background_batch)[:, :, 1]
        clip_window = tf.to_float(
            tf.stack([0, 0, image_shape[1], image_shape[2]]))
        (proposal_boxes, proposal_scores, _, _, _,
         num_proposals) = post_processing.batch_multiclass_non_max_suppression(
             tf.expand_dims(proposal_boxes, axis=2),
             tf.expand_dims(rpn_objectness_softmax_without_background,
                            axis=2),
             self._first_stage_nms_score_threshold,
             self._first_stage_nms_iou_threshold,
             self._first_stage_max_proposals,
             self._first_stage_max_proposals,
             clip_window=clip_window)
        if self._is_training:
            proposal_boxes = tf.stop_gradient(proposal_boxes)
            if not self._hard_example_miner:
                (groundtruth_boxlists, groundtruth_classes_with_background_list, _, _,
                 ) = self._format_groundtruth_data(image_shape)
                (proposal_boxes, proposal_scores,
                 num_proposals) = self._unpad_proposals_and_sample_box_classifier_batch(
                     proposal_boxes, proposal_scores, num_proposals,
                     groundtruth_boxlists, groundtruth_classes_with_background_list)
        # normalize proposal boxes
        proposal_boxes_reshaped = tf.reshape(proposal_boxes, [-1, 4])
        normalized_proposal_boxes_reshaped = box_list_ops.to_normalized_coordinates(
            box_list.BoxList(proposal_boxes_reshaped),
            image_shape[1], image_shape[2], check_range=False).get()
        proposal_boxes = tf.reshape(normalized_proposal_boxes_reshaped,
                                    [-1, proposal_boxes.shape[1].value, 4])
        return proposal_boxes, proposal_scores, num_proposals

    def _unpad_proposals_and_sample_box_classifier_batch(
            self,
            proposal_boxes,
            proposal_scores,
            num_proposals,
            groundtruth_boxlists,
            groundtruth_classes_with_background_list):
        """Unpads proposals and samples a minibatch for second stage.
        Args:
          proposal_boxes: A float tensor with shape
            [batch_size, num_proposals, 4] representing the (potentially zero
            padded) proposal boxes for all images in the batch.  These boxes are
            represented as normalized coordinates.
          proposal_scores:  A float tensor with shape
            [batch_size, num_proposals] representing the (potentially zero
            padded) proposal objectness scores for all images in the batch.
          num_proposals: A Tensor of type `int32`. A 1-D tensor of shape [batch]
            representing the number of proposals predicted for each image in
            the batch.
          groundtruth_boxlists: A list of BoxLists containing (absolute) coordinates
            of the groundtruth boxes.
          groundtruth_classes_with_background_list: A list of 2-D one-hot
            (or k-hot) tensors of shape [num_boxes, num_classes+1] containing the
            class targets with the 0th index assumed to map to the background class.
        Returns:
          proposal_boxes: A float tensor with shape
            [batch_size, second_stage_batch_size, 4] representing the (potentially
            zero padded) proposal boxes for all images in the batch.  These boxes
            are represented as normalized coordinates.
          proposal_scores:  A float tensor with shape
            [batch_size, second_stage_batch_size] representing the (potentially zero
            padded) proposal objectness scores for all images in the batch.
          num_proposals: A Tensor of type `int32`. A 1-D tensor of shape [batch]
            representing the number of proposals predicted for each image in
            the batch.
        """
        single_image_proposal_box_sample = []
        single_image_proposal_score_sample = []
        single_image_num_proposals_sample = []
        for (single_image_proposal_boxes,
             single_image_proposal_scores,
             single_image_num_proposals,
             single_image_groundtruth_boxlist,
             single_image_groundtruth_classes_with_background) in zip(
                 tf.unstack(proposal_boxes),
                 tf.unstack(proposal_scores),
                 tf.unstack(num_proposals),
                 groundtruth_boxlists,
                 groundtruth_classes_with_background_list):
            static_shape = single_image_proposal_boxes.get_shape()
            sliced_static_shape = tf.TensorShape([tf.Dimension(None),
                                                  static_shape.dims[-1]])
            single_image_proposal_boxes = tf.slice(
                single_image_proposal_boxes,
                [0, 0],
                [single_image_num_proposals, -1])
            single_image_proposal_boxes.set_shape(sliced_static_shape)

            single_image_proposal_scores = tf.slice(single_image_proposal_scores,
                                                    [0],
                                                    [single_image_num_proposals])
            single_image_boxlist = box_list.BoxList(
                single_image_proposal_boxes)
            single_image_boxlist.add_field(fields.BoxListFields.scores,
                                           single_image_proposal_scores)
            sampled_boxlist = self._sample_box_classifier_minibatch(
                single_image_boxlist,
                single_image_groundtruth_boxlist,
                single_image_groundtruth_classes_with_background)
            sampled_padded_boxlist = box_list_ops.pad_or_clip_box_list(
                sampled_boxlist,
                num_boxes=self._second_stage_batch_size)
            single_image_num_proposals_sample.append(tf.minimum(
                sampled_boxlist.num_boxes(),
                self._second_stage_batch_size))
            bb = sampled_padded_boxlist.get()
            single_image_proposal_box_sample.append(bb)
            single_image_proposal_score_sample.append(
                sampled_padded_boxlist.get_field(fields.BoxListFields.scores))
        return (tf.stack(single_image_proposal_box_sample),
                tf.stack(single_image_proposal_score_sample),
                tf.stack(single_image_num_proposals_sample))

    def _format_groundtruth_data(self, image_shape):
        """Helper function for preparing groundtruth data for target assignment.
        In order to be consistent with the model.DetectionModel interface,
        groundtruth boxes are specified in normalized coordinates and classes are
        specified as label indices with no assumed background category.  To prepare
        for target assignment, we:
        1) convert boxes to absolute coordinates,
        2) add a background class at class index 0
        Args:
          image_shape: A 1-D int32 tensor of shape [4] representing the shape of the
            input image batch.
        Returns:
          groundtruth_boxlists: A list of BoxLists containing (absolute) coordinates
            of the groundtruth boxes.
          groundtruth_classes_with_background_list: A list of 2-D one-hot
            (or k-hot) tensors of shape [num_boxes, num_classes+1] containing the
            class targets with the 0th index assumed to map to the background class.
          groundtruth_masks_list: a list of 2-D tf.bool tensors of
            shape [num_boxes, height_in, width_in] containing instance
            masks with values in {0, 1}. Will be None if no masks are provided.
          groundtruth_motions_list: a list of 2-D tf.float32 tensors of
            shape [num_boxes, num_motion_gt_params] containing instance
            motions. Will be None if no motions are provided.
        """
        groundtruth_boxlists = [
            box_list_ops.to_absolute_coordinates(
                box_list.BoxList(boxes), image_shape[1], image_shape[2])
            for boxes in self.groundtruth_lists(fields.BoxListFields.boxes)]
        groundtruth_classes_with_background_list = [
            tf.to_float(
                tf.pad(one_hot_encoding, [[0, 0], [1, 0]], mode='CONSTANT'))
            for one_hot_encoding in self.groundtruth_lists(
                fields.BoxListFields.classes)]
        try:
            groundtruth_masks_list = self.groundtruth_lists(
                fields.BoxListFields.masks)
        except RuntimeError:
            groundtruth_masks_list = None
        try:
            groundtruth_motions_list = self.groundtruth_lists(
                fields.BoxListFields.motions)
        except RuntimeError:
            groundtruth_motions_list = None
        return (groundtruth_boxlists, groundtruth_classes_with_background_list,
                groundtruth_masks_list, groundtruth_motions_list)

    def _sample_box_classifier_minibatch(self,
                                         proposal_boxlist,
                                         groundtruth_boxlist,
                                         groundtruth_classes_with_background):
        """Samples a mini-batch of proposals to be sent to the box classifier.
        Helper function for self._postprocess_rpn.
        Args:
          proposal_boxlist: A BoxList containing K proposal boxes in absolute
            coordinates.
          groundtruth_boxlist: A Boxlist containing N groundtruth object boxes in
            absolute coordinates.
          groundtruth_classes_with_background: A tensor with shape
            `[N, self.num_classes + 1]` representing groundtruth classes. The
            classes are assumed to be k-hot encoded, and include background as the
            zero-th class.
        Returns:
          a BoxList contained sampled proposals.
        """
        (cls_targets, cls_weights, _, _, _) = self._detector_target_assigner.assign(
            proposal_boxlist, groundtruth_boxlist,
            groundtruth_classes_with_background)
        # Selects all boxes as candidates if none of them is selected according
        # to cls_weights. This could happen as boxes within certain IOU ranges
        # are ignored. If triggered, the selected boxes will still be ignored
        # during loss computation.
        cls_weights += tf.to_float(tf.equal(tf.reduce_sum(cls_weights), 0))
        positive_indicator = tf.greater(tf.argmax(cls_targets, axis=1), 0)
        sampled_indices = self._second_stage_sampler.subsample(
            tf.cast(cls_weights, tf.bool),
            self._second_stage_batch_size,
            positive_indicator)
        return box_list_ops.boolean_mask(proposal_boxlist, sampled_indices)

    def _compute_second_stage_input_feature_maps(self, features_to_crop,
                                                 proposal_boxes_normalized,
                                                 absolute_proposal_boxes):
        """Crops to a set of proposals from the feature maps for a batch of images.
        Helper function for self._postprocess_rpn. This function calls
        `tf.image.crop_and_resize` to create the feature map to be passed to the
        second stage box classifier for each proposal.
        Args:
          features_to_crop: A list of float32 tensors with shape
            [batch_size, height, width, depth]
          proposal_boxes_normalized: A float32 tensor with shape [batch_size,
            num_proposals, box_code_size] containing proposal boxes in
            normalized coordinates.
          absolute_proposal_boxes: same boxes as proposal_boxes_normalized, in
            absolute coordinates.
        Returns:
          A float32 tensor with shape [K, new_height, new_width, depth].
        """
        def get_box_inds(proposals):
            proposals_shape = proposals.get_shape().as_list()
            if any(dim is None for dim in proposals_shape):
                proposals_shape = tf.shape(proposals)
            ones_mat = tf.ones(proposals_shape[:2], dtype=tf.int32)
            multiplier = tf.expand_dims(
                tf.range(start=0, limit=proposals_shape[0]), 1)
            return tf.reshape(ones_mat * multiplier, [-1])

        if len(features_to_crop) == 1:
            cropped_regions = tf.image.crop_and_resize(
                features_to_crop[0],
                self._flatten_first_two_dimensions(proposal_boxes_normalized),
                get_box_inds(proposal_boxes_normalized),
                (self._initial_crop_size, self._initial_crop_size))
            return slim.max_pool2d(
                cropped_regions,
                [self._maxpool_kernel_size, self._maxpool_kernel_size],
                stride=self._maxpool_stride)
        else:
            return self._crop_from_feature_pyramid(
                features_to_crop,
                self._flatten_first_two_dimensions(proposal_boxes_normalized),
                self._flatten_first_two_dimensions(absolute_proposal_boxes),
                self._initial_crop_size,
                self._initial_crop_size)

    def _crop_from_feature_pyramid(self, feature_pyramid,
                                   normalized_boxes,
                                   absolute_boxes,
                                   crop_height, crop_width):
        """Crops boxes from appropriate levels of a feature pyramid.
        Helper function for self._compute_second_stage_input_feature_maps.
        Args:
          feature_pyramid: A list of float32 tensors with shape
            [batch_size, height_i, width_i, depth].
          normalized_boxes: A float32 tensor with shape [batch_size,
            num_proposals, box_code_size] containing boxes in
            normalized coordinates.
          absolute_boxes: same boxes as normalized_boxes, in
            absolute coordinates.
          crop_height: Height of crops.
          crop_width: Width of crops.
        Returns:
          A float32 tensor with shape [K, crop_height, crop_width, depth].
        """
        # TODO assert that the generator is a FpnAnchorGenerator if we use the FPN arch
        # and the GridAnchorGenerator if we use the standard arch
        layer_indices = self._first_stage_anchor_generator.assign_boxes_to_layers(
            absolute_boxes)

        cropped_regions_list = []
        assigned_box_indices_list = []
        for i, feature_map in enumerate(feature_pyramid):
            assigned_box_indices = tf.where(tf.equal(layer_indices, i))
            assigned_boxes = tf.gather_nd(
                normalized_boxes, assigned_box_indices)
            cropped_regions = tf.image.crop_and_resize(
                feature_map,
                assigned_boxes,
                tf.zeros(tf.shape(assigned_boxes)[:1], dtype=tf.int32),
                (crop_height, crop_width))
            cropped_regions_list.append(cropped_regions)
            assigned_box_indices_list.append(assigned_box_indices)

        cropped_regions = tf.concat(cropped_regions_list, axis=0)
        assigned_box_indices = tf.to_int32(
            tf.concat(assigned_box_indices_list, axis=0))

        return tf.scatter_nd(
            assigned_box_indices,
            cropped_regions,
            tf.shape(cropped_regions))

    def _postprocess_box_classifier(self,
                                    refined_box_encodings,
                                    class_predictions_with_background,
                                    proposal_boxes,
                                    num_proposals,
                                    image_shape,
                                    rpn_features_to_crop,
                                    mask_threshold=0.5):
        """Converts predictions from the second stage box classifier to detections.
        Args:
          refined_box_encodings: a 3-D tensor with shape
            [total_num_padded_proposals, num_classes, 4] representing predicted
            (final) refined box encodings.
          class_predictions_with_background: a 3-D tensor with shape
            [total_num_padded_proposals, num_classes + 1] containing class
            predictions (logits) for each of the proposals.  Note that this tensor
            *includes* background class predictions (at class index 0).
          proposal_boxes: [batch_size, self.max_num_proposals, 4] representing
            decoded proposal bounding boxes.
          num_proposals: A Tensor of type `int32`. A 1-D tensor of shape [batch]
            representing the number of proposals predicted for each image in
            the batch.
          image_shape: a 1-D tensor representing the input image shape.
          rpn_features_to_crop: A list of 4-D float32 tensors with shape
            [batch_size, height, width, depth] representing image features to crop
            using the refined boxes.
          mask_threshold: a scalar threshold determining which mask values are
            rounded to 0 or 1.
        Returns:
          A dictionary containing:
            `detection_boxes`: [batch, max_detection, 4]
            `detection_scores`: [batch, max_detections]
            `detection_classes`: [batch, max_detections]
            `num_detections`: [batch]
            `detection_masks`:
              (optional) [batch, max_detections, mask_height, mask_width]
            `detection_motions`:
              (optional) [batch, max_detections, num_motion_params]
        """
        refined_box_encodings_batch = tf.reshape(refined_box_encodings,
                                                 [-1, self.max_num_proposals,
                                                  self.num_classes,
                                                  self._box_coder.code_size])
        class_predictions_with_background_batch = tf.reshape(
            class_predictions_with_background,
            [-1, self.max_num_proposals, self.num_classes + 1]
        )
        refined_decoded_boxes_batch = self._batch_decode_boxes(
            refined_box_encodings_batch, proposal_boxes)
        class_predictions_with_background_batch = (
            self._second_stage_score_conversion_fn(
                class_predictions_with_background_batch))
        class_predictions_batch = tf.reshape(
            tf.slice(class_predictions_with_background_batch,
                     [0, 0, 1], [-1, -1, -1]),
            [-1, self.max_num_proposals, self.num_classes])
        clip_window = tf.to_float(
            tf.stack([0, 0, image_shape[1], image_shape[2]]))

        (nmsed_boxes, nmsed_scores, nmsed_classes, _, _,
         num_detections) = self._second_stage_nms_fn(
             refined_decoded_boxes_batch,  # TODO verify softmax doesn't break NMS
             class_predictions_batch,
             clip_window=clip_window,
             change_coordinate_frame=True,
             num_valid_boxes=num_proposals)

        detections = {'detection_boxes': nmsed_boxes,
                      'detection_scores': nmsed_scores,
                      'detection_classes': nmsed_classes,
                      'num_detections': tf.to_float(num_detections)}

        detections.update(self._predict_third_stage(
            rpn_features_to_crop,
            nmsed_boxes,
            nmsed_classes,
            image_shape,
            num_detections,
            mask_threshold))

        return detections

    def _predict_third_stage(self,
                             rpn_features_to_crop,
                             refined_boxes_normalized,
                             classes,
                             image_shape,
                             num_detections,
                             mask_threshold=.5):
        """Compute mask and motion branch on features extracted with refined
        boxes (evaluation only).
        Args:
          rpn_features_to_crop: A list of 4-D float32 tensors with shape
            [batch_size, height, width, depth] representing image features to crop
            using the refined boxes.
          refined_boxes_normalized: A [batch_size, max_detections, 4] float32 tensor
            containing the refined boxes after non-max suppression.
          classes: A [batch_size, max_detections] float32 tensor
            containing the class for boxes.
        Returns:
          A dictionary containing:
            `detection_masks`:
              (optional) [batch, max_detections, mask_height, mask_width]
            `detection_motions`:
              (optional) [batch, max_detections, num_motion_params]
        """
        detections = {}

        absolute_refined_boxes_reshaped = box_list_ops.to_absolute_coordinates(
            box_list.BoxList(tf.reshape(refined_boxes_normalized, [-1, 4])),
            image_shape[1], image_shape[2]).get()
        absolute_refined_boxes = tf.reshape(
            absolute_refined_boxes_reshaped,
            [-1, refined_boxes_normalized.shape[1].value, 4])

        flattened_refined_feature_maps = (
            self._compute_second_stage_input_feature_maps(
                rpn_features_to_crop,
                refined_boxes_normalized,
                absolute_refined_boxes))

        refined_box_classifier_features = (
            self._feature_extractor.extract_box_classifier_features(
                flattened_refined_feature_maps,
                scope=self.second_stage_feature_extractor_scope,
                reuse=True))
        refined_box_predictions = self._mask_rcnn_box_predictor.predict(
            refined_box_classifier_features,
            num_predictions_per_location=1,
            scope=self.second_stage_box_predictor_scope,
            reuse=True)

        classes_one_hot = tf.cast(
            tf.one_hot(tf.to_int32(classes), depth=self._num_classes),
            dtype=tf.bool)
        max_detections = tf.shape(classes)[1]

        if box_predictor.MASK_PREDICTIONS in refined_box_predictions:
            mask_predictions_per_class = tf.squeeze(
                refined_box_predictions[box_predictor.MASK_PREDICTIONS], axis=1)
            mask_height = mask_predictions_per_class.shape[2].value
            mask_width = mask_predictions_per_class.shape[3].value
            mask_predictions_per_class_flat = tf.reshape(
                mask_predictions_per_class, [-1, max_detections,
                                             self.num_classes, mask_height * mask_width])
            mask_predictions_flat = tf.boolean_mask(
                mask_predictions_per_class_flat, classes_one_hot)
            mask_predictions = tf.reshape(
                mask_predictions_flat, [-1, max_detections,
                                        mask_height, mask_width])
            detections['detection_masks'] = tf.to_float(
                tf.greater_equal(tf.sigmoid(mask_predictions), mask_threshold))

            # mask feature maps for motion stage
            #crop_size = tf.shape(refined_box_classifier_features)[1:3]
            # features_mask = tf.image.resize_area(
            #    tf.reshape(detections['detection_masks'],
            #               [-1, mask_height, mask_width, 1]),
            #    crop_size)
            # refined_masked_box_classifier_features = (
            #    refined_box_classifier_features * features_mask)

            # refined_box_predictions = self._mask_rcnn_box_predictor.predict(
            #  refined_masked_box_classifier_features,
            #  num_predictions_per_location=1,
            #  scope=self.second_stage_box_predictor_scope,
            #  reuse=True)

        if box_predictor.MOTION_PREDICTIONS in refined_box_predictions:
            motion_predictions_per_class = tf.squeeze(
                refined_box_predictions[box_predictor.MOTION_PREDICTIONS], axis=1)
            num_motion_params = motion_predictions_per_class.shape[2].value
            motion_predictions_per_class_reshaped = tf.reshape(
                motion_predictions_per_class,
                [-1, max_detections, self.num_classes, num_motion_params])
            motion_predictions_reshaped = tf.boolean_mask(
                motion_predictions_per_class_reshaped, classes_one_hot)
            motion_predictions = tf.reshape(
                motion_predictions_reshaped, [-1, max_detections, num_motion_params])
            detections['detection_motions'] = motion_predictions

        return detections

    def _batch_decode_boxes(self, box_encodings, anchor_boxes):
        """Decode tensor of refined box encodings.
        Args:
          refined_box_encodings: a 3-D tensor with shape
            [batch_size, max_num_proposals, num_classes, self._box_coder.code_size]
            representing predicted (final) refined box encodings.
          proposal_boxes: [batch_size, self.max_num_proposals, 4] representing
            decoded proposal bounding boxes.
        Returns:
          refined_box_predictions: a [batch_size, max_num_proposals, num_classes, 4]
            float tensor representing (padded) refined bounding box predictions
            (for each image in batch, proposal and class).
        """
        """Decodes box encodings with respect to the anchor boxes.
    Args:
      box_encodings: a 4-D tensor with shape
        [batch_size, num_anchors, num_classes, self._box_coder.code_size]
        representing box encodings.
      anchor_boxes: [batch_size, num_anchors, 4] representing
        decoded bounding boxes.
    Returns:
      decoded_boxes: a [batch_size, num_anchors, num_classes, 4]
        float tensor representing bounding box predictions
        (for each image in batch, proposal and class).
    """
        combined_shape = shape_utils.combined_static_and_dynamic_shape(
            box_encodings)
        num_classes = combined_shape[2]
        tiled_anchor_boxes = tf.tile(
            tf.expand_dims(anchor_boxes, 2), [1, 1, num_classes, 1])
        tiled_anchors_boxlist = box_list.BoxList(
            tf.reshape(tiled_anchor_boxes, [-1, 4]))
        decoded_boxes = self._box_coder.decode(
            tf.reshape(box_encodings, [-1, self._box_coder.code_size]),
            tiled_anchors_boxlist)
        return tf.reshape(decoded_boxes.get(),
                          tf.stack([combined_shape[0], combined_shape[1],
                                    num_classes, 4]))

    def loss(self, prediction_dict, scope=None):
        """Compute scalar loss tensors given prediction tensors.
        If first_stage_only=True, only RPN related losses are computed (i.e.,
        `rpn_localization_loss` and `rpn_objectness_loss`).  Otherwise all
        losses are computed.
        Args:
          prediction_dict: a dictionary holding prediction tensors (see the
            documentation for the predict method.  If first_stage_only=True, we
            expect prediction_dict to contain `rpn_box_encodings`,
            `rpn_objectness_predictions_with_background`, `rpn_features_to_crop`,
            `image_shape`, and `anchors` fields.  Otherwise we expect
            prediction_dict to additionally contain `refined_box_encodings`,
            `class_predictions_with_background`, `num_proposals`, and
            `proposal_boxes` fields.
          scope: Optional scope name.
        Returns:
          a dictionary mapping loss keys (`first_stage_localization_loss`,
            `first_stage_objectness_loss`, 'second_stage_localization_loss',
            'second_stage_classification_loss') to scalar tensors representing
            corresponding loss values.
        """
        with tf.name_scope(scope, 'Loss', prediction_dict.values()):
            (groundtruth_boxlists, groundtruth_classes_with_background_list,
             groundtruth_masks_list, groundtruth_motions_list
             ) = self._format_groundtruth_data(prediction_dict['image_shape'])
            loss_dict = self._loss_rpn(
                prediction_dict['rpn_box_encodings'],
                prediction_dict['rpn_objectness_predictions_with_background'],
                prediction_dict['anchors'],
                groundtruth_boxlists,
                groundtruth_classes_with_background_list)
            loss_dict.update(self._loss_global(
                groundtruth_masks_list,
                prediction_dict.get('camera_motion'),
                self._groundtruth_camera_motion_list))
            if not self._first_stage_only:
                loss_dict.update(
                    self._loss_box_classifier(
                        prediction_dict['image_shape'],
                        prediction_dict['refined_box_encodings'],
                        prediction_dict['class_predictions_with_background'],
                        prediction_dict['proposal_boxes'],
                        prediction_dict['num_proposals'],
                        groundtruth_boxlists,
                        groundtruth_classes_with_background_list,
                        prediction_dict.get('mask_predictions'),
                        groundtruth_masks_list,
                        prediction_dict.get('motion_predictions'),
                        groundtruth_motions_list,
                        prediction_dict.get('camera_motion'),
                        self._groundtruth_camera_motion_list))
        return loss_dict

    def _loss_global(self,
                     groundtruth_masks_list,
                     predicted_camera_motion,
                     groundtruth_camera_motion_list):
        loss_dict = {}
        if predicted_camera_motion is not None:
            if self._first_stage_camera_motion_loss_from_flow:
                gt_depth = tf.stack(self._groundtruth_depth_list, axis=0)
                gt_flow = tf.stack(self._groundtruth_flow_list, axis=0)
                gt_masks = tf.stack(groundtruth_masks_list, axis=0)
                camera_motion_losses = motion_util.flow_camera_motion_loss(
                    tf.to_float(gt_masks),
                    predicted_camera_motion, gt_depth, gt_flow,
                    self._camera_intrinsics)
            else:
                if groundtruth_camera_motion_list is None:
                    raise RuntimeError(
                        "No ground truth camera motion provided.")
                groundtruth_camera_motion = tf.stack(
                    groundtruth_camera_motion_list, axis=0)
                camera_motion_losses = motion_util.camera_motion_loss(
                    predicted_camera_motion,
                    groundtruth_camera_motion)
            camera_motion_loss = tf.reduce_mean(camera_motion_losses)
            loss_dict.update({
                'first_stage_camera_motion_loss':
                self._first_stage_camera_motion_loss_weight * camera_motion_loss})
        return loss_dict

    def _loss_rpn(self,
                  rpn_box_encodings,
                  rpn_objectness_predictions_with_background,
                  anchors,
                  groundtruth_boxlists,
                  groundtruth_classes_with_background_list):
        """Computes scalar RPN loss tensors.
        Uses self._proposal_target_assigner to obtain regression and classification
        targets for the first stage RPN, samples a "minibatch" of anchors to
        participate in the loss computation, and returns the RPN losses.
        Args:
          rpn_box_encodings: A 4-D float tensor of shape
            [batch_size, num_anchors, self._box_coder.code_size] containing
            predicted proposal box encodings.
          rpn_objectness_predictions_with_background: A 2-D float tensor of shape
            [batch_size, num_anchors, 2] containing objectness predictions
            (logits) for each of the anchors with 0 corresponding to background
            and 1 corresponding to object.
          anchors: A 2-D tensor of shape [num_anchors, 4] representing anchors
            for the first stage RPN.  Note that `num_anchors` can differ depending
            on whether the model is created in training or inference mode.
          groundtruth_boxlists: A list of BoxLists containing coordinates of the
            groundtruth boxes.
          groundtruth_classes_with_background_list: A list of 2-D one-hot
            (or k-hot) tensors of shape [num_boxes, num_classes+1] containing the
            class targets with the 0th index assumed to map to the background class.
        Returns:
          a dictionary mapping loss keys (`first_stage_localization_loss`,
            `first_stage_objectness_loss`) to scalar tensors representing
            corresponding loss values.
        """
        with tf.name_scope('RPNLoss'):
            (batch_cls_targets, batch_cls_weights, batch_reg_targets,
             batch_reg_weights, _) = target_assigner.batch_assign_targets(
                 self._proposal_target_assigner, box_list.BoxList(anchors),
                 groundtruth_boxlists, len(groundtruth_boxlists)*[None])
            batch_cls_targets = tf.squeeze(batch_cls_targets, axis=2)

            def _minibatch_subsample_fn(inputs):
                cls_targets, cls_weights = inputs
                return self._first_stage_sampler.subsample(
                    tf.cast(cls_weights, tf.bool),
                    self._first_stage_minibatch_size, tf.cast(cls_targets, tf.bool))
            batch_sampled_indices = tf.to_float(tf.map_fn(
                _minibatch_subsample_fn,
                [batch_cls_targets, batch_cls_weights],
                dtype=tf.bool,
                parallel_iterations=self._parallel_iterations,
                back_prop=True))

            # Normalize by number of examples in sampled minibatch
            normalizer = tf.reduce_sum(batch_sampled_indices, axis=1)
            batch_one_hot_targets = tf.one_hot(
                tf.to_int32(batch_cls_targets), depth=2)
            sampled_reg_indices = tf.multiply(batch_sampled_indices,
                                              batch_reg_weights)

            localization_losses = self._first_stage_localization_loss(
                rpn_box_encodings, batch_reg_targets, weights=sampled_reg_indices)
            objectness_losses = self._first_stage_objectness_loss(
                rpn_objectness_predictions_with_background,
                batch_one_hot_targets, weights=batch_sampled_indices)
            localization_loss = tf.reduce_mean(
                tf.reduce_sum(localization_losses, axis=1) / normalizer)
            objectness_loss = tf.reduce_mean(
                tf.reduce_sum(objectness_losses, axis=1) / normalizer)
            loss_dict = {
                'first_stage_localization_loss':
                self._first_stage_loc_loss_weight * localization_loss,
                'first_stage_objectness_loss':
                self._first_stage_obj_loss_weight * objectness_loss,
            }
        return loss_dict

    def _loss_box_classifier(self,
                             image_shape,
                             refined_box_encodings,
                             class_predictions_with_background,
                             proposal_boxes,
                             num_proposals,
                             groundtruth_boxlists,
                             groundtruth_classes_with_background_list,
                             mask_predictions=None,
                             groundtruth_masks_list=None,
                             motion_predictions=None,
                             groundtruth_motions_list=None,
                             predicted_camera_motion=None,
                             groundtruth_camera_motion_list=None):
        """Computes scalar box classifier loss tensors.
        Uses self._detector_target_assigner to obtain regression and classification
        targets for the second stage box classifier, optionally performs
        hard mining, and returns losses.  All losses are computed independently
        for each image and then averaged across the batch.
        This function assumes that the proposal boxes in the "padded" regions are
        actually zero (and thus should not be matched to).
        Args:
          image_shape: a 1-D tensor of shape [4] representing the input
            image shape.
          refined_box_encodings: a 3-D tensor with shape
            [total_num_proposals, num_classes, box_coder.code_size] representing
            predicted (final) refined box encodings.
          class_predictions_with_background: a 3-D tensor with shape
            [total_num_proposals, num_classes + 1] containing class
            predictions (logits) for each of the anchors.  Note that this tensor
            *includes* background class predictions (at class index 0).
          proposal_boxes: [batch_size, self.max_num_proposals, 4] representing
            decoded proposal bounding boxes.
          num_proposals: A Tensor of type `int32`. A 1-D tensor of shape [batch]
            representing the number of proposals predicted for each image in
            the batch.
          groundtruth_boxlists: a list of BoxLists containing coordinates of the
            groundtruth boxes.
          groundtruth_classes_with_background_list: a list of 2-D one-hot
            (or k-hot) tensors of shape [num_boxes, num_classes + 1] containing the
            class targets with the 0th index assumed to map to the background class.
          mask_predictions: (optional) a 4-D tensor with shape
            [total_num_proposals, num_classes, mask_height, mask_width]
            containing instance mask predictions (logits).
          groundtruth_masks_list: (optional) a list of 3-D tf.bool tensors of
            shape [num_boxes, height_in, width_in] containing instance
            masks with values in {0, 1}. Must be provided if mask_predictions is
            not None.
          motion_predictions: (optional) a 3-D tensor with shape
            [total_num_proposals, num_classes, num_motion_params]
            containing instance motion predictions.
          groundtruth_motions_list: (optional) a list of 2-D tf.float32 tensors of
            shape [num_boxes, num_gt_motion_params] containing instance
            motions. Must be provided if motion_predictions is
            not None.
          predicted_camera_motion: (optional) a 2-D tensor with shape
            [num_batch, num_camera_motion_params]
            containing instance motion predictions.
          groundtruth_camera_motion_list: (optional) a list of 2-D tf.float32
            tensors of shape [num_gt_camera_motion_params] containing camera
            motions. Must be provided if predicted_camera_motion is None
            and self._second_stage_motion_loss_flow is True.
        Returns:
          a dictionary mapping loss keys ('second_stage_localization_loss',
            'second_stage_classification_loss') to scalar tensors representing
            corresponding loss values.
        """
        with tf.name_scope('BoxClassifierLoss'):
            paddings_indicator = self._padded_batched_proposals_indicator(
                num_proposals, self.max_num_proposals)
            proposal_boxlists = [
                box_list.BoxList(proposal_boxes_single_image)
                for proposal_boxes_single_image in tf.unstack(proposal_boxes)]
            batch_size = len(proposal_boxlists)

            num_proposals_or_one = tf.to_float(tf.expand_dims(
                tf.maximum(num_proposals, tf.ones_like(num_proposals)), 1))
            normalizer = tf.tile(num_proposals_or_one,
                                 [1, self.max_num_proposals]) * batch_size

            (batch_cls_targets_with_background, batch_cls_weights, batch_reg_targets,
             batch_reg_weights, match_list) = target_assigner.batch_assign_targets(
                 self._detector_target_assigner, proposal_boxlists,
                 groundtruth_boxlists, groundtruth_classes_with_background_list)

            flat_cls_targets_with_background = tf.reshape(
                batch_cls_targets_with_background,
                [batch_size * self.max_num_proposals, -1])

            def _mask_predictions_by_class_targets(predictions_for_all_classes,
                                                   out_shape_last_dim):
                # We only predict refined location encodings for the non background
                # classes, but we now pad it to make it compatible with the class
                # predictions
                predictions_with_background = tf.pad(
                    predictions_for_all_classes, [[0, 0], [1, 0], [0, 0]])
                predictions_masked_by_class_targets = tf.boolean_mask(
                    predictions_with_background,
                    tf.greater(flat_cls_targets_with_background, 0))
                return tf.reshape(
                    predictions_masked_by_class_targets,
                    [batch_size, -1, out_shape_last_dim])

            reshaped_refined_box_encodings = (
                _mask_predictions_by_class_targets(refined_box_encodings, 4))

            second_stage_loc_losses = self._second_stage_localization_loss(
                reshaped_refined_box_encodings,
                batch_reg_targets, weights=batch_reg_weights) / normalizer
            second_stage_cls_losses = self._second_stage_classification_loss(
                class_predictions_with_background,
                batch_cls_targets_with_background,
                weights=batch_cls_weights) / normalizer
            second_stage_loc_loss = tf.reduce_sum(
                tf.boolean_mask(second_stage_loc_losses, paddings_indicator))
            second_stage_cls_loss = tf.reduce_sum(
                tf.boolean_mask(second_stage_cls_losses, paddings_indicator))

            if self._hard_example_miner:
                if mask_predictions is not None:
                    raise RuntimeError(
                        'Hard example miner not yet adapted to mask prediction.')
                (second_stage_loc_loss, second_stage_cls_loss
                 ) = self._unpad_proposals_and_apply_hard_mining(
                    proposal_boxlists, second_stage_loc_losses,
                    second_stage_cls_losses, num_proposals)

            loss_dict = {
                'second_stage_localization_loss':
                (self._second_stage_loc_loss_weight * second_stage_loc_loss),
                'second_stage_classification_loss':
                (self._second_stage_cls_loss_weight * second_stage_cls_loss)
            }

            if mask_predictions is not None:
                if groundtruth_masks_list is None:
                    raise RuntimeError('No groundtruth masks provided.')

                mask_height, mask_width = tf.unstack(
                    tf.shape(mask_predictions))[2:]

                (batch_mask_targets, batch_mask_weights
                 ) = target_assigner.batch_assign_mask_targets(
                    image_shape,
                    groundtruth_masks_list,
                    proposal_boxlists,
                    match_list,
                    mask_height,
                    mask_width)

                mask_dim = mask_height * mask_width
                mask_predictions_flat = tf.reshape(mask_predictions,
                                                   [batch_size * self.max_num_proposals, -1, mask_dim])

                reshaped_mask_predictions = _mask_predictions_by_class_targets(
                    mask_predictions_flat, mask_dim)

                second_stage_mask_losses = self._second_stage_mask_loss(
                    reshaped_mask_predictions,
                    batch_mask_targets, weights=batch_mask_weights
                ) / normalizer
                second_stage_mask_loss = tf.reduce_sum(
                    tf.boolean_mask(second_stage_mask_losses, paddings_indicator))

                loss_dict.update({
                    'second_stage_mask_loss':
                    (self._second_stage_mask_loss_weight * second_stage_mask_loss)
                })

            if motion_predictions is not None:
                # if image_shape[3] != 6: # TODO put somewhere else
                #  raise RuntimeError('Input image must be two concatenated RGB frames for motion prediction.')
                #
                num_motion_params = tf.unstack(
                    tf.shape(motion_predictions))[-1]
                reshaped_motion_predictions = _mask_predictions_by_class_targets(
                    motion_predictions, num_motion_params)

                if not self._second_stage_motion_loss_from_flow:
                    if groundtruth_motions_list is None:
                        raise RuntimeError('No groundtruth motions provided.')

                    (batch_motion_targets, batch_motion_weights
                     ) = target_assigner.batch_assign_motion_targets(
                        groundtruth_motions_list,
                        match_list)

                    second_stage_motion_losses = motion_util.motion_loss(
                        reshaped_motion_predictions,
                        batch_motion_targets,
                        batch_motion_weights) / normalizer
                else:
                    if self._groundtruth_depth_list is None:
                        raise RuntimeError('No groundtruth depth provided.')
                    if self._groundtruth_flow_list is None:
                        raise RuntimeError('No groundtruth flow provided.')
                    camera_motion = predicted_camera_motion
                    # if camera_motion is None: # TODO switch this logic, i.e. use camera gt if available?
                    if groundtruth_camera_motion_list is None:
                        raise RuntimeError('No groundtruth or predicted camera motion'
                                           'provided for flow-based motion supervision.')
                    camera_motion = tf.stack(
                        groundtruth_camera_motion_list, axis=0)
                    groundtruth_depth = tf.stack(
                        self._groundtruth_depth_list, axis=0)
                    groundtruth_flow = tf.stack(
                        self._groundtruth_flow_list, axis=0)

                    masks = tf.reshape(
                        batch_mask_targets,
                        [batch_size, self.max_num_proposals, mask_height, mask_width])
                    second_stage_motion_losses = motion_util.flow_motion_loss(
                        proposal_boxes,
                        masks,
                        reshaped_motion_predictions,
                        camera_motion,
                        groundtruth_depth,
                        groundtruth_flow,
                        self._camera_intrinsics,
                        batch_mask_weights
                    ) / normalizer

                second_stage_motion_loss = tf.reduce_sum(
                    tf.boolean_mask(second_stage_motion_losses, paddings_indicator))

                loss_dict.update({
                    'second_stage_motion_loss':
                    (self._second_stage_motion_loss_weight * second_stage_motion_loss)
                })

        return loss_dict

    def _padded_batched_proposals_indicator(self,
                                            num_proposals,
                                            max_num_proposals):
        """Creates indicator matrix of non-pad elements of padded batch proposals.
        Args:
          num_proposals: Tensor of type tf.int32 with shape [batch_size].
          max_num_proposals: Maximum number of proposals per image (integer).
        Returns:
          A Tensor of type tf.bool with shape [batch_size, max_num_proposals].
        """
        batch_size = tf.size(num_proposals)
        tiled_num_proposals = tf.tile(
            tf.expand_dims(num_proposals, 1), [1, max_num_proposals])
        tiled_proposal_index = tf.tile(
            tf.expand_dims(tf.range(max_num_proposals), 0), [batch_size, 1])
        return tf.greater(tiled_num_proposals, tiled_proposal_index)

    def _unpad_proposals_and_apply_hard_mining(self,
                                               proposal_boxlists,
                                               second_stage_loc_losses,
                                               second_stage_cls_losses,
                                               num_proposals):
        """Unpads proposals and applies hard mining.
        Args:
          proposal_boxlists: A list of `batch_size` BoxLists each representing
            `self.max_num_proposals` representing decoded proposal bounding boxes
            for each image.
          second_stage_loc_losses: A Tensor of type `float32`. A tensor of shape
            `[batch_size, self.max_num_proposals]` representing per-anchor
            second stage localization loss values.
          second_stage_cls_losses: A Tensor of type `float32`. A tensor of shape
            `[batch_size, self.max_num_proposals]` representing per-anchor
            second stage classification loss values.
          num_proposals: A Tensor of type `int32`. A 1-D tensor of shape [batch]
            representing the number of proposals predicted for each image in
            the batch.
        Returns:
          second_stage_loc_loss: A scalar float32 tensor representing the second
            stage localization loss.
          second_stage_cls_loss: A scalar float32 tensor representing the second
            stage classification loss.
        """
        for (proposal_boxlist, single_image_loc_loss, single_image_cls_loss,
             single_image_num_proposals) in zip(
                 proposal_boxlists,
                 tf.unstack(second_stage_loc_losses),
                 tf.unstack(second_stage_cls_losses),
                 tf.unstack(num_proposals)):
            proposal_boxlist = box_list.BoxList(
                tf.slice(proposal_boxlist.get(),
                         [0, 0], [single_image_num_proposals, -1]))
            single_image_loc_loss = tf.slice(single_image_loc_loss,
                                             [0], [single_image_num_proposals])
            single_image_cls_loss = tf.slice(single_image_cls_loss,
                                             [0], [single_image_num_proposals])
            return self._hard_example_miner(
                location_losses=tf.expand_dims(single_image_loc_loss, 0),
                cls_losses=tf.expand_dims(single_image_cls_loss, 0),
                decoded_boxlist_list=[proposal_boxlist])

    def restore_map(self, from_detection_checkpoint=True):
        """Returns a map of variables to load from a foreign checkpoint.
        See parent class for details.
        Args:
          from_detection_checkpoint: whether to restore from a full detection
            checkpoint (with compatible variable names) or to restore from a
            classification checkpoint for initialization prior to training.
        Returns:
          A dict mapping variable names (to load from a checkpoint) to variables in
          the model graph.
        """
        if not from_detection_checkpoint:
            return self._feature_extractor.restore_from_classification_checkpoint_fn(
                self.first_stage_feature_extractor_scope,
                self.second_stage_feature_extractor_scope)

        variables_to_restore = tf.global_variables()
        variables_to_restore.append(slim.get_or_create_global_step())
        # Only load feature extractor variables to be consistent with loading from
        # a classification checkpoint.
        feature_extractor_variables = tf.contrib.framework.filter_variables(
            variables_to_restore,
            include_patterns=[self.first_stage_feature_extractor_scope,
                              self.second_stage_feature_extractor_scope],
            exclude_patterns='conv1_adapted')
        return {var.op.name: var for var in feature_extractor_variables}
