const API_BASE = "http://127.0.0.1:5000";

// TABS 
const encryptTab = document.getElementById("encryptTab");
const decryptTab = document.getElementById("decryptTab");

const encryptSection = document.getElementById("encryptSection");
const decryptSection = document.getElementById("decryptSection");

encryptTab.addEventListener("click", () => {
  encryptTab.classList.add("active");
  decryptTab.classList.remove("active");
  encryptSection.classList.remove("hidden");
  decryptSection.classList.add("hidden");
});

decryptTab.addEventListener("click", () => {
  decryptTab.classList.add("active");
  encryptTab.classList.remove("active");
  decryptSection.classList.remove("hidden");
  encryptSection.classList.add("hidden");
});

// HELPERS 
function showPreview(inputEl, imgEl, emptyEl) {
  const file = inputEl.files[0];
  if (!file) return;
  const url = URL.createObjectURL(file);
  imgEl.src = url;
  imgEl.style.display = "block";
  emptyEl.style.display = "none";
}

function downloadTextFile(filename, text) {
  const blob = new Blob([text], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
}

function startProgress(progressId) {
  const bar = document.getElementById(progressId);
  bar.style.width = "0%";
  let p = 0;
  const timer = setInterval(() => {
    p += 8;
    if (p > 90) p = 90;
    bar.style.width = p + "%";
  }, 140);
  return timer;
}

// CUSTOM FILE BUTTONS 
const encImage = document.getElementById("encImage");
const encPickBtn = document.getElementById("encPickBtn");
const encFileName = document.getElementById("encFileName");

encPickBtn.addEventListener("click", () => encImage.click());
encImage.addEventListener("change", () => {
  encFileName.textContent = encImage.files[0] ? encImage.files[0].name : "No file chosen";
});

const decImage = document.getElementById("decImage");
const decPickBtn = document.getElementById("decPickBtn");
const decImageName = document.getElementById("decImageName");

decPickBtn.addEventListener("click", () => decImage.click());
decImage.addEventListener("change", () => {
  decImageName.textContent = decImage.files[0] ? decImage.files[0].name : "No file chosen";
});

const decKey = document.getElementById("decKey");
const decPickKeyBtn = document.getElementById("decPickKeyBtn");
const decKeyName = document.getElementById("decKeyName");

decPickKeyBtn.addEventListener("click", () => decKey.click());
decKey.addEventListener("change", () => {
  decKeyName.textContent = decKey.files[0] ? decKey.files[0].name : "No file chosen";
});

//PREVIEWS 
const encPreview = document.getElementById("encPreview");
const encPreviewEmpty = document.getElementById("encPreviewEmpty");

encImage.addEventListener("change", () => {
  showPreview(encImage, encPreview, encPreviewEmpty);
});

const decPreview = document.getElementById("decPreview");
const decPreviewEmpty = document.getElementById("decPreviewEmpty");

decImage.addEventListener("change", () => {
  showPreview(decImage, decPreview, decPreviewEmpty);
});

// ENCRYPT API 
const encryptBtn = document.getElementById("encryptBtn");
const encMsg = document.getElementById("encMsg");
const encLoader = document.getElementById("encLoader");
const encBtnText = document.getElementById("encBtnText");

const encOutPreview = document.getElementById("encOutPreview");
const encOutPreviewEmpty = document.getElementById("encOutPreviewEmpty");

const downloadEncBtn = document.getElementById("downloadEncBtn");
const downloadKeyBtn = document.getElementById("downloadKeyBtn");

window._encryptedImageUrl = null;
window._keyJsonData = null;

encryptBtn.addEventListener("click", async () => {
  const file = encImage.files[0];
  const pass = document.getElementById("encPassword").value.trim();

  if (!file) {
    encMsg.textContent = "Please upload an image.";
    return;
  }
  if (pass.length < 4) {
    encMsg.textContent = "Password too short (min 4 chars).";
    return;
  }

  document.getElementById("encProgress").style.width = "0%";
  encLoader.classList.remove("hidden");
  encBtnText.textContent = "Encrypting...";
  encMsg.textContent = "Encrypting...";

  downloadEncBtn.disabled = true;
  downloadKeyBtn.disabled = true;

  encOutPreview.style.display = "none";
  encOutPreview.src = "";
  encOutPreviewEmpty.style.display = "grid";

  document.getElementById("mEntropy").textContent = "--";
  document.getElementById("mNPCR").textContent = "--";
  document.getElementById("mUACI").textContent = "--";

  const timer = startProgress("encProgress");

  try {
    const formData = new FormData();
    formData.append("image", file);
    formData.append("password", pass);

    const res = await fetch(`${API_BASE}/encrypt`, {
      method: "POST",
      body: formData
    });

    const data = await res.json();
    clearInterval(timer);

    if (!res.ok) {
      encMsg.textContent = data.error || "Encryption failed.";
      document.getElementById("encProgress").style.width = "0%";
      return;
    }

    const encUrl = "data:image/png;base64," + data.encrypted_image_base64;
    encOutPreview.src = encUrl;
    encOutPreview.style.display = "block";
    encOutPreviewEmpty.style.display = "none";

    window._encryptedImageUrl = encUrl;
    window._keyJsonData = data.key_json;

    document.getElementById("mEntropy").textContent = data.metrics.entropy;
    document.getElementById("mNPCR").textContent = data.metrics.npcr + "%";
    document.getElementById("mUACI").textContent = data.metrics.uaci + "%";

    document.getElementById("encProgress").style.width = "100%";
    encMsg.textContent = "Encryption successful. Download encrypted image + key.json.";

    downloadEncBtn.disabled = false;
    downloadKeyBtn.disabled = false;

  } catch (err) {
    clearInterval(timer);
    document.getElementById("encProgress").style.width = "0%";
    encMsg.textContent = "Backend not reachable. Please try again later.";
  } finally {
    encLoader.classList.add("hidden");
    encBtnText.textContent = "Encrypt";
  }
});

downloadEncBtn.addEventListener("click", () => {
  if (!window._encryptedImageUrl) return;
  const a = document.createElement("a");
  a.href = window._encryptedImageUrl;
  a.download = "encrypted.png";
  document.body.appendChild(a);
  a.click();
  a.remove();
});

downloadKeyBtn.addEventListener("click", () => {
  if (!window._keyJsonData) return;
  downloadTextFile("key.json", JSON.stringify(window._keyJsonData, null, 2));
});

//DECRYPT API 
const decryptBtn = document.getElementById("decryptBtn");
const decMsg = document.getElementById("decMsg");
const decLoader = document.getElementById("decLoader");
const decBtnText = document.getElementById("decBtnText");

const decOutPreview = document.getElementById("decOutPreview");
const decOutPreviewEmpty = document.getElementById("decOutPreviewEmpty");
const downloadDecBtn = document.getElementById("downloadDecBtn");

window._decryptedImageUrl = null;

decryptBtn.addEventListener("click", async () => {
  const file = decImage.files[0];
  const key = decKey.files[0];
  const pass = document.getElementById("decPassword").value.trim();

  if (!file) {
    decMsg.textContent = "Upload encrypted image.";
    return;
  }
  if (!key) {
    decMsg.textContent = "Upload key.json file.";
    return;
  }
  if (pass.length < 4) {
    decMsg.textContent = "Password too short (min 4 chars).";
    return;
  }

  document.getElementById("decProgress").style.width = "0%";
  decLoader.classList.remove("hidden");
  decBtnText.textContent = "Decrypting...";
  decMsg.textContent = "Decrypting...";

  downloadDecBtn.disabled = true;

  decOutPreview.style.display = "none";
  decOutPreview.src = "";
  decOutPreviewEmpty.style.display = "grid";

  const timer = startProgress("decProgress");

  try {
    const formData = new FormData();
    formData.append("image", file);
    formData.append("key", key);
    formData.append("password", pass);

    const res = await fetch(`${API_BASE}/decrypt`, {
      method: "POST",
      body: formData
    });

    const data = await res.json();
    clearInterval(timer);

    if (!res.ok) {
      decMsg.textContent = data.error || "Decryption failed.";
      document.getElementById("decProgress").style.width = "0%";
      return;
    }

    const decUrl = "data:image/png;base64," + data.decrypted_image_base64;

    decOutPreview.src = decUrl;
    decOutPreview.style.display = "block";
    decOutPreviewEmpty.style.display = "none";

    window._decryptedImageUrl = decUrl;

    document.getElementById("decProgress").style.width = "100%";
    decMsg.textContent = "Decryption successful. Download decrypted output.";

    downloadDecBtn.disabled = false;

  } catch (err) {
    clearInterval(timer);
    document.getElementById("decProgress").style.width = "0%";
    decMsg.textContent = "Backend not reachable. Please try again later.";
  } finally {
    decLoader.classList.add("hidden");
    decBtnText.textContent = "Decrypt";
  }
});

downloadDecBtn.addEventListener("click", () => {
  if (!window._decryptedImageUrl) return;
  const a = document.createElement("a");
  a.href = window._decryptedImageUrl;
  a.download = "decrypted.png";
  document.body.appendChild(a);
  a.click();
  a.remove();
});
