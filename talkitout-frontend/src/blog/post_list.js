import React from "react";

const PostDetail = ({ object }) => {
  return (
    <article className="media content-section">
      <div className="media-body">
        <div className="article-metadata">
          <img
            className="rounded-circle article-img"
            src={object.author.profile.image}
            alt={`${object.author.username}'s profile`}
          />
          <a className="mr-2" href="#">
            {object.author}
          </a>
          <small className="text-muted">{object.date_posted}</small>
        </div>
        <h2 className="article-title">{object.title}</h2>
        <p
          className="article-content"
          dangerouslySetInnerHTML={{ __html: object.content }}
        />
      </div>
    </article>
  );
};

export default PostDetail;
