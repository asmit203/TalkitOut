import React, { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom"; // Assuming you are using React Router for navigation
import { Base } from "./base";

const FavoriteButton = ({ postId, csrf }) => {
  const handleFavorite = async () => {
    try {
      const response = await fetch(`http://localhost:8000/api/fav/${postId}/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrf, // Replace with your CSRF token
        },
        credentials: "include",
      });

      if (response.ok) {
        console.log("Post added to favorites!");
        // Optionally, you can update the UI or state to reflect the change
      } else {
        console.error("Failed to add post to favorites");
      }
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <button
      className="btn btn-info"
      onClick={handleFavorite}
      style={{ marginLeft: "550px", position: "relative", top: "-60px" }}
    >
      &hearts;
    </button>
  );
};

const PostDetail = ({
  post,
  user,
  isAuthenticated,
  postIsVoted,
  comments,
  number_of_votes,
  csrftoken,
}) => {
  const [commentText, setCommentText] = useState("");
  const handleVote = async (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);

    try {
      const response = await fetch(e.target.action, {
        method: "POST",
        headers: {
          "X-CSRFToken": formData.get("csrfmiddlewaretoken"),
        },
        body: formData,
        credentials: "include",
      });

      const data = await response.json();
      window.location.href = data.redirect_url;
      // Update your component state or take further action based on the response
    } catch (error) {
      console.error("Error:", error);
    }
  };
  const handleComment = async (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);

    try {
      await fetch(e.target.action, {
        method: "POST",
        headers: {
          "X-CSRFToken": formData.get("csrfmiddlewaretoken"),
        },
        body: formData,
        credentials: "include",
      });

      window.location.reload();
      // Update your component state or take further action based on the response
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <article className="media content-section">
      <img
        className="rounded-circle article-img"
        src={post.author.profile.image}
        alt="Author"
      />
      <div className="media-body">
        <div className="article-metadata">
          <Link to={`user-posts/${post.author.username}`} className="mr-2">
            {post.author.username}
          </Link>
          <small className="text-muted">
            {new Date(post.date_posted).toLocaleDateString()}
          </small>
          {post.author.username === user.username && (
            <div>
              <Link
                to={`http://localhost:8000/api/post/${post.id}/update/`}
                className="btn btn-secondary btn-sm mt-1 mb-1"
              >
                Update
              </Link>
              <Link
                to={`/post/${post.id}/delete/`}
                className="btn btn-danger btn-sm mt-1 mb-1"
              >
                Delete
              </Link>
            </div>
          )}
        </div>
        <h2 className="article-title">{post.title}</h2>
        <p
          className="article-content"
          dangerouslySetInnerHTML={{ __html: post.content }}
        ></p>
        {isAuthenticated ? (
          <>
            <form
              action={"http://localhost:8000/api/post-vote/" + post.id + "/"}
              method="POST"
              onSubmit={handleVote}
            >
              <input
                type="hidden"
                name="csrfmiddlewaretoken"
                value={csrftoken}
              />
              <input type="hidden" name="post_id" value={post.id} />
              {postIsVoted ? (
                <button type="submit" className="btn btn-info" value={post.id}>
                  Unlike
                </button>
              ) : (
                <button type="submit" className="btn btn-info" value={post.id}>
                  Like
                </button>
              )}
            </form>
            <h5>Comments</h5>
            {comments.map((comment) => (
              <p key={comment.id}>
                {comment.author} says: {comment.text}
              </p>
            ))}
            <h5>Add Comment</h5>

            <form
              action={"http://localhost:8000/api/post/comment/" + post.id + "/"}
              method="POST"
              onSubmit={handleComment}
            >
              <input
                type="hidden"
                name="csrfmiddlewaretoken"
                value={csrftoken}
              />{" "}
              <input type="hidden" name="post_id" value={post.id} />
              <textarea
                className="form-control"
                name="text"
                value={commentText}
                onChange={(e) => setCommentText(e.target.value)}
                required
              ></textarea>
              <br />
              <input
                type="submit"
                className="btn btn-outline-info"
                value="Add Comment"
              />
            </form>
          </>
        ) : (
          <div>
            <Link
              to={`login?next=${window.location.pathname}`}
              className="btn btn-outline-info"
            >
              Log in to vote this article!
            </Link>
          </div>
        )}
        <strong className="text-secondary">
          {number_of_votes} Vote{number_of_votes !== 1 ? "s" : ""}
        </strong>
        <FavoriteButton postId={post.id} csrf={csrftoken} />
      </div>
    </article>
  );
};

const PostDetailPage = ({ user, isAuthenticated }) => {
  const [postObj, setPostObj] = useState({
    post: {
      id: "",
      title: "Loading...",
      content: "",
      date_posted: "2023-12-07T16:17:10.742207+05:30",
      author: { username: "", profile: { image: "" } },
      votes: "",
      favourites: "",
    },
    number_of_votes: "",
    post_is_voted: "voted",
    comments: [],
  });
  const queryParam = useParams().id;

  // Function to get a cookie value by name
  const getCookie = (name) => {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(";").shift();
  };
  const csrftoken = getCookie("csrftoken");
  useEffect(() => {
    if (isNaN(parseInt(queryParam))) {
      return;
    }
    // Extract post ID from the current URL
    let postId = queryParam;
    console.log(postId);
    // Get the CSRF token from the Django cookie
    fetch(`/api/post/${postId}/`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
    }).then((response) => {
      if (response.status === 200) {
        response.json().then((data) => {
          console.log(data);
          setPostObj(data);
        });
      }
    });
  }, [queryParam]);
  if (isNaN(parseInt(queryParam))) {
    window.location.href = "/";
  }
  return (
    <Base>
      <PostDetail
        post={postObj.post}
        user={user}
        isAuthenticated={isAuthenticated}
        postIsVoted={postObj.post_is_voted}
        comments={postObj.comments}
        number_of_votes={postObj.number_of_votes}
        csrftoken={csrftoken}
      ></PostDetail>
    </Base>
  );
};

export { PostDetailPage };
