import { useState } from "react";
import "./ChatbotWidget.css";

function ChatbotWidget() {
  const [isOpen, setIsOpen] = useState(false);
  const [isMaximized, setIsMaximized] = useState(false);
  const [message, setMessage] = useState("");

  const [messages, setMessages] = useState([
    {
      sender: "bot",
      text: "Hi! I'm your AI Doubt Solver. Ask me anything about this topic.",
    },
  ]);

  const sendMessage = () => {
    if (!message.trim()) {
      return;
    }

    const userMessage = {
      sender: "user",
      text: message,
    };

    const botMessage = {
      sender: "bot",
      text: "I'm currently a demo chatbot. A real AI response will be connected later.",
    };

    setMessages((previousMessages) => [
      ...previousMessages,
      userMessage,
      botMessage,
    ]);

    setMessage("");
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