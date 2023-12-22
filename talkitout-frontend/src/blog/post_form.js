import React, { useState } from "react";

const PostForm = ({ csrf }) => {
  const [formData, setFormData] = useState({
    title: "",
    content: "",
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleFormSubmit = async (e) => {
    e.preventDefault();
    // Your form submission logic goes here
    console.log("Form data:", formData);
    try {
      fetch("/api/post/new/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrf,
        },
        body: JSON.stringify(formData),
      }).then((response) => {
        if (response.ok) {
          console.log("Form submission successful");
          // Optionally, you can redirect the user or perform other actions after successful submission.
        } else {
          console.error("Form submission failed");
        }
      });
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <div className="content-section">
      <form onSubmit={handleFormSubmit} enctype="multipart/form-data">
        <fieldset className="form-group">
          <legend className="border-bottom mb-4">Blog Post</legend>
          <input type="hidden" name="csrfmiddlewaretoken" value={csrf} />
          {/* Title input */}
          <div className="form-group">
            <label htmlFor="title">Title:</label>
            <input
              type="text"
              id="title"
              name="title"
              value={formData.title}
              onChange={handleInputChange}
              className="form-control"
            />
          </div>

          {/* Content textarea */}
          <div className="form-group">
            <label htmlFor="content">Content:</label>
            <textarea
              id="content"
              name="content"
              value={formData.content}
              onChange={handleInputChange}
              className="form-control"
            />
          </div>
        </fieldset>

        <div className="form-group">
          <button className="btn btn-outline-info" type="submit">
            Post
          </button>
        </div>
      </form>
    </div>
  );
};

export { PostForm };
