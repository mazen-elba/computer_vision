# CNN Facial Landmark

Facial landmark detection based on convolution neural network.

The model is build with TensorFlow, the training code is provided so you can train your own model with your own datasets.

A sample gif extracted from video file showing the detection result.

![](doc/demo01.gif)

### Prerequisites

TensorFlow

```bash
# For CPU
python3 -m pip install tensorflow

# or, if you have a CUDA compatible GPU
python3 -m pip install tensorflow-gpu

```

## Train & evaluate

Before training started, make sure the following requirements are met.

- training and evaluation tf-record file.
- a directory to store the check point files.
- hyper parameters like training steps, batch size, number of epochs.

The following command shows how to train the model for 500 steps and evaluate it after training.

```bash
# From the repo's root directory
python3 landmark.py \
    --train_record train.record \
    --val_record validation.record \
    --model_dir train \
    --train_steps 500 \
    --batch_size 32
```

## Inference

If you are using TensorFlow Serving in the cloud, the exported SavedModel could be imported directly.

For local applications, [butterfly](https://github.com/yinguobing/butterfly) is a lightweight python module that is designed for frozen model and you can find a demo project demonstrating how to do inference with image and video/webcam.

## Acknowledgments

- The TensorFlow team for their comprehensive tutorial.
- The iBUG team for their public dataset.
