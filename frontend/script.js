const messageInput = document.getElementById("messageInput");
const sendButton = document.getElementById("sendButton");
const chatBox = document.getElementById("chatBox");

const memoryList = document.getElementById("memoryList");
const memoryCount = document.getElementById("memoryCount");
const memoryState = document.getElementById("memoryState");
const memoryTimeline = document.getElementById("memoryTimeline");

const responseWhy = document.getElementById("responseWhy");
const whyMemoryText = document.getElementById("whyMemoryText");

let memoryHistory = [];
let isSending = false;


// ========================================
// FORMAT AI RESPONSE
// ========================================

function formatAIResponse(text) {
    if (!text) {
        return "";
    }

    if (typeof marked !== "undefined") {
        return marked.parse(text, {
            breaks: true,
            gfm: true
        });
    }

    return text.replace(/\n/g, "<br>");
}


// ========================================
// ADD MESSAGE
// ========================================

function addMessage(text, type) {

    if (!text) {
        return;
    }

    // Prevent the same AI response from being rendered twice
    if (type === "ai") {

        const existingMessages =
            chatBox.querySelectorAll(".message.ai");

        for (const message of existingMessages) {

            const existingContent =
                message.querySelector(".message-content");

            if (
                existingContent &&
                existingContent.dataset.rawText === text
            ) {
                console.log("Duplicate AI response blocked.");
                return;
            }
        }
    }

    const message = document.createElement("div");

    message.className = "message " + type;

    const content = document.createElement("div");

    content.className = "message-content";

    if (type === "ai") {

        content.dataset.rawText = text;

        content.innerHTML = formatAIResponse(text);

    } else {

        content.textContent = text;

    }

    message.appendChild(content);

    chatBox.appendChild(message);

    chatBox.scrollTop = chatBox.scrollHeight;
}

// ========================================
// MEMORY STATE
// ========================================

function updateMemoryState(memories) {

    if (!memoryState) {
        return;
    }

    if (memories && memories.length > 0) {

        memoryState.className = "memory-state recalled";

        memoryState.innerHTML = `
            <span class="state-icon">🔎</span>

            <div>
                <strong>MEMORY RECALLED</strong>

                <small>
                    ${memories.length}
                    relevant ${memories.length === 1 ? "memory" : "memories"}
                    influenced this response.
                </small>
            </div>
        `;

    } else {

        memoryState.className = "memory-state learned";

        memoryState.innerHTML = `
            <span class="state-icon">✨</span>

            <div>
                <strong>NEW MEMORY LEARNED</strong>

                <small>
                    This interaction has been added to Alex's memory.
                </small>
            </div>
        `;
    }
}


// ========================================
// WHY THIS RESPONSE
// ========================================

function showResponseWhy(memories) {

    if (!responseWhy || !whyMemoryText) {
        return;
    }

    if (!memories || memories.length === 0) {

        responseWhy.classList.add("hidden");

        return;
    }

    responseWhy.classList.remove("hidden");

    whyMemoryText.innerHTML = "";

    const label = document.createElement("div");

    label.className = "why-memory-label";

    label.textContent = "Memory used:";

    whyMemoryText.appendChild(label);

    memories.slice(0, 3).forEach(function(memory) {

        const item = document.createElement("div");

        item.className = "why-memory-item";

        item.textContent = memory;

        whyMemoryText.appendChild(item);

    });
}


// ========================================
// MEMORY TIMELINE
// ========================================

function updateMemoryTimeline(memories) {

    if (!memoryTimeline) {
        return;
    }

    if (memories && memories.length > 0) {

        memories.forEach(function(memory) {

            if (!memoryHistory.includes(memory)) {
                memoryHistory.push(memory);
            }

        });
    }

    if (memoryHistory.length === 0) {

        memoryTimeline.innerHTML = `
            <div class="timeline-empty">

                <div class="timeline-empty-icon">🧠</div>

                <p>No memories yet</p>

                <small>
                    Start chatting to build Alex's memory.
                </small>

            </div>
        `;

        return;
    }

    memoryTimeline.innerHTML = "";

    const recentMemories = [...memoryHistory]
        .reverse()
        .slice(0, 6);

    recentMemories.forEach(function(memory, index) {

        const item = document.createElement("div");

        item.className = "timeline-item";

        item.innerHTML = `
            <div class="timeline-line">
                <div class="timeline-dot"></div>
            </div>

            <div class="timeline-content">

                <div class="timeline-date">
                    ${index === 0 ? "Just now" : "Previous interaction"}
                </div>

                <div class="timeline-memory"></div>

            </div>
        `;

        item.querySelector(".timeline-memory").textContent = memory;

        memoryTimeline.appendChild(item);

    });
}


// ========================================
// MEMORY CARDS
// ========================================

function showMemories(memories) {

    if (!memoryList || !memoryCount) {
        return;
    }

    memoryList.innerHTML = "";

    if (!memories || memories.length === 0) {

        memoryCount.textContent = "0 memories";

        memoryList.innerHTML = `
            <div class="empty-memory">

                <div class="empty-icon">🧠</div>

                <p>No memories found yet.</p>

                <small>
                    MemoryDesk will learn from this conversation.
                </small>

            </div>
        `;

        return;
    }

    memoryCount.textContent =
        memories.length +
        (memories.length === 1 ? " memory" : " memories");

    memories.forEach(function(memory, index) {

        const card = document.createElement("div");

        card.className = "memory-card";

        card.innerHTML = `
            <div class="memory-card-top">

                <span class="memory-number">
                    Memory ${index + 1}
                </span>

                <span class="memory-check">
                    ✓
                </span>

            </div>

            <div class="memory-text"></div>
        `;

        card.querySelector(".memory-text").textContent = memory;

        memoryList.appendChild(card);

    });
}


// ========================================
// SEND MESSAGE
// ========================================

async function sendMessage() {

    // VERY IMPORTANT:
    // Stop duplicate requests.
    if (isSending) {
        return;
    }

    const message = messageInput.value.trim();

    if (!message) {
        return;
    }

    isSending = true;

    sendButton.disabled = true;

    sendButton.textContent = "Thinking...";


    // ------------------------------------
    // USER MESSAGE
    // ------------------------------------

    addMessage(message, "user");

    messageInput.value = "";


    if (responseWhy) {
        responseWhy.classList.add("hidden");
    }


    try {

        const response = await fetch("/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                customer_name: "Alex",
                message: message
            })

        });


        const data = await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail || "Something went wrong"
            );

        }


        // ------------------------------------
        // AI RESPONSE
        // ------------------------------------

        addMessage(data.answer, "ai");


        // ------------------------------------
        // MEMORY UI
        // ------------------------------------
        addMessage(data.answer, "ai");

        showMemories(data.memories);

        updateMemoryState(data.memories);

        showResponseWhy(data.memories);

        updateMemoryTimeline(data.memories);

    }

    catch (error) {

        console.error("MemoryDesk error:", error);

        addMessage(
            "Sorry, something went wrong. Please try again.",
            "ai"
        );

    }

    finally {

        isSending = false;

        sendButton.disabled = false;

        sendButton.textContent = "Send ➤";

        messageInput.focus();

    }
}


// ========================================
// BUTTON
// ========================================

sendButton.onclick = sendMessage;


// ========================================
// ENTER KEY
// ========================================

messageInput.onkeydown = function(event) {

    if (event.key === "Enter" && !event.shiftKey) {

        event.preventDefault();

        sendMessage();

    }

};