# Image Resizer

Program resizes images by scale or width/height

# Quickstart

Requires __Pillow__ for image manipulation:

```bash
$ pip install -r requirements.txt
```

Available arguments:
* `-W` or `--width` - new width
* `-H` or `--height` - new height
* `-S` or `--scale` - scale image according to this number
* `-O` or `--output` - output image file path

Example of script launch on Linux, Python 3.5:

```bash
$ python image_resize.py <path to input image> --scale 0.5 --output <path to output image>
```

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
