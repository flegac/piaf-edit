import cv2
import imutils
import numpy as np
from skimage import exposure

from piafedit.model.libs.operator import Buffer


def edge_detection(buffer: Buffer) -> Buffer:
    # data = cv2.cvtColor(data, cv2.COLOR_BGR2GRAY)
    # data = cv2.bilateralFilter(data, 11, 17, 17)
    edged = cv2.Canny(buffer, 0, 255)
    return np.dstack((edged, edged, edged))


def show_contours(buffer: Buffer) -> Buffer:
    buffer = buffer.copy()
    # gray = cv2.cvtColor(data, cv2.COLOR_BGR2GRAY)
    # gray = cv2.bilateralFilter(gray, 11, 17, 17)
    edged = cv2.Canny(buffer, 0, 255)

    cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:]
    for c in cnts:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.015 * peri, True)
        cv2.drawContours(buffer, [approx], -1, color=(0, 255, 0), thickness=1)
    return buffer


def normalize(buffer: Buffer) -> Buffer:
    buffer -= buffer.min()
    buffer = buffer / max(1, buffer.max())
    return buffer


def erode(buffer: Buffer) -> Buffer:
    kernel = np.ones((5, 5), np.uint8)
    return cv2.erode(buffer, kernel, iterations=1)


def dilate(buffer: Buffer) -> Buffer:
    kernel = np.ones((5, 5), np.uint8)
    return cv2.dilate(buffer, kernel, iterations=1)


def contrast_stretching(buffer: Buffer) -> Buffer:
    p2, p98 = np.percentile(buffer, (1, 99))
    return exposure.rescale_intensity(buffer, in_range=(p2, p98))
