import React, { useEffect, useState } from "react";
import { Base } from "./base";

const Announcements = ({ announcements, csrftoken, user }) => {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");

  const handleFormSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch("http://localhost:8000/api/announcements/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({ title, description }),
      });

      if (response.ok) {
        // Clear the form fields and fetch announcements again
        setTitle("");
        setDescription("");
        window.location.reload();
      } else {
        console.error("Failed to submit announcement");
      }
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <div>
      {user.is_superuser && (
        <form onSubmit={handleFormSubmit}>
          <label>Title:</label>
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
          />

          <label>Description:</label>
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
          ></textarea>

          <button type="submit">Submit</button>
        </form>
      )}
      <div className="container">
        {announcements.map((announce) => (
          <div key={announce.id}>
            <h2>{announce.title}</h2>
            <p dangerouslySetInnerHTML={{ __html: announce.description }}></p>
          </div>
        ))}
      </div>
    </div>
  );
};

const AnnouncementsPage = () => {
  const [announcements, setAnnouncements] = useState([]);
  const getCookie = (name) => {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(";").shift();
  };
  const csrftoken = getCookie("csrftoken");
  useEffect(() => {
    fetch("/api/announcements").then(async (response) => {
      if (response.status === 200) {
        response.json().then((data) => {
          console.log(data);
          setAnnouncements(data);
        });
      }
    });
  }, []);

  return (
    <Base>
      <Announcements announcements={announcements} csrftoken={csrftoken} />
    </Base>
  );
};
export { AnnouncementsPage };
