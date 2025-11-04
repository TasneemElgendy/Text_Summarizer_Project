// static/js/main.js

document.addEventListener("DOMContentLoaded", () => {
    const inputText = document.getElementById("inputText");
    const charCount = document.getElementById("charCount");
    const summarizeBtn = document.getElementById("summarizeBtn");
    const summaryBox = document.getElementById("summary");
    const copyBtn = document.getElementById("copyBtn");
    const clearBtn = document.getElementById("clearBtn");
    const lengthRange = document.getElementById("lengthRange");
    const lengthLabel = document.getElementById("lengthLabel");
    const dropzone = document.getElementById("dropzone");
    const fileInput = document.getElementById("fileInput");

    const MAX_CHARS = 4000;

    // تحديث العداد
    inputText.addEventListener("input", () => {
        const len = inputText.value.length;
        charCount.textContent = `${len.toLocaleString()} / ${MAX_CHARS} characters`;
        if (len > MAX_CHARS) {
        inputText.value = inputText.value.substring(0, MAX_CHARS);
        }
    });

    // تحميل ملف نصي
    dropzone.addEventListener("click", () => fileInput.click());
    fileInput.addEventListener("change", handleFileUpload);

    dropzone.addEventListener("dragover", (e) => {
        e.preventDefault();
        dropzone.classList.add("dragover");
    });
    dropzone.addEventListener("dragleave", () => dropzone.classList.remove("dragover"));
    dropzone.addEventListener("drop", (e) => {
        e.preventDefault();
        dropzone.classList.remove("dragover");
        const file = e.dataTransfer.files[0];
        handleTextFile(file);
    });

    function handleFileUpload(e) {
        const file = e.target.files[0];
        handleTextFile(file);
    }

    function handleTextFile(file) {
        if (!file || !file.name.endsWith(".txt")) return alert("Please upload a .txt file");
        const reader = new FileReader();
        reader.onload = (e) => {
        inputText.value = e.target.result.substring(0, MAX_CHARS);
        const len = inputText.value.length;
        charCount.textContent = `${len.toLocaleString()} / ${MAX_CHARS} characters`;
        };
        reader.readAsText(file);
    }

    // تغيير طول الملخص
    lengthRange.addEventListener("input", () => {
        const val = parseInt(lengthRange.value);
        if (val <= 20) lengthLabel.textContent = `Short (${val}%)`;
        else if (val <= 35) lengthLabel.textContent = `Medium (${val}%)`;
        else lengthLabel.textContent = `Long (${val}%)`;
    });

    // زر التلخيص
    summarizeBtn.addEventListener("click", async () => {
        const text = inputText.value.trim();
        if (!text) {
        alert("Please enter text to summarize.");
        return;
        }

        summarizeBtn.classList.add("loading");
        summarizeBtn.textContent = "Summarizing...";

        summaryBox.innerHTML = `<div style="color: var(--muted);">Processing your summary...</div>`;

        try {
        const response = await fetch("/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text }),
        });

        const result = await response.json();
        if (result.error) throw new Error(result.error);

        summaryBox.textContent = result.summary || "No summary returned.";
        } catch (err) {
        summaryBox.textContent = "⚠️ Error: " + err.message;
        } finally {
        summarizeBtn.classList.remove("loading");
        summarizeBtn.textContent = "Summarize Now";
        }
    });

    // زر النسخ
    copyBtn.addEventListener("click", async () => {
        const summary = summaryBox.textContent.trim();
        if (!summary || summary.startsWith("No summary")) return;
        try {
        await navigator.clipboard.writeText(summary);
        copyBtn.textContent = "Copied!";
        setTimeout(() => (copyBtn.textContent = "Copy Summary"), 1500);
        } catch {
        alert("Failed to copy text.");
        }
    });

    // زر المسح
    clearBtn.addEventListener("click", () => {
        inputText.value = "";
        summaryBox.innerHTML = `<div style="color:var(--muted);">No summary yet. Click "Summarize Now" to create one.</div>`;
        charCount.textContent = `0 / ${MAX_CHARS} characters`;
    });
});
