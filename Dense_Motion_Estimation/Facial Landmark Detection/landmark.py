"""
Convolutional Neural Network for facial landmarks detection.
"""

import argparse

import cv2
import numpy as np
import tensorflow as tf

from model import LandmarkModel

# add arguments parser to accept user specified arguments
parser = argparse.ArgumentParser()
parser.add_argument("--trainRecord", default="train.record", type=str,
                    help="Training record file")
parser.add_argument("--valRecord", default="validation.record", type=str,
                    help="validation record file")
parser.add_argument("--modelDir", default="train", type=str,
                    help="training model directory")
parser.add_argument("--exportDir", default=None, type=str,
                    help="directory to export the saved model")
parser.add_argument("--trainSteps", default=1000, type=int,
                    help="training steps")
parser.add_argument("--numEpochs", default=None, type=int,
                    help="epochs of training dataset")
parser.add_argument("--batchSize", default=16, type=int,
                    help="training batch size")
parser.add_argument("--rawInput", default=False, type=bool,
                    help="Use raw tensor as model input.")


# CAUTION: The image width, height and channels should be consist with your training data.
# Here they are set as 128 to be complied with the tutorial.
# Mismatching of the image size will cause error of mismatching tensor shapes.
IMG_WIDTH = 128
IMG_HEIGHT = 128
IMG_CHANNEL = 3


def cnnModelFx(features, labels, mode):
    """
    The model function for the network.
    """
    # construct the network
    model = LandmarkModel(outputSize=68*2)
    logits = model(features)

    # make prediction for PREDICATION mode
    predictions = logits
    if mode == tf.estimator.ModeKeys.PREDICT:
        return tf.estimator.EstimatorSpec(
            mode=mode,
            predictions=predictions,
            export_outputs={
                "predict": tf.estimator.export.PredictOutput(predictions)
            })

    # calculate loss using mean squared error
    loss = tf.losses.mean_squared_error(labels=labels, predictions=predictions)

    # create a tensor logging purposes
    tf.identity(loss, name="loss")
    tf.summary.scalar("loss", loss)

    # configure the train OP for TRAIN mode
    if mode == tf.estimator.ModeKeys.TRAIN:
        optimizer = tf.train.AdamOptimizer(learning_rate=0.001)

        trainOp = optimizer.minimize(
            loss=loss,
            global_step=tf.train.get_global_step())
    else:
        trainOp = None

    # create a metric
    rmseMetrics = tf.metrics.root_mean_squared_error(
        labels=labels,
        predictions=predictions)
    metrics = {"eval_mse": rmseMetrics}

    # a tensor for metric logging
    tf.identity(rmseMetrics[1], name="root_mean_squared_error")
    tf.summary.scalar("root_mean_squared_error", rmseMetrics[1])

    # generate a summary node for the images
    tf.summary.image("images", features, max_outputs=6)

    return tf.estimator.EstimatorSpec(
        mode=mode,
        predictions=predictions,
        loss=loss,
        train_op=trainOp,
        eval_metric_ops=metrics
    )


def _parseFunction(record):
    """
    Extract data from a `tf.Example` protocol buffer.
    """
    # defaults are not specified since both keys are required
    keysToFeatures = {
        "image/filename": tf.FixedLenFeature([], tf.string),
        "image/encoded": tf.FixedLenFeature([], tf.string),
        "label/marks": tf.FixedLenFeature([136], tf.float32),
    }
    parsedFeatures = tf.parse_single_example(record, keysToFeatures)

    # extract features from single example
    imageDecoded = tf.image.decode_image(parsedFeatures["image/encoded"])
    imageReshaped = tf.reshape(
        imageDecoded, [IMG_HEIGHT, IMG_WIDTH, IMG_CHANNEL])
    points = tf.cast(parsedFeatures["label/marks"], tf.float32)

    return imageReshaped, points


def inputFx(recordFile, batchSize, numEpochs=None, shuffle=True):
    """
    Input function required for TensorFlow Estimator.
    """
    dataset = tf.data.TFRecordDataset(recordFile)

    # use `Dataset.map()` to build a pair of a feature dictionary and a label tensor for each example.
    dataset = dataset.map(_parseFunction)
    if shuffle is True:
        dataset = dataset.shuffle(buffer_size=10000)
    dataset = dataset.batch(batchSize)
    dataset = dataset.repeat(numEpochs)

    # make dataset iterator
    iterator = dataset.make_one_shot_iterator()

    # return the feature and label
    image, label = iterator.get_next()
    return image, label


def servingInputReceiverFx():
    """An input function for TensorFlow Serving."""

    def _preprocessImage(imageBytes):
        """Preprocess a single raw image."""
        image = tf.image.decode_jpeg(imageBytes, channels=IMG_CHANNEL)
        image.set_shape((None, None, IMG_CHANNEL))
        image = tf.image.resize_images(image, [IMG_HEIGHT, IMG_WIDTH],
                                       method=tf.image.ResizeMethod.BILINEAR,
                                       align_corners=False)
        return image
    imageBytesList = tf.compat.v1.placeholder(
        shape=[None], dtype=tf.string,
        name="encoded_image_string_tensor")
    image = tf.map_fn(_preprocessImage, imageBytesList,
                      dtype=tf.float32, back_prop=False)

    return tf.estimator.export.TensorServingInputReceiver(
        features=image,
        receiver_tensors={"imageBytes": imageBytesList})


def tensorInputReceiverFx():
    """An input function accept raw tensors."""
    def _preprocessImage(imageTensor):
        """Preprocess a single raw image tensor."""
        image = tf.image.resize_images(imageTensor, [IMG_HEIGHT, IMG_WIDTH],
                                       method=tf.image.ResizeMethod.BILINEAR,
                                       align_corners=False)
        return image

    imageTensor = tf.compat.v1.placeholder(
        shape=[None, None, None, 3], dtype=tf.uint8,
        name="imageTensor")
    image = tf.map_fn(_preprocessImage, imageTensor,
                      dtype=tf.float32, back_prop=False)

    return tf.estimator.export.TensorServingInputReceiver(
        features=image,
        receiver_tensors={"image": imageTensor})


def main(unusedArgv):
    """Train, eval and export the model."""
    # parse the arguments
    args = parser.parse_args(unusedArgv[1:])

    # create the estimator
    estimator = tf.estimator.Estimator(
        model_fn=cnnModelFx, model_dir=args.modelDir)

    # train for N steps
    tf.logging.info("Starting to train.")
    estimator.train(
        input_fn=lambda: inputFx(recordFile=args.trainRecord,
                                 batchSize=args.batchSize,
                                 numEpochs=args.numEpochs,
                                 shuffle=True),
        steps=args.trainSteps)

    # do evaluation after training
    tf.logging.info("Starting to evaluate.")
    evaluation = estimator.evaluate(
        input_fn=lambda: inputFx(recordFile=args.valRecord,
                                 batchSize=1,
                                 numEpochs=1,
                                 shuffle=False))
    print(evaluation)

    # export trained model as SavedModel
    receiver_fn = tensorInputReceiverFx if args.rawInput else servingInputReceiverFx
    if args.exportDir is not None:
        estimator.export_savedmodel(args.exportDir, receiver_fn)


if __name__ == "__main__":
    tf.logging.set_verbosity(tf.logging.INFO)
    tf.app.run(main)
