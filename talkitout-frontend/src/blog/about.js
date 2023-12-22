import React, { useEffect, useState } from "react";
import { Base } from "./base";

const FavoritesList = ({ favorites }) => {
  return (
    <div>
      <h1>Favourites</h1>
      {favorites.map((post) => (
        <article key={post.id} className="media content-section">
          <div className="media-body">
            <div className="article-metadata">
              <img
                className="rounded-circle article-img"
                src={post.author.profile.image}
                alt="Author"
              />
              <a className="mr-2" href={`/user-posts/${post.author.username}`}>
                {post.author.username}
              </a>
              <small className="text-muted">{post.date_posted}</small>
            </div>
            <h2>
              <a className="article-title" href={`/post/${post.id}`}>
                {post.title}
              </a>
            </h2>
            <p
              className="article-content"
              dangerouslySetInnerHTML={{ __html: post.content }}
            ></p>
            <strong className="text-secondary">
              {post.votes.count} Vote{post.votes.count !== 1 && "s"}
            </strong>
          </div>
        </article>
      ))}
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
      <h1>Blog About!</h1>
    </Base>
  );
};
export { AboutPage };
