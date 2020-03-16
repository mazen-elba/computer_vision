from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf

from nets import nets_factory

slim = tf.contrib.slim


class NetworksTest(tf.test.TestCase):

    def testGetNetworkFn(self):
        batch_size = 5
        num_classes = 1000
        for net in nets_factory.networks_map:
            with self.test_session():
                net_fn = nets_factory.get_network_fn(net, num_classes)
                # Most networks use 224 as their default_image_size
                image_size = getattr(net_fn, 'default_image_size', 224)
                inputs = tf.random_uniform(
                    (batch_size, image_size, image_size, 3))
                logits, end_points = net_fn(inputs)
                self.assertTrue(isinstance(logits, tf.Tensor))
                self.assertTrue(isinstance(end_points, dict))
                self.assertEqual(logits.get_shape().as_list()[0], batch_size)
                self.assertEqual(logits.get_shape().as_list()[-1], num_classes)

    def testGetNetworkFnArgScope(self):
        batch_size = 5
        num_classes = 10
        net = 'cifarnet'
        with self.test_session(use_gpu=True):
            net_fn = nets_factory.get_network_fn(net, num_classes)
            image_size = getattr(net_fn, 'default_image_size', 224)
            with slim.arg_scope([slim.model_variable, slim.variable],
                                device='/CPU:0'):
                inputs = tf.random_uniform(
                    (batch_size, image_size, image_size, 3))
                net_fn(inputs)
            weights = tf.get_collection(
                tf.GraphKeys.GLOBAL_VARIABLES, 'CifarNet/conv1')[0]
            self.assertDeviceEqual('/CPU:0', weights.device)


if __name__ == '__main__':
    tf.test.main()
