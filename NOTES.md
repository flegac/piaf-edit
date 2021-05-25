
# Libs Documentation

- [pyqtgraph](https://pyqtgraph.readthedocs.io/en/latest/)
- [rx operators](https://rxpy.readthedocs.io/en/latest/operators.html)


# TODO LIST

## FIXES
- clean up events (subject/observables)
- ViewManager should be closely related to the corresponding BrowserWidget
- in general : rethink how data/buttons/actions are coordinated


## BUSINESS FEATURES

- Easy plugin API

- custom resampling (bilinear, cubic, nearest, ...)
- Custom operators
 + dilate/erode
 - edge detection
 - more functions from opencv / sklearn
 - sobel
 - kernel (conv2d)
 - model onnx
 
- allow to edit operator parameters

- bands manipulation
  - change order
  - change RGB binding
  - view single band

- image editor !
  - color picker
  - brushes
  - polygon draw/fill

## TECHNICAL FEATURES
- Bigger images (QuadTree, Tiling)

## DONE

- reactive stream (RX) ?
- refacto docking system
- auto-resizable grid of widgets
- display logs in interface
- background tasks (Threads / Processes)
- drag & drop


- use jupyter Qt console
  https://qtconsole.readthedocs.io/en/stable/index.html
