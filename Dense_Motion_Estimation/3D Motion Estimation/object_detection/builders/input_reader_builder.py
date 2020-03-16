import tensorflow as tf

from object_detection.data_decoders import tf_example_decoder
from object_detection.protos import input_reader_pb2

parallel_reader = tf.contrib.slim.parallel_reader


def build(input_reader_config):
    """Builds a tensor dictionary based on the InputReader config.
    Args:
      input_reader_config: A input_reader_pb2.InputReader object.
    Returns:
      A tensor dict based on the input_reader_config.
    Raises:
      ValueError: On invalid input reader proto.
    """
    if not isinstance(input_reader_config, input_reader_pb2.InputReader):
        raise ValueError('input_reader_config not of type '
                         'input_reader_pb2.InputReader.')

    if input_reader_config.WhichOneof('input_reader') == 'tf_record_input_reader':
        config = input_reader_config.tf_record_input_reader
        _, string_tensor = parallel_reader.parallel_read(
            config.input_path,
            reader_class=tf.TFRecordReader,
            num_epochs=(input_reader_config.num_epochs
                        if input_reader_config.num_epochs else None),
            num_readers=input_reader_config.num_readers,
            shuffle=input_reader_config.shuffle,
            dtypes=[tf.string, tf.string],
            capacity=input_reader_config.queue_capacity,
            min_after_dequeue=input_reader_config.min_after_dequeue)

        return tf_example_decoder.TfExampleDecoder(
            input_reader_config.load_detection_groundtruth,
            input_reader_config.load_motion_groundtruth,
            input_reader_config.load_XYZ
        ).decode(string_tensor)

    raise ValueError('Unsupported input_reader_config.')