import { useState } from "react";
import { useParams } from "react-router-dom";
import { api } from "../api/client";
import "./ChatbotWidget.css";

function ChatbotWidget() {
  const [isOpen, setIsOpen] = useState(false);
  const [isMaximized, setIsMaximized] = useState(false);
  const [message, setMessage] = useState("");
  const [isSending, setIsSending] = useState(false);
  const { grade, subject } = useParams();

  const [messages, setMessages] = useState([
    {
      sender: "bot",
      text: "Hi! I'm your AI Doubt Solver. Ask me anything about this topic.",
    },
  ]);

  const sendMessage = async () => {
    if (!message.trim()) {
      return;
    }

    const userMessage = {
      sender: "user",
      text: message,
    };

    setMessages((previousMessages) => [...previousMessages, userMessage]);
    setMessage("");
    setIsSending(true);
    try {
      const response = await api.ask(userMessage.text, { className: grade, subject });
      setMessages((previousMessages) => [...previousMessages, { sender: "bot", text: response.answer }]);
    } catch (error) {
      setMessages((previousMessages) => [...previousMessages, { sender: "bot", text: error.message }]);
    } finally {
      setIsSending(false);
    }
  };

  return (
    <>
      {!isOpen && (
        <button
          className="chatbot-toggle"
          onClick={() => setIsOpen(true)}
        >
          💬
        </button>
      )}

      {isOpen && (
        <div className={`chatbot-window ${isMaximized ? "maximized" : ""}`}>
          <div className="chatbot-header">
            <div>
              <h3>AI Doubt Solver</h3>
              <span>Ask your doubts</span>
            </div>

            <div className="chatbot-header-actions">
              <button
                className="chatbot-maximize"
                onClick={() => setIsMaximized(!isMaximized)}
                title={isMaximized ? "Restore size" : "Maximize window"}
              >
                {isMaximized ? "🗗" : "⛶"}
              </button>

              <button
                className="chatbot-close"
                onClick={() => {
                  setIsOpen(false);
                  setIsMaximized(false);
                }}
              >
                ×
              </button>
            </div>
          </div>

          <div className="chatbot-messages">
            {messages.map((msg, index) => (
              <div
                key={index}
                className={`chat-message ${msg.sender}`}
              >
                {msg.text}
              </div>
            ))}
          </div>

          <div className="chatbot-input-area">
            <input
              type="text"
              placeholder="Ask a question..."
              value={message}
              disabled={isSending}
              onChange={(e) => setMessage(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  sendMessage();
                }
              }}
            />

            <button onClick={sendMessage}>
              ➤
            </button>
          </div>
        </div>
      )}
    </>
  );
}

export default ChatbotWidget;