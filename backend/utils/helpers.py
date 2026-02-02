import base64
import hashlib
import numpy as np
import cv2


def password_hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def get_seed_from_hash(hashed_key: str) -> int:
    # use first 8 hex chars -> 32-bit integer
    return int(hashed_key[:8], 16)


def bgr_to_base64_png(img_bgr):
    ok, buffer = cv2.imencode(".png", img_bgr)
    if not ok:
        return None
    return base64.b64encode(buffer).decode("utf-8")


def bytes_to_bgr_image(file_bytes: bytes):
    arr = np.frombuffer(file_bytes, np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    return img
