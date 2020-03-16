import functools
import tensorflow as tf

from object_detection.core import data_decoder
from object_detection.core import standard_fields as fields

slim_example_decoder = tf.contrib.slim.tfexample_decoder


class TfExampleDecoder(data_decoder.DataDecoder):
    """Tensorflow Example proto decoder."""

    def __init__(self, load_detection_gt=True, load_motion_gt=True, load_XYZ=True):
        """Constructor sets keys_to_features and items_to_handlers."""
        self.keys_to_features = {
            'image/encoded': tf.FixedLenFeature((), tf.string, default_value=''),
            'image/format': tf.FixedLenFeature((), tf.string, default_value='jpeg'),
            'image/filename': tf.FixedLenFeature((), tf.string, default_value=''),
            'image/key/sha256': tf.FixedLenFeature((), tf.string, default_value=''),
            'image/source_id': tf.FixedLenFeature((), tf.string, default_value=''),
            'image/height': tf.FixedLenFeature((), tf.int64, 1),
            'image/width': tf.FixedLenFeature((), tf.int64, 1),
            # Motion R-CNN
            'next_image/encoded': tf.FixedLenFeature((), tf.string, default_value=''),
            'image/camera/intrinsics': tf.FixedLenFeature((3,), tf.float32),
            'image/depth': tf.VarLenFeature(tf.float32),
            'image/flow': tf.VarLenFeature(tf.float32)
        }
        self.items_to_handlers = {
            fields.InputDataFields.image: slim_example_decoder.Image(
                image_key='image/encoded', format_key='image/format', channels=3),
            fields.InputDataFields.source_id: (
                slim_example_decoder.Tensor('image/source_id')),
            fields.InputDataFields.key: (
                slim_example_decoder.Tensor('image/key/sha256')),
            fields.InputDataFields.filename: (
                slim_example_decoder.Tensor('image/filename')),
            # Motion R-CNN
            fields.InputDataFields.next_image: slim_example_decoder.Image(
                image_key='next_image/encoded', format_key='image/format', channels=3),
            fields.InputDataFields.camera_intrinsics: (
                slim_example_decoder.Tensor('image/camera/intrinsics')),
            fields.InputDataFields.groundtruth_depth: (
                slim_example_decoder.ItemHandlerCallback(
                    ['image/depth', 'image/height', 'image/width'],
                    self._decode_depth)),
            fields.InputDataFields.groundtruth_flow: (
                slim_example_decoder.ItemHandlerCallback(
                    ['image/flow', 'image/height', 'image/width'],
                    self._decode_flow))
        }
        if load_XYZ:
            self.keys_to_features.update({
                # Motion R-CNN
                'next_image/depth': tf.VarLenFeature(tf.float32)
            })
            self.items_to_handlers.update({
                fields.InputDataFields.groundtruth_next_depth: (
                    slim_example_decoder.ItemHandlerCallback(
                        ['next_image/depth', 'image/height', 'image/width'],
                        self._decode_next_depth))
            })

        if load_detection_gt:
            self.keys_to_features.update({
                # Object boxes and classes.
                'image/object/bbox/xmin': tf.VarLenFeature(tf.float32),
                'image/object/bbox/xmax': tf.VarLenFeature(tf.float32),
                'image/object/bbox/ymin': tf.VarLenFeature(tf.float32),
                'image/object/bbox/ymax': tf.VarLenFeature(tf.float32),
                'image/object/class/label': tf.VarLenFeature(tf.int64),
                'image/object/area': tf.VarLenFeature(tf.float32),
                'image/object/is_crowd': tf.VarLenFeature(tf.int64),
                'image/object/difficult': tf.VarLenFeature(tf.int64),
                # Instance masks and classes.
                'image/segmentation/object/index_0': tf.VarLenFeature(tf.int64),
                'image/segmentation/object/index_1': tf.VarLenFeature(tf.int64),
                'image/segmentation/object/index_2': tf.VarLenFeature(tf.int64),
                'image/segmentation/object/class': tf.VarLenFeature(tf.int64),
                'image/segmentation/object/count': tf.FixedLenFeature((), tf.int64, 1),
            })
            self.items_to_handlers.update({
                # Object boxes and classes.
                fields.InputDataFields.groundtruth_boxes: (
                    slim_example_decoder.BoundingBox(
                        ['ymin', 'xmin', 'ymax', 'xmax'], 'image/object/bbox/')),
                fields.InputDataFields.groundtruth_classes: (
                    slim_example_decoder.Tensor('image/object/class/label')),
                fields.InputDataFields.groundtruth_area: slim_example_decoder.Tensor(
                    'image/object/area'),
                fields.InputDataFields.groundtruth_is_crowd: (
                    slim_example_decoder.Tensor('image/object/is_crowd')),
                fields.InputDataFields.groundtruth_difficult: (
                    slim_example_decoder.Tensor('image/object/difficult')),
                # Instance masks and classes.
                fields.InputDataFields.groundtruth_instance_masks: (
                    slim_example_decoder.ItemHandlerCallback(
                        ['image/segmentation/object/index_0',
                         'image/segmentation/object/index_1',
                         'image/segmentation/object/index_2',
                         'image/segmentation/object/count',
                         'image/height', 'image/width'],
                        self._decode_instance_masks)),
                fields.InputDataFields.groundtruth_instance_classes: (
                    slim_example_decoder.Tensor('image/segmentation/object/class')),
            })

        if load_motion_gt:
            self.keys_to_features.update({
                # Motion R-CNN
                'image/camera/motion': tf.FixedLenFeature((8,), tf.float32)
            })
            self.items_to_handlers.update({
                # Motion R-CNN
                fields.InputDataFields.groundtruth_camera_motion: (
                    slim_example_decoder.Tensor('image/camera/motion')),
            })
            if load_detection_gt:
                self.keys_to_features.update({
                    # Motion R-CNN
                    'image/object/motion': tf.VarLenFeature(tf.float32)
                })
                self.items_to_handlers.update({
                    # Motion R-CNN
                    fields.InputDataFields.groundtruth_instance_motions: (
                        slim_example_decoder.ItemHandlerCallback(
                            ['image/object/motion', 'image/segmentation/object/count'],
                            self._decode_instance_motions))
                })

    def decode(self, tf_example_string_tensor):
        """Decodes serialized tensorflow example and returns a tensor dictionary.
        Args:
          tf_example_string_tensor: a string tensor holding a serialized tensorflow
            example proto.
        Returns:
          A dictionary of the following tensors.
          fields.InputDataFields.image - 3D uint8 tensor of shape [None, None, 3]
            containing image.
          fields.InputDataFields.source_id - string tensor containing original
            image id.
          fields.InputDataFields.key - string tensor with unique sha256 hash key.
          fields.InputDataFields.filename - string tensor with original dataset
            filename.
          fields.InputDataFields.groundtruth_boxes - 2D float32 tensor of shape
            [None, 4] containing box corners.
          fields.InputDataFields.groundtruth_classes - 1D int64 tensor of shape
            [None] containing classes for the boxes.
          fields.InputDataFields.groundtruth_area - 1D float32 tensor of shape
            [None] containing containing object mask area in pixel squared.
          fields.InputDataFields.groundtruth_is_crowd - 1D bool tensor of shape
            [None] indicating if the boxes enclose a crowd.
          fields.InputDataFields.groundtruth_difficult - 1D bool tensor of shape
            [None] indicating if the boxes represent `difficult` instances.
          fields.InputDataFields.groundtruth_instance_masks - 3D int64 tensor of
            shape [None, None, None] containing instance masks.
          fields.InputDataFields.groundtruth_instance_classes - 1D int64 tensor
            of shape [None] containing classes for the instance masks.
        """

        serialized_example = tf.reshape(tf_example_string_tensor, shape=[])
        decoder = slim_example_decoder.TFExampleDecoder(self.keys_to_features,
                                                        self.items_to_handlers)
        keys = decoder.list_items()
        tensors = decoder.decode(serialized_example, items=keys)
        tensor_dict = dict(zip(keys, tensors))
        is_crowd = fields.InputDataFields.groundtruth_is_crowd
        tensor_dict[is_crowd] = tf.cast(tensor_dict[is_crowd], dtype=tf.bool)
        tensor_dict[fields.InputDataFields.image].set_shape([None, None, 3])
        if fields.InputDataFields.next_image in tensor_dict:
            tensor_dict[fields.InputDataFields.next_image].set_shape([
                                                                     None, None, 3])
        return tensor_dict

    def _decode_instance_masks(self, keys_to_tensors):
        """Decode instance segmentation masks from sparse indices.
        The instance segmentation masks are reshaped to [num_instances, height,
        width] and cast to boolean type to save memory.
        Args:
          keys_to_tensors: a dictionary from keys to tensors.
        Returns:
          A 3-D boolean tensor of shape [num_instances, height, width].
        """
        height = keys_to_tensors['image/height']
        width = keys_to_tensors['image/width']
        num_instances = keys_to_tensors['image/segmentation/object/count']
        index_0 = keys_to_tensors['image/segmentation/object/index_0']
        index_1 = keys_to_tensors['image/segmentation/object/index_1']
        index_2 = keys_to_tensors['image/segmentation/object/index_2']

        if isinstance(index_0, tf.SparseTensor):
            index_0 = tf.sparse_tensor_to_dense(index_0)
        if isinstance(index_1, tf.SparseTensor):
            index_1 = tf.sparse_tensor_to_dense(index_1)
        if isinstance(index_2, tf.SparseTensor):
            index_2 = tf.sparse_tensor_to_dense(index_2)

        sparse_indices = tf.stack([index_0, index_1, index_2], axis=1)
        output_shape = tf.stack([num_instances, height, width])

        masks = tf.sparse_to_dense(sparse_indices=sparse_indices,
                                   output_shape=output_shape,
                                   sparse_values=1)
        return tf.cast(masks, tf.bool)

    def _decode_depth(self, keys_to_tensors):
        depth = keys_to_tensors['image/depth']
        if isinstance(depth, tf.SparseTensor):
            depth = tf.sparse_tensor_to_dense(depth)
        height = keys_to_tensors['image/height']
        width = keys_to_tensors['image/width']
        return tf.reshape(depth, tf.cast(tf.stack([height, width, 1], 0), tf.int32))

    def _decode_next_depth(self, keys_to_tensors):
        depth = keys_to_tensors['next_image/depth']
        if isinstance(depth, tf.SparseTensor):
            depth = tf.sparse_tensor_to_dense(depth)
        height = keys_to_tensors['image/height']
        width = keys_to_tensors['image/width']
        return tf.reshape(depth, tf.cast(tf.stack([height, width, 1], 0), tf.int32))

    def _decode_flow(self, keys_to_tensors):
        flow = keys_to_tensors['image/flow']
        if isinstance(flow, tf.SparseTensor):
            flow = tf.sparse_tensor_to_dense(flow)
        height = keys_to_tensors['image/height']
        width = keys_to_tensors['image/width']
        return tf.reshape(flow, tf.cast(tf.stack([height, width, 2], 0), tf.int32))

    def _decode_instance_motions(self, keys_to_tensors):
        motions = keys_to_tensors['image/object/motion']
        if isinstance(motions, tf.SparseTensor):
            motions = tf.sparse_tensor_to_dense(motions)
        num_instances = keys_to_tensors['image/segmentation/object/count']
        return tf.reshape(motions, tf.cast(tf.stack([num_instances, 11], 0), tf.int32))
