import tensorflow as tf

from object_detection.core import minibatch_sampler


class BalancedPositiveNegativeSampler(minibatch_sampler.MinibatchSampler):
    """Subsamples minibatches to a desired balance of positives and negatives."""

    def __init__(self, positive_fraction=0.5):
        """Constructs a minibatch sampler.
        Args:
          positive_fraction: desired fraction of positive examples (scalar in [0,1])
        Raises:
          ValueError: if positive_fraction < 0, or positive_fraction > 1
        """
        if positive_fraction < 0 or positive_fraction > 1:
            raise ValueError('positive_fraction should be in range [0,1]. '
                             'Received: %s.' % positive_fraction)
        self._positive_fraction = positive_fraction

    def subsample(self, indicator, batch_size, labels):
        """Returns subsampled minibatch.
        Args:
          indicator: boolean tensor of shape [N] whose True entries can be sampled.
          batch_size: desired batch size.
          labels: boolean tensor of shape [N] denoting positive(=True) and negative
              (=False) examples.
        Returns:
          is_sampled: boolean tensor of shape [N], True for entries which are
              sampled.
        Raises:
          ValueError: if labels and indicator are not 1D boolean tensors.
        """
        if len(indicator.get_shape().as_list()) != 1:
            raise ValueError('indicator must be 1 dimensional, got a tensor of '
                             'shape %s' % indicator.get_shape())
        if len(labels.get_shape().as_list()) != 1:
            raise ValueError('labels must be 1 dimensional, got a tensor of '
                             'shape %s' % labels.get_shape())
        if labels.dtype != tf.bool:
            raise ValueError('labels should be of type bool. Received: %s' %
                             labels.dtype)
        if indicator.dtype != tf.bool:
            raise ValueError('indicator should be of type bool. Received: %s' %
                             indicator.dtype)

        # Only sample from indicated samples
        negative_idx = tf.logical_not(labels)
        positive_idx = tf.logical_and(labels, indicator)
        negative_idx = tf.logical_and(negative_idx, indicator)

        # Sample positive and negative samples separately
        max_num_pos = int(self._positive_fraction * batch_size)
        sampled_pos_idx = self.subsample_indicator(positive_idx, max_num_pos)
        max_num_neg = batch_size - \
            tf.reduce_sum(tf.cast(sampled_pos_idx, tf.int32))
        sampled_neg_idx = self.subsample_indicator(negative_idx, max_num_neg)

        sampled_idx = tf.logical_or(sampled_pos_idx, sampled_neg_idx)
        return sampled_idx
