import React, { useState } from "react";
import "./chatbot.css";

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState("");

  const handleInputChange = (e) => {
    setInputValue(e.target.value);
  };

  const handleSendMessage = () => {
    if (inputValue.trim() === "") return;

    const newMessages = [...messages, { text: inputValue, isUser: true }];
    setMessages(newMessages);

    // Simulate a response from the chatbot (you can replace this with an API call)
    const botResponse = "Hello!";
    const newBotMessages = [
      ...newMessages,
      { text: botResponse, isUser: false },
    ];
    setMessages(newBotMessages);

    // Clear the input field
    setInputValue("");
  };

  return (
    <>
      <div
        className="chatbot-toggle-button"
        onClick={() => {
          document
            .querySelector(".chatbot-container")
            .classList.toggle("hidden");
        }}
      >
        <img src="/chatbot.png" alt="chatbot icon" />
      </div>
      <div className="flexbox chatbot-container hidden">
        <div className="chatbot-messages">
          {messages.map((message, index) => (
            <>
              <div
                key={index}
                className={message.isUser ? "user-message" : "bot-message"}
              >
                {message.text}
              </div>
              {!message.isUser && <hr></hr>}
            </>
          ))}
        </div>
        <div className="flexbox chatbot-input">
          <input
            type="text"
            value={inputValue}
            onChange={handleInputChange}
            placeholder="Type a message..."
          />
          <button onClick={handleSendMessage}>Send</button>
        </div>
      </div>
    </>
  );
};

export { Chatbot };
