# Changelog

- /!\ Bug: BrowserWidget : resizing from small to big size some times cause crash !

## Focus

- Pipeline should have a Dataclass with list of operators enums
  - reload current pipeline in ViewConfigPanel

- ViewManager should be closely related to the corresponding BrowserWidget

- BrowserWidget
  - TODO: configurable layout strategy (vertical vs horizontal first)
  - TODO: use Generic[T] & typehint widget/data

## 0.0.1-devxxx

- SourceBrowser : make sources draggable (to the OverviewPanel)
- reactive stream (RX) ?
- display logs in interface
- background tasks (Threads / Processes)
- drag & drop
- custom resampling (bilinear, cubic, nearest)

- use jupyter Qt console
  https://qtconsole.readthedocs.io/en/stable/index.html


# TODO LIST

- DataSource hierarchy
    + read(Window)
    + write(buffer,Window)

## FIXES
- clean up events (subject/observables)
- in general : rethink how data/buttons/actions are coordinated

## BUSINESS FEATURES

- Easy plugin API

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
- Bigger images / faster loading (QuadTree, Pyramids, Tiling ...)
