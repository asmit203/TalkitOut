import React, { useState } from "react";
import "./chatbot.css";

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState("");
  const getCookie = (name) => {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(";").shift();
  };
  const handleInputChange = (e) => {
    setInputValue(e.target.value);
  };

  const handleSendMessage = () => {
    if (inputValue.trim() === "") return;

    const newMessages = [...messages, { text: inputValue, isUser: true }];
    setMessages(newMessages);
    var botResponse = "...";
    try {
      fetch("chatbot/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({ query: inputValue.trim() }),
      }).then(async (response) => {
        if (response.ok) {
          botResponse = await response.text();
          botResponse = botResponse.slice(1, -1);
          // Optionally, you can redirect the user or perform other actions after successful submission.
        } else {
          botResponse = "error loading bot response";
          console.error("Form submission failed");
        }
        const newBotMessages = [
          ...newMessages,
          { text: botResponse, isUser: false },
        ];
        setMessages(newBotMessages);
      });
    } catch (error) {
      console.error("Error:", error);
    }

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
