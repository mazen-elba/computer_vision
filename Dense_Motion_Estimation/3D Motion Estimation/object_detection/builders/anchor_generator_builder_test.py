import tensorflow as tf

from google.protobuf import text_format
from object_detection.anchor_generators import grid_anchor_generator
from object_detection.anchor_generators import multiple_grid_anchor_generator
from object_detection.builders import anchor_generator_builder
from object_detection.protos import anchor_generator_pb2


class AnchorGeneratorBuilderTest(tf.test.TestCase):

    def assert_almost_list_equal(self, expected_list, actual_list, delta=None):
        self.assertEqual(len(expected_list), len(actual_list))
        for expected_item, actual_item in zip(expected_list, actual_list):
            self.assertAlmostEqual(expected_item, actual_item, delta=delta)

    def test_build_grid_anchor_generator_with_defaults(self):
        anchor_generator_text_proto = """
      grid_anchor_generator {
      }
     """
        anchor_generator_proto = anchor_generator_pb2.AnchorGenerator()
        text_format.Merge(anchor_generator_text_proto, anchor_generator_proto)
        anchor_generator_object = anchor_generator_builder.build(
            anchor_generator_proto)
        self.assertTrue(isinstance(anchor_generator_object,
                                   grid_anchor_generator.GridAnchorGenerator))
        self.assertListEqual(anchor_generator_object._scales, [])
        self.assertListEqual(anchor_generator_object._aspect_ratios, [])
        with self.test_session() as sess:
            base_anchor_size, anchor_offset, anchor_stride = sess.run(
                [anchor_generator_object._base_anchor_size,
                 anchor_generator_object._anchor_offset,
                 anchor_generator_object._anchor_stride])
        self.assertAllEqual(anchor_offset, [0, 0])
        self.assertAllEqual(anchor_stride, [16, 16])
        self.assertAllEqual(base_anchor_size, [256, 256])

    def test_build_grid_anchor_generator_with_non_default_parameters(self):
        anchor_generator_text_proto = """
      grid_anchor_generator {
        height: 128
        width: 512
        height_stride: 10
        width_stride: 20
        height_offset: 30
        width_offset: 40
        scales: [0.4, 2.2]
        aspect_ratios: [0.3, 4.5]
      }
     """
        anchor_generator_proto = anchor_generator_pb2.AnchorGenerator()
        text_format.Merge(anchor_generator_text_proto, anchor_generator_proto)
        anchor_generator_object = anchor_generator_builder.build(
            anchor_generator_proto)
        self.assertTrue(isinstance(anchor_generator_object,
                                   grid_anchor_generator.GridAnchorGenerator))
        self.assert_almost_list_equal(anchor_generator_object._scales,
                                      [0.4, 2.2])
        self.assert_almost_list_equal(anchor_generator_object._aspect_ratios,
                                      [0.3, 4.5])
        with self.test_session() as sess:
            base_anchor_size, anchor_offset, anchor_stride = sess.run(
                [anchor_generator_object._base_anchor_size,
                 anchor_generator_object._anchor_offset,
                 anchor_generator_object._anchor_stride])
        self.assertAllEqual(anchor_offset, [30, 40])
        self.assertAllEqual(anchor_stride, [10, 20])
        self.assertAllEqual(base_anchor_size, [128, 512])

    def test_raise_value_error_on_empty_anchor_genertor(self):
        anchor_generator_text_proto = """
    """
        anchor_generator_proto = anchor_generator_pb2.AnchorGenerator()
        text_format.Merge(anchor_generator_text_proto, anchor_generator_proto)
        with self.assertRaises(ValueError):
            anchor_generator_builder.build(anchor_generator_proto)


if __name__ == '__main__':
    tf.test.main()
