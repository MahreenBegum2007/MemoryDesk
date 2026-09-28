const messageInput = document.getElementById("messageInput");
const sendButton = document.getElementById("sendButton");
const chatBox = document.getElementById("chatBox");
const memoryList = document.getElementById("memoryList");
const memoryCount = document.getElementById("memoryCount");

function addMessage(text, type) {
    const message = document.createElement("div");
    message.className = `message ${type}`;

    const content = document.createElement("div");
    content.className = "message-content";
    content.textContent = text;

    message.appendChild(content);
    chatBox.appendChild(message);

    chatBox.scrollTop = chatBox.scrollHeight;
}

function showMemories(memories) {
    memoryList.innerHTML = "";

    if (!memories || memories.length === 0) {
        memoryCount.textContent = "0";

        memoryList.innerHTML = `
            <div class="empty-memory">
                <div class="empty-icon">🧠</div>
                <p>No relevant memories yet.</p>
                <small>MemoryDesk will learn from this conversation.</small>
            </div>
        `;

        return;
    }

    memoryCount.textContent = memories.length;

    // Memory status
    const status = document.createElement("div");
    status.className = "memory-status";
    status.innerHTML = `
        <span class="memory-dot"></span>
        <div>
            <strong>Memory Used</strong>
            <small>${memories.length} relevant ${memories.length === 1 ? "memory" : "memories"} found</small>
        </div>
    `;

    memoryList.appendChild(status);

    // Memory cards
    memories.forEach((memory, index) => {
        const card = document.createElement("div");
        card.className = "memory-card";

        card.innerHTML = `
            <div class="memory-card-top">
                <span class="memory-number">Memory ${index + 1}</span>
                <span class="memory-check">✓</span>
            </div>
            <div class="memory-text"></div>
        `;

        card.querySelector(".memory-text").textContent = memory;

        memoryList.appendChild(card);
    });

    // Learning indicator
    const learning = document.createElement("div");
    learning.className = "learning-box";
    learning.innerHTML = `
        <div class="learning-icon">✨</div>
        <div>
            <strong>Memory updated</strong>
            <small>This interaction helps MemoryDesk understand Alex better.</small>
        </div>
    `;

    memoryList.appendChild(learning);
}

async function sendMessage() {
    const message = messageInput.value.trim();

    if (!message) {
        return;
    }

    addMessage(message, "user");

    messageInput.value = "";
    sendButton.disabled = true;
    sendButton.textContent = "Thinking...";

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
            throw new Error(data.detail || "Something went wrong");
        }

        addMessage(data.answer, "ai");

        showMemories(data.memories);

    } catch (error) {
        addMessage(
            "Sorry, something went wrong. Please try again.",
            "ai"
        );

        console.error(error);

    } finally {
        sendButton.disabled = false;
        sendButton.textContent = "Send ➤";
        messageInput.focus();
    }
}

sendButton.addEventListener("click", sendMessage);

messageInput.addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});