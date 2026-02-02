import numpy as np
import cv2


def entropy_gray(img_bgr):
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    hist = cv2.calcHist([gray], [0], None, [256], [0, 256]).ravel()
    p = hist / np.sum(hist)
    p = p[p > 0]
    return float(-np.sum(p * np.log2(p)))


def npcr(original_bgr, encrypted_bgr):
    diff = (original_bgr != encrypted_bgr).astype(np.uint8)
    return float(np.mean(diff) * 100)


def uaci(original_bgr, encrypted_bgr):
    o = original_bgr.astype(np.float32)
    e = encrypted_bgr.astype(np.float32)
    return float(np.mean(np.abs(o - e)) / 255.0 * 100)
