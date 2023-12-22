import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { Base } from "./base";

const DeletePostForm = ({ user, isAuthenticated }) => {
  const [post, setPost] = useState(null);
  const postId = useParams().id;
  const getCookie = (name) => {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(";").shift();
  };
  useEffect(() => {
    // Fetch the post data when the component mounts
    fetch(`/api/post/${postId}/`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
    })
      .then((response) => response.json())
      .then((data) => {
        setPost(data.post);
        console.log(data);
      })
      .catch((error) => console.error("Error fetching post:", error));
  }, [postId]);

  const handleDelete = (e) => {
    e.preventDefault();
    // Send a DELETE request to the server
    fetch(`/api/post/${postId}/delete/`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
    })
      .then((response) => {
        console.log(response);
        if (response.ok) {
          // Handle successful deletion
          console.log("Post deleted successfully");
          window.location = "/";
        } else {
          // Handle error in deletion
          alert("Failed to delete post! see console output for more details.");
          console.error("Failed to delete post");
        }
      })
      .catch((error) => console.error("Error deleting post:", error));
  };

  if (!post) {
    return <div>Loading...</div>;
  }
  const csrftoken = getCookie("csrftoken");
  return (
    <Base>
      <div className="content-section">
        <form onSubmit={handleDelete}>
          <fieldset className="form-group">
            <legend className="border-bottom mb-4">Delete Post</legend>
            <h2>Are you sure you want to delete the post "{post.title}"?</h2>
          </fieldset>
          <input type="hidden" name="csrfmiddlewaretoken" value={csrftoken} />
          <div className="form-group">
            <button className="btn btn-outline-danger" type="submit">
              Yes, Delete
            </button>
            <a className="btn btn-outline-secondary" href={`/post/${post.id}/`}>
              Cancel
            </a>
          </div>
        </form>
      </div>
    </Base>
  );
};

export { DeletePostForm };
