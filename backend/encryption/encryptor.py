import random
import numpy as np
import cv2

from utils.helpers import get_seed_from_hash
from encryption.graph_utils import kruskal_mst, dfs_order


def encrypt_channel(channel, hashed_key):
    mst_adj, rows, cols = kruskal_mst(channel)
    size = rows * cols

    seed = get_seed_from_hash(hashed_key)
    random.seed(seed)
    np.random.seed(seed)

    start_node = random.randint(0, size - 1)
    order = dfs_order(mst_adj, start_node, size)

    flat = channel.flatten()
    values = flat[order]

    perm = np.random.permutation(len(values))
    shuffled = values[perm]

    encrypted = np.zeros(size, dtype=np.uint8)
    for idx, val in zip(order, shuffled):
        encrypted[idx] = val

    return encrypted.reshape(rows, cols), order, perm, start_node, rows, cols


def decrypt_channel(enc_channel, order, perm, hashed_key, start_node, rows, cols):
    size = rows * cols
    seed = get_seed_from_hash(hashed_key)

    random.seed(seed)
    np.random.seed(seed)

    inverse_perm = np.zeros_like(perm)
    inverse_perm[perm] = np.arange(len(perm))

    flat_enc = enc_channel.flatten()
    shuffled = np.array([flat_enc[i] for i in order])

    restored = shuffled[inverse_perm]

    decrypted = np.zeros(size, dtype=np.uint8)
    for idx, val in zip(order, restored):
        decrypted[idx] = val

    return decrypted.reshape(rows, cols)


def encrypt_image(img_bgr, hashed_key):
    B, G, R = cv2.split(img_bgr)

    R_enc, R_order, R_perm, R_start, rows, cols = encrypt_channel(R, hashed_key)
    G_enc, G_order, G_perm, G_start, _, _ = encrypt_channel(G, hashed_key)
    B_enc, B_order, B_perm, B_start, _, _ = encrypt_channel(B, hashed_key)

    encrypted_img = cv2.merge([B_enc, G_enc, R_enc])

    key_json = {
        "algo": "mst_dfs_channel_v1",
        "rows": rows,
        "cols": cols,
        "R": {"order": R_order, "perm": R_perm.tolist(), "start": R_start},
        "G": {"order": G_order, "perm": G_perm.tolist(), "start": G_start},
        "B": {"order": B_order, "perm": B_perm.tolist(), "start": B_start},
    }

    return encrypted_img, key_json


def decrypt_image(enc_img_bgr, hashed_key, key_json):
    rows = key_json["rows"]
    cols = key_json["cols"]

    B_enc, G_enc, R_enc = cv2.split(enc_img_bgr)

    R_dec = decrypt_channel(
        R_enc,
        key_json["R"]["order"],
        np.array(key_json["R"]["perm"]),
        hashed_key,
        key_json["R"]["start"],
        rows, cols
    )

    G_dec = decrypt_channel(
        G_enc,
        key_json["G"]["order"],
        np.array(key_json["G"]["perm"]),
        hashed_key,
        key_json["G"]["start"],
        rows, cols
    )

    B_dec = decrypt_channel(
        B_enc,
        key_json["B"]["order"],
        np.array(key_json["B"]["perm"]),
        hashed_key,
        key_json["B"]["start"],
        rows, cols
    )

    decrypted_img = cv2.merge([B_dec, G_dec, R_dec])
    return decrypted_img
