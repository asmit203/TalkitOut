import React, { useEffect, useState } from "react";
import { Base } from "./base";

/*eslint no-extend-native: ["error", { "exceptions": ["String"] }]*/
const hashCode = async function (s) {
  // encode as UTF-8
  const msgBuffer = new TextEncoder().encode(s);

  // hash the message
  const hashBuffer = await crypto.subtle.digest("SHA-256", msgBuffer);

  // convert ArrayBuffer to Array
  const hashArray = Array.from(new Uint8Array(hashBuffer));

  // convert bytes to hex string
  const hashHex = hashArray
    .map((b) => b.toString(16).padStart(2, "0"))
    .join("");
  return hashHex;
};
// Post component
const Post = ({ post }) => (
  <article className="media content-section">
    <div className="media-body">
      <div className="article-metadata">
        <img
          className="rounded-circle article-img"
          src={post.author.profile.image}
          alt="Author"
        />
        <a className="mr-2" href={`/user/${post.author.username}`}>
          {post.author.username}
        </a>
        <small className="text-muted">
          {new Date(post.date_posted).toLocaleString()}
        </small>
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
      <strong className="text-secondary">{`${post.votes.length} Vote${
        post.votes.count !== 1 ? "s" : ""
      }`}</strong>
    </div>
  </article>
);
// PostsList component
const PostsList = ({ posts }) => (
  <div>
    {posts.map((post) => (
      <Post key={post.id} post={post} />
    ))}
  </div>
);

// Pagination component
const Pagination = ({ pageObj }) => (
  <div>
    {pageObj.has_previous && (
      <>
        <a className="btn btn-outline-info mb-4" href="?page=1">
          First
        </a>
        <a
          className="btn btn-outline-info mb-4"
          href={`?page=${pageObj.previous_page_number}`}
        >
          Previous
        </a>
      </>
    )}
    {pageObj.paginator.page_range.map((num) => (
      <React.Fragment key={num}>
        {pageObj.number === num ? (
          <a className="btn btn-info mb-4" href={`?page=${num}`}>
            {num}
          </a>
        ) : (
          num > pageObj.number - 3 &&
          num < pageObj.number + 3 && (
            <a className="btn btn-outline-info mb-4" href={`?page=${num}`}>
              {num}
            </a>
          )
        )}
      </React.Fragment>
    ))}
    {pageObj.has_next && (
      <>
        <a
          className="btn btn-outline-info mb-4"
          href={`?page=${pageObj.next_page_number}`}
        >
          Next
        </a>
        <a
          className="btn btn-outline-info mb-4"
          href={`?page=${pageObj.paginator.num_pages}`}
        >
          Last
        </a>
      </>
    )}
  </div>
);

// FriendsList component
const FriendsList = ({ friends, friendsLastSeen, currentUser }) => {
  useEffect(() => {
    async function getChatRooms() {
      for (let i = 0; i < friends.length; i++) {
        friends[i]["chatroom"] = await hashCode(
          currentUser.email < friends[i].friend.email
            ? currentUser.email + "_" + friends[i].friend.email
            : friends[i].friend.email + "_" + currentUser.email
        );
      }
    }
    getChatRooms();
    console.log(friends);
  }, [friends, currentUser]);
  return (
    <div className="content-section">
      <h3>Friends</h3>
      <p>Checkout your friends and continue your conversations.</p>
      <ul className="list-group">
        {friends.map((friend) => {
          return (
            <li
              key={friend.friend.username}
              className="list-group-item list-group-item-light"
            >
              <a href={"http://localhost:8000/chat/" + friend.chatroom}>
                {friend.friend.username}
              </a>{" "}
              - Last Seen:
              {friendsLastSeen.map(
                (lastseen) =>
                  lastseen.username === friend.friend.username && (
                    <span key={lastseen.username}>
                      {new Date(lastseen.lastseen).toLocaleString()}
                    </span>
                  )
              )}
            </li>
          );
        })}
      </ul>
    </div>
  );
};

// GroupList component
const GroupList = ({ groups, isAuthenticated }) => {
  return (
    <div className="content-section">
      <h3>Your Groups</h3>
      <p>Chat with your friends at once.</p>
      <div className="text-center">
        {isAuthenticated && (
          <a href="http://localhost:8000/api/create_group">Create Group</a>
        )}
      </div>
      <ul className="list-group">
        {groups.map((group) => (
          <li
            key={group.name}
            className="list-group-item list-group-item-light"
          >
            <a href={"http://localhost:8000/chat/" + encodeURIComponent(btoa(group.name))}>
              {group.name}
            </a>
          </li>
        ))}
      </ul>
    </div>
  );
};

// OtherList component
const OtherList = ({ othersList, currentUser }) => (
  <div className="content-section">
    <h3>Add Friends</h3>
    <p>Make new friends and start new conversations.</p>
    <ul className="list-group">
      {othersList.map((other) => {
        return (
          <li
            key={other.username}
            className="list-group-item list-group-item-light"
          >
            {/* {other.username < currentUser.username ? (
              <a href={"http://localhost:8000/chat/" + roomName}>
                {other.username}
              </a>
            ) : (
              <a
                href={"http://localhost:8000/api/add_friend/" + other.username}
              >
                {other.username}
              </a>
            )} */}
            <a href={"http://localhost:8000/api/add_friend/" + other.username}>
              {other.username}
            </a>
          </li>
        );
      })}
    </ul>
  </div>
);

const HomePage = ({ user }) => {
  const [homePosts, setHomePosts] = useState([]);
  const [friends, setFriends] = useState([]);
  const [others, setOthers] = useState([]);
  const [groups, setGroups] = useState([]);
  const [friendsLastSeen, setFriendsLastSeen] = useState([]);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  useEffect(() => {
    fetch("/api/is_authenticated").then(async (response) => {
      if (response.status === 200) {
        response.text().then((data) => {
          console.log("ISAUTH:", data);
          setIsAuthenticated(data === "true");
        });
      }
    });
  }, []);
  useEffect(() => {
    fetch("api/home_posts").then(async (response) => {
      if (response.status === 200) {
        response.json().then((data) => {
          console.log(data);
          setHomePosts(data);
        });
      }
    });
  }, []);

  useEffect(() => {
    if (isAuthenticated) {
      fetch("api/friends").then(async (response) => {
        if (response.status === 200) {
          response.json().then((data) => {
            console.log(data);
            setFriends(data);
          });
        }
      });
      fetch("api/friends_last_seen").then(async (response) => {
        if (response.status === 200) {
          response.json().then((data) => {
            console.log(data);
            setFriendsLastSeen(data);
          });
        }
      });
      fetch("api/groups").then(async (response) => {
        if (response.status === 200) {
          response.json().then((data) => {
            console.log(data);
            setGroups(data);
          });
        }
      });

      fetch("api/others").then(async (response) => {
        if (response.status === 200) {
          response.json().then((data) => {
            console.log(data);
            setOthers(data);
          });
        }
      });
    }
  }, [isAuthenticated]);

  return (
    <Base
      friends={friends}
      friendsLastSeen={friendsLastSeen}
      groupsList={groups}
      othersList={others}
    >
      <PostsList posts={homePosts}></PostsList>
    </Base>
  );
};

export { HomePage, PostsList, Pagination, FriendsList, GroupList, OtherList };
