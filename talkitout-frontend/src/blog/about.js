import React, { useEffect, useState } from "react";
import { Base } from "./base";
import { ChatBotSection } from "./chatbot";

const AboutAndChatbot = ({ user, isAuthenticated }) => {
  return (
    <div style={{ padding: "2rem" }}>
      <h1>About</h1>
      <p>A Complete Open Source Blogging Solution.</p>
      <a href="https://github.com/asmit203/TalkitOut">
        https://github.com/asmit203/TalkitOut
      </a>
      <hr></hr>
      <h1>ChatBot</h1>
      <ChatBotSection
        user={user}
        isAuthenticated={isAuthenticated}
      ></ChatBotSection>
    </div>
  );
};

const AboutPage = () => {
  const [friends, setFriends] = useState([]);
  const [others, setOthers] = useState([]);
  const [groups, setGroups] = useState([]);
  const [friendsLastSeen, setFriendsLastSeen] = useState([]);

  useEffect(() => {
    fetch("/api/friends").then(async (response) => {
      if (response.status === 200) {
        response.json().then((data) => {
          console.log(data);
          setFriends(data);
        });
      }
    });
    fetch("/api/friends_last_seen").then(async (response) => {
      if (response.status === 200) {
        response.json().then((data) => {
          console.log(data);
          setFriendsLastSeen(data);
        });
      }
    });
    fetch("/api/groups").then(async (response) => {
      if (response.status === 200) {
        response.json().then((data) => {
          console.log(data);
          setGroups(data);
        });
      }
    });

    fetch("/api/others").then(async (response) => {
      if (response.status === 200) {
        response.json().then((data) => {
          console.log(data);
          setOthers(data);
        });
      }
    });
  }, []);

  return (
    <Base
      friends={friends}
      friendsLastSeen={friendsLastSeen}
      groupsList={groups}
      othersList={others}
    >
      <AboutAndChatbot></AboutAndChatbot>
    </Base>
  );
};
export { AboutPage };
