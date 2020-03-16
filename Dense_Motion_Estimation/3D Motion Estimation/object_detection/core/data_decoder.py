from abc import ABCMeta
from abc import abstractmethod


class DataDecoder(object):
    """Interface for data decoders."""
    __metaclass__ = ABCMeta

    @abstractmethod
    def decode(self, data):
        """Return a single image and associated labels.
        Args:
          data: a string tensor holding a serialized protocol buffer corresponding
            to data for a single image.
        Returns:
          tensor_dict: a dictionary containing tensors. Possible keys are defined in
              reader.Fields.
        """
        pass
