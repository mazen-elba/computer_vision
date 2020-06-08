import tensorflow as tf


class LandmarkModel(object):
    def __init__(self, outputSize):
        self.outputSize = outputSize

    def __call__(self, inputTensor):
        # |== Layer 0: input layer ==|

        # input feature x should be of shape (batch_size, image_width, image_height, color_channels)
        # As we will directly using the decoded image tensor of data type int8, a convertion should be performed
        inputs = tf.cast(inputTensor, tf.float32)

        # |== Layer 1 ==|

        with tf.variable_scope("layer1"):
            # convolutional layer
            # computes 32 features using a 3x3 filter with ReLU activation
            conv1 = tf.layers.conv2d(
                inputs=inputs,
                filters=32,
                kernel_size=[3, 3],
                strides=(1, 1),
                padding="valid",
                activation=tf.nn.relu)

            # pooling layer
            # first max pooling layer with a 2x2 filter and stride of 2
            pool1 = tf.layers.max_pooling2d(
                inputs=conv1,
                pool_size=[2, 2],
                strides=(2, 2),
                padding="valid")

        # |== Layer 2 ==|

        with tf.variable_scope("layer2"):
            # convolutional layer
            # computes 64 features using a 3x3 filter with ReLU activation
            conv2 = tf.layers.conv2d(
                inputs=pool1,
                filters=64,
                kernel_size=[3, 3],
                strides=(1, 1),
                padding="valid",
                activation=tf.nn.relu)

            # convolutional layer
            # computes 64 features using a 3x3 filter with ReLU activation
            conv3 = tf.layers.conv2d(
                inputs=conv2,
                filters=64,
                kernel_size=[3, 3],
                strides=(1, 1),
                padding="valid",
                activation=tf.nn.relu)

            # pooling layer
            # second max pooling layer with a 2x2 filter and stride of 2
            pool2 = tf.layers.max_pooling2d(
                inputs=conv3,
                pool_size=[2, 2],
                strides=(2, 2),
                padding="valid")

        # |== Layer 3 ==|

        with tf.variable_scope("layer3"):
            # convolutional layer
            # computes 64 features using a 3x3 filter with ReLU activation
            conv4 = tf.layers.conv2d(
                inputs=pool2,
                filters=64,
                kernel_size=[3, 3],
                strides=(1, 1),
                padding="valid",
                activation=tf.nn.relu)

            # convolutional layer
            # computes 64 features using a 3x3 filter with ReLU activation
            conv5 = tf.layers.conv2d(
                inputs=conv4,
                filters=64,
                kernel_size=[3, 3],
                strides=(1, 1),
                padding="valid",
                activation=tf.nn.relu)

            # pooling layer
            # third max pooling layer with a 2x2 filter and stride of 2
            pool3 = tf.layers.max_pooling2d(
                inputs=conv5,
                pool_size=[2, 2],
                strides=(2, 2),
                padding="valid")

        # |== Layer 4 ==|

        with tf.variable_scope("layer4"):
            # convolutional layer
            # computes 128 features using a 3x3 filter with ReLU activation
            conv6 = tf.layers.conv2d(
                inputs=pool3,
                filters=128,
                kernel_size=[3, 3],
                strides=(1, 1),
                padding="valid",
                activation=tf.nn.relu)

            # convolutional layer
            # computes 128 features using a 3x3 filter with ReLU activation
            conv7 = tf.layers.conv2d(
                inputs=conv6,
                filters=128,
                kernel_size=[3, 3],
                strides=(1, 1),
                padding="valid",
                activation=tf.nn.relu)

            # pooling layer
            # fourth max pooling layer with a 2x2 filter and stride of 2
            pool4 = tf.layers.max_pooling2d(
                inputs=conv7,
                pool_size=[2, 2],
                strides=(1, 1),
                padding="valid")

        # |== Layer 5 ==|

        with tf.variable_scope("layer5"):
            # convolutional layer
            conv8 = tf.layers.conv2d(
                inputs=pool4,
                filters=256,
                kernel_size=[3, 3],
                strides=(1, 1),
                padding="valid",
                activation=tf.nn.relu)

        # |== Layer 6 ==|

        with tf.variable_scope("layer6"):
            # flatten tensor into a batch of vectors
            flatten = tf.layers.flatten(inputs=conv8)

            # dense layer 1, a fully connected layer.
            dense1 = tf.layers.dense(
                inputs=flatten,
                units=1024,
                activation=tf.nn.relu,
                use_bias=True)

            # dense layer 2, also known as the output layer
            logits = tf.layers.dense(
                inputs=dense1,
                units=self.outputSize,
                activation=None,
                use_bias=True,
                name="logits")
            logits = tf.identity(logits, "final_dense")

        return logits
