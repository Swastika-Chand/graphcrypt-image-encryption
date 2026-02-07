import json
from flask import Flask, request, jsonify
from flask_cors import CORS

from utils.helpers import password_hash, bgr_to_base64_png, bytes_to_bgr_image
from encryption.encryptor import encrypt_image, decrypt_image
from encryption.metrics import entropy_gray, npcr, uaci

app = Flask(__name__)

CORS(app)

@app.route("/")
def home():
    return "GraphCrypt Backend Running (Local) "


@app.route("/encrypt", methods=["POST"])
def encrypt():
    try:
        if "image" not in request.files:
            return jsonify({"error": "Image missing"}), 400

        password = request.form.get("password", "").strip()
        if len(password) < 4:
            return jsonify({"error": "Password too short"}), 400

        img = bytes_to_bgr_image(request.files["image"].read())
        if img is None:
            return jsonify({"error": "Invalid image"}), 400

        hashed_key = password_hash(password)

        encrypted_img, key_json = encrypt_image(img, hashed_key)
        key_json["password_hash"] = hashed_key

        metrics = {
            "entropy": round(entropy_gray(encrypted_img), 3),
            "npcr": round(npcr(img, encrypted_img), 2),
            "uaci": round(uaci(img, encrypted_img), 2),
        }

        enc_b64 = bgr_to_base64_png(encrypted_img)

        return jsonify({
            "encrypted_image_base64": enc_b64,
            "key_json": key_json,
            "metrics": metrics
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/decrypt", methods=["POST"])
def decrypt():
    try:
        if "image" not in request.files or "key" not in request.files:
            return jsonify({"error": "Missing inputs"}), 400

        password = request.form.get("password", "").strip()
        hashed_key = password_hash(password)

        enc_img = bytes_to_bgr_image(request.files["image"].read())
        key_json = json.loads(request.files["key"].read())

        if hashed_key != key_json.get("password_hash"):
            return jsonify({"error": "Wrong password"}), 400

        decrypted_img = decrypt_image(enc_img, hashed_key, key_json)
        dec_b64 = bgr_to_base64_png(decrypted_img)

        return jsonify({"decrypted_image_base64": dec_b64})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
