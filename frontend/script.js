const BACKEND_URL = "http://127.0.0.1:8000";

const chat = document.getElementById("chat");
const questionInput = document.getElementById("question");
const fileChipContainer = document.getElementById("fileChipContainer");
const pdfFileInput = document.getElementById("pdfFile");


// Track currently attached file's chip element
let currentChip = null;


// Called when user picks a file from the "+" button
function handleFileSelect(event) {

    const file = event.target.files[0];

    if (!file) {
        return;
    }

    // Show the chip inside the search bar right away
    showFileChip(file.name, "uploading");

    // Kick off the actual upload
    uploadPDF(file);
}


// Render (or replace) the file chip shown above the textarea
function showFileChip(fileName, state) {

    // Remove any existing chip first (only one file at a time)
    fileChipContainer.innerHTML = "";

    const chip = document.createElement("div");

    chip.className = "file-chip" + (state === "error" ? " error" : state === "uploading" ? " uploading" : "");

    const typeLabel = state === "uploading" ? "Uploading..." : state === "error" ? "Failed" : "PDF";

    chip.innerHTML = `
        <div class="file-chip-icon-box">📄</div>
        <div class="file-chip-text">
            <span class="file-chip-name" title="${escapeHTML(fileName)}">${escapeHTML(fileName)}</span>
            <span class="file-chip-type">${typeLabel}</span>
        </div>
        <span class="file-chip-remove" title="Remove">✕</span>
    `;

    chip.querySelector(".file-chip-remove").addEventListener("click", removeFileChip);

    fileChipContainer.appendChild(chip);

    currentChip = chip;
}


// Update the existing chip's state/text once upload finishes/fails
function updateFileChip(fileName, state) {

    if (!currentChip) {
        return;
    }

    currentChip.className = "file-chip" + (state === "error" ? " error" : "");

    const typeLabel = state === "error" ? "Failed" : "PDF";

    currentChip.innerHTML = `
        <div class="file-chip-icon-box">📄</div>
        <div class="file-chip-text">
            <span class="file-chip-name" title="${escapeHTML(fileName)}">${escapeHTML(fileName)}</span>
            <span class="file-chip-type">${typeLabel}</span>
        </div>
        <span class="file-chip-remove" title="Remove">✕</span>
    `;

    currentChip.querySelector(".file-chip-remove").addEventListener("click", removeFileChip);
}


// Remove the chip and reset the file input
function removeFileChip() {

    fileChipContainer.innerHTML = "";

    currentChip = null;

    pdfFileInput.value = "";
}


// Upload PDF
async function uploadPDF(file) {

    if (!file) {
        return;
    }

    const formData = new FormData();

    formData.append("file", file);

    try {

        const response = await fetch(
            `${BACKEND_URL}/upload`,
            {
                method: "POST",
                body: formData
            }
        );

        const data = await response.json();

        if (!response.ok) {

            updateFileChip(file.name, "error");

            addAIMessage(
                "❌ " + (data.error || "PDF upload failed.")
            );

            return;
        }

        // Mark the chip as successfully attached
        updateFileChip(file.name, "done");

        addAIMessage(
            `✅ PDF processed successfully.\n\nPages: ${data.pages}\nChunks: ${data.chunks}`
        );

    } catch (error) {

        updateFileChip(file.name, "error");

        addAIMessage(
            "❌ Cannot connect to the backend."
        );

        console.error(error);
    }
}


// Ask Question
async function askQuestion() {

    const question = questionInput.value.trim();

    if (!question) {
        return;
    }


    // Remove welcome screen
    const welcome = document.querySelector(".welcome");

    if (welcome) {
        welcome.remove();
    }


    // Show user question
    addUserMessage(question);


    // Clear input
    questionInput.value = "";


    // Reset textarea height
    questionInput.style.height = "auto";


    // Show loading
    const loading = addAIMessage("Thinking...", true);


    try {

        const response = await fetch(
            `${BACKEND_URL}/query?question=${encodeURIComponent(question)}`
        );

        const data = await response.json();


        // Remove loading
        loading.remove();


        if (!response.ok) {

            addAIMessage(
                "❌ " + (data.detail || "Something went wrong.")
            );

            return;
        }


        // Show AI answer
        addAIMessage(data.answer);


    } catch (error) {

        loading.remove();

        addAIMessage(
            "❌ Cannot connect to the backend."
        );

        console.error(error);
    }
}


// Add User Message
function addUserMessage(text) {

    const message = document.createElement("div");

    message.className = "message user-message";

    message.innerHTML = `
        <div class="bubble">
            ${escapeHTML(text)}
        </div>
    `;

    chat.appendChild(message);

    scrollToBottom();
}


// Add AI Message
function addAIMessage(text, loading = false) {

    const message = document.createElement("div");

    message.className = "message ai-message";

    if (loading) {
        message.innerHTML = `
            <div class="bubble loading">
                ${text}
            </div>
        `;
    } else {
        message.innerHTML = `
            <div class="bubble">
                ${escapeHTML(text)}
            </div>
        `;
    }

    chat.appendChild(message);

    scrollToBottom();

    return message;
}


// Scroll to latest message
function scrollToBottom() {

    chat.scrollTop = chat.scrollHeight;
}


// Prevent HTML injection
function escapeHTML(text) {

    const div = document.createElement("div");

    div.textContent = text;

    return div.innerHTML;
}


// Enter = Send
// Shift + Enter = New Line
questionInput.addEventListener("keydown", function(event) {

    if (event.key === "Enter" && !event.shiftKey) {

        event.preventDefault();

        askQuestion();
    }

});


// Auto resize textarea
questionInput.addEventListener("input", function() {

    this.style.height = "auto";

    this.style.height =
        Math.min(this.scrollHeight, 150) + "px";

});