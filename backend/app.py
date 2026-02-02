import json
from flask import Flask, request, jsonify
from flask_cors import CORS

from utils.helpers import password_hash, bgr_to_base64_png, bytes_to_bgr_image
from encryption.encryptor import encrypt_image, decrypt_image
from encryption.metrics import entropy_gray, npcr, uaci

app = Flask(__name__)

# ✅ CORS for deployed frontend
CORS(app, resources={r"/*": {"origins": "*"}})


@app.get("/")
def home():
    return "GraphCrypt Backend Running ✅"


@app.get("/health")
def health():
    return jsonify({"status": "Backend running ✅"})


@app.post("/encrypt")
def encrypt():
    try:
        if "image" not in request.files:
            return jsonify({"error": "Image missing"}), 400

        password = request.form.get("password", "").strip()
        if len(password) < 4:
            return jsonify({"error": "Password too short (min 4 chars)"}), 400

        img_file = request.files["image"]
        img = bytes_to_bgr_image(img_file.read())

        if img is None:
            return jsonify({"error": "Invalid image"}), 400

        hashed_key = password_hash(password)

        # ✅ Encrypt using your MST+DFS pipeline
        encrypted_img, key_json = encrypt_image(img, hashed_key)

        # ✅ Save verification hash in key.json
        key_json["password_hash"] = hashed_key

        metrics = {
            "entropy": round(entropy_gray(encrypted_img), 3),
            "npcr": round(npcr(img, encrypted_img), 2),
            "uaci": round(uaci(img, encrypted_img), 2),
        }

        enc_b64 = bgr_to_base64_png(encrypted_img)
        if enc_b64 is None:
            return jsonify({"error": "Encoding failed"}), 500

        return jsonify({
            "encrypted_image_base64": enc_b64,
            "key_json": key_json,
            "metrics": metrics
        })

    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500


@app.post("/decrypt")
def decrypt():
    try:
        if "image" not in request.files:
            return jsonify({"error": "Encrypted image missing"}), 400
        if "key" not in request.files:
            return jsonify({"error": "key.json missing"}), 400

        password = request.form.get("password", "").strip()
        if len(password) < 4:
            return jsonify({"error": "Password too short (min 4 chars)"}), 400

        enc_file = request.files["image"]
        enc_img = bytes_to_bgr_image(enc_file.read())

        if enc_img is None:
            return jsonify({"error": "Invalid encrypted image"}), 400

        # ✅ Parse key.json safely
        try:
            key_text = request.files["key"].read().decode("utf-8")
            key_json = json.loads(key_text)
        except Exception:
            return jsonify({"error": "Invalid key.json"}), 400

        hashed_key = password_hash(password)

        # ✅ verify password
        if hashed_key != key_json.get("password_hash"):
            return jsonify({"error": "Wrong password"}), 400

        # ✅ verify correct algorithm/version
        if key_json.get("algo") != "mst_dfs_channel_v1":
            return jsonify({"error": "Wrong key format"}), 400

        # ✅ Decrypt
        decrypted_img = decrypt_image(enc_img, hashed_key, key_json)

        dec_b64 = bgr_to_base64_png(decrypted_img)
        if dec_b64 is None:
            return jsonify({"error": "Encoding failed"}), 500

        return jsonify({"decrypted_image_base64": dec_b64})

    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500


if __name__ == "__main__":
    # ✅ Local run only
    app.run(debug=True, host="127.0.0.1", port=5000, use_reloader=False)
