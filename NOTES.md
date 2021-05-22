# TODO LIST

## BUSINESS FEATURES

- use jupyter Qt console
  https://qtconsole.readthedocs.io/en/stable/index.html

- allow to edit operator to apply on DataSource

- display statistics: (min,max,avg) + (mean, std) + bands

- allow to define a filter to apply to the zoomed region
    - ressampling function (bilinear, cubic or average)
    - any kernel (sobel, conv2d, any neural network ...)

- bands manipulation
  - change order
  - view single band

## TECHNICAL FEATURES
- Bigger images (QuadTree, Tiling)

## DONE

- reactive stream (RX) ?
- refacto docking system
- auto-resizable grid of widgets
- display logs in interface
- background tasks (Threads / Processes)
- drag & drop