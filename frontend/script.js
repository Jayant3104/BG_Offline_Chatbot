/* ================= SIDEBAR ================= */

const sidebar = document.getElementById("chatbotSidebar");
const openBtn = document.getElementById("openSidebarBtn");
const headerLogo = document.getElementById("headerLogo");

function closeSidebar() {
    sidebar.classList.add("is-hidden");
    openBtn.classList.add("show");
    headerLogo.classList.add("show");
}

function openSidebar() {
    sidebar.classList.remove("is-hidden");
    openBtn.classList.remove("show");
    headerLogo.classList.remove("show");
}

function startNewChat() {
    location.reload();
}

/* ================= CHAT FLOW ================= */

function openChat() {
    document.getElementById("startScreen").style.display = "none";
    document.getElementById("chatArea").style.display = "flex";

    const question = document.getElementById("queryInput").value.trim();
    const alarm = document.getElementById("alarmCodeInput").value.trim();

    if (!question && !alarm) return;

    // Show user message
    addMessage("user", alarm || question);

    // Call backend with BOTH fields
    callBot({
        query: question || null,
        alarm_code: alarm || null
    });

    // Clear inputs
    document.getElementById("queryInput").value = "";
    document.getElementById("alarmCodeInput").value = "";
}


function sendMessage() {
    const input = document.getElementById("chatInput");
    const text = input.value.trim();
    if (!text) return;

    addMessage("user", text);
    input.value = "";

    // Chat input is treated as query
    callBot({
        query: text,
        alarm_code: null
    });
}

/* ================= MESSAGE UI ================= */

function addMessage(type, text) {
    const chatMessages = document.getElementById("chatMessages");

    const div = document.createElement("div");
    div.className = `message ${type}`;
    div.innerText = text;

    chatMessages.appendChild(div);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    return div;
}

/* ================= BACKEND CALL ================= */

const BACKEND_URL = "http://127.0.0.1:8000/chat";

async function callBackend(payload) {
    try {
        console.log("Sending payload:", payload); // DEBUG

        const response = await fetch(BACKEND_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            throw new Error("Backend error");
        }

        const data = await response.json();
        return data.reply || "No response from server.";

    } catch (error) {
        console.error("Backend connection failed:", error);
        return "❌ Unable to connect to server. Please try again.";
    }
}

/* ================= BOT LOGIC ================= */

async function callBot(payload) {
    const chatMessages = document.getElementById("chatMessages");

    // Loading bubble
    const botDiv = document.createElement("div");
    botDiv.className = "message bot";
    botDiv.innerText = "Loading...";
    chatMessages.appendChild(botDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    // Backend response
    const reply = await callBackend(payload);

    // Replace loading with real reply
    botDiv.innerText = reply;
}

/* ================= ENTER KEY SUPPORT ================= */

document.addEventListener("DOMContentLoaded", () => {
    const chatInput = document.getElementById("chatInput");
    if (chatInput) {
        chatInput.addEventListener("keydown", (e) => {
            if (e.key === "Enter") {
                e.preventDefault();
                sendMessage();
            }
        });
    }
});
/* ================= ENTER KEY SUPPORT (HOME PAGE) ================= */

document.addEventListener("DOMContentLoaded", () => {
    const queryInput = document.getElementById("queryInput");
    const alarmCodeInput = document.getElementById("alarmCodeInput");

    function handleHomeEnter(e) {
        if (e.key === "Enter") {
            e.preventDefault();
            openChat();
        }
    }

    if (queryInput) {
        queryInput.addEventListener("keydown", handleHomeEnter);
    }

    if (alarmCodeInput) {
        alarmCodeInput.addEventListener("keydown", handleHomeEnter);
    }
});
