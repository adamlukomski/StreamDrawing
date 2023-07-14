# StreamDrawing

![white canvas with hello world](/images/image_000.png)

A tiny full screen drawing app - for streaming

Why? To be able to quickly draw mathematics, explain ideas, sketch on the fly

Requirements: tablet supported by PyQt5

Example: Wacom Intuos on Linux

Usage: buttons:
- f - toggles fullscreen
- q - quits
- Ctrl-s - save (creates a dir and dumps all .pngs - in background)
- a - add a new slide and jump to it
- page up / down - navigate between slides

Supports pen and eraser modes

PROBLEMS, BUGS, LIMITATIONS
- scenes the same as desktop resolution, not portable between resolutions for now
- no preview of brushes (eraser particularly)
- raster graphics - simple drawing on canvas
- save creates a directory in a current one, no feedback about success / failure

Author: Adam Lukomski, 2023

License: MIT
