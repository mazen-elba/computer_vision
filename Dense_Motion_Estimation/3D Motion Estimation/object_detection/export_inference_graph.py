import tensorflow as tf
from google.protobuf import text_format
from object_detection import exporter
from object_detection.protos import pipeline_pb2

slim = tf.contrib.slim
flags = tf.app.flags

flags.DEFINE_string('input_type', 'image_tensor', 'Type of input node. Can be '
                    'one of [`image_tensor`, `encoded_image_string_tensor`, '
                    '`tf_example`]')
flags.DEFINE_string('pipeline_config_path', None,
                    'Path to a pipeline_pb2.TrainEvalPipelineConfig config '
                    'file.')
flags.DEFINE_string('trained_checkpoint_prefix', None,
                    'Path to trained checkpoint, typically of the form '
                    'path/to/model.ckpt')
flags.DEFINE_string('output_directory', None, 'Path to write outputs.')

FLAGS = flags.FLAGS


def main(_):
    assert FLAGS.pipeline_config_path, '`pipeline_config_path` is missing'
    assert FLAGS.trained_checkpoint_prefix, (
        '`trained_checkpoint_prefix` is missing')
    assert FLAGS.output_directory, '`output_directory` is missing'

    pipeline_config = pipeline_pb2.TrainEvalPipelineConfig()
    with tf.gfile.GFile(FLAGS.pipeline_config_path, 'r') as f:
        text_format.Merge(f.read(), pipeline_config)
    exporter.export_inference_graph(
        FLAGS.input_type, pipeline_config, FLAGS.trained_checkpoint_prefix,
        FLAGS.output_directory)


if __name__ == '__main__':
    tf.app.run()
