import React, { useState } from "react";
import "./chatbot.css";

const ChatbotWidget = () => {
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
const ChatBotSection = ({ user, isAuthenticated }) => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState("");
  const [attachedFiles, setAttachedFiles] = useState([]);

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

    const newMessages = [
      ...messages,
      {
        text:
          inputValue +
          "<br>" +
          (document.querySelector(".attachedFiles>div").innerHTML || ""),
        isUser: true,
      },
    ];
    setMessages(newMessages);
    var botResponse = "...";
    try {
      fetch("chatbot/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({
          query: inputValue.trim(),
          attached: attachedFiles,
        }),
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
    setAttachedFiles([]);
  };
  const cancelModal = () => {
    document.querySelector(".modal-chatbot input").value = "";
    document.querySelector(".modal-chatbot").classList.add("hidden");
  };
  const attachFile = () => {
    if (document.querySelector(".modal-chatbot input").value.trim() === "")
      return;
    setAttachedFiles([
      ...attachedFiles,
      document.querySelector(".modal-chatbot input").value,
    ]);
    document.querySelector(".modal-chatbot input").value = "";
    document.querySelector(".modal-chatbot").classList.add("hidden");
  };
  return (
    <>
      <div className="modal-chatbot hidden">
        <div className="flexbox card">
          <h1>Attach Files</h1>
          <p>
            Upload a File and get its link from{" "}
            <a
              style={{ display: "block" }}
              href={"http://localhost:8000/stream/user/" + user.username}
              target="_blank"
              rel="noreferrer"
            >
              Here.
            </a>{" "}
            <input
              type="text"
              className="fileLink"
              placeholder="Paste File Link Here"
            />
          </p>
          <div className="flexbox buttonContainer">
            <button className="secondary" onClick={cancelModal}>
              Cancel
            </button>
            <button onClick={attachFile}>Attach</button>
          </div>
        </div>
      </div>
      <div className="flexbox chatbot-section-container">
        <div className="chatbot-messages">
          {messages.map((message, index) => (
            <>
              <div
                key={index}
                className={message.isUser ? "user-message" : "bot-message"}
                dangerouslySetInnerHTML={{ __html: message.text }}
              ></div>
              {!message.isUser && <hr></hr>}
            </>
          ))}
        </div>
        <div
          className={
            attachedFiles.length === 0
              ? "attachedFiles hidden"
              : "attachedFiles"
          }
        >
          <strong>Attached Files</strong>
          <div>
            {attachedFiles.map((file) => (
              <a
                href={"http://localhost:8000" + file}
                target="_blank"
                rel="noreferrer"
              >
                {file}
              </a>
            ))}
          </div>
        </div>
        <div className="flexbox chatbot-input">
          <input
            type="text"
            value={inputValue}
            onChange={handleInputChange}
            placeholder="Type a message..."
          />
          <button onClick={handleSendMessage}>Send</button>
          <button
            className="upload"
            onClick={() => {
              if (!isAuthenticated) {
                alert("Please Login to Upload Files");
                return;
              }
              document
                .querySelector(".modal-chatbot")
                .classList.remove("hidden");
            }}
          >
            Upload
          </button>
        </div>
      </div>
    </>
  );
};
export { ChatbotWidget, ChatBotSection };
