from abc import ABCMeta
from abc import abstractmethod

import tensorflow as tf

from object_detection.utils import ops


class MinibatchSampler(object):
    """Abstract base class for subsampling minibatches."""
    __metaclass__ = ABCMeta

    def __init__(self):
        """Constructs a minibatch sampler."""
        pass

    @abstractmethod
    def subsample(self, indicator, batch_size, **params):
        """Returns subsample of entries in indicator.
        Args:
          indicator: boolean tensor of shape [N] whose True entries can be sampled.
          batch_size: desired batch size.
          **params: additional keyword arguments for specific implementations of
              the MinibatchSampler.
        Returns:
          sample_indicator: boolean tensor of shape [N] whose True entries have been
          sampled. If sum(indicator) >= batch_size, sum(is_sampled) = batch_size
        """
        pass

    @staticmethod
    def subsample_indicator(indicator, num_samples):
        """Subsample indicator vector.
        Given a boolean indicator vector with M elements set to `True`, the function
        assigns all but `num_samples` of these previously `True` elements to
        `False`. If `num_samples` is greater than M, the original indicator vector
        is returned.
        Args:
          indicator: a 1-dimensional boolean tensor indicating which elements
            are allowed to be sampled and which are not.
          num_samples: int32 scalar tensor
        Returns:
          a boolean tensor with the same shape as input (indicator) tensor
        """
        indices = tf.where(indicator)
        indices = tf.random_shuffle(indices)
        indices = tf.reshape(indices, [-1])

        num_samples = tf.minimum(tf.size(indices), num_samples)
        selected_indices = tf.slice(indices, [0], tf.reshape(num_samples, [1]))

        selected_indicator = ops.indices_to_dense_vector(selected_indices,
                                                         tf.shape(indicator)[0])

        return tf.equal(selected_indicator, 1)
