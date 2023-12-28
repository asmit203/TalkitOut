import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import ThemeToggleButton from "./theme";
import { FriendsList, GroupList, OtherList } from "./home";
import { Chatbot } from "./chatbot";

const Header = ({ user, isAuthenticated }) => {
  return (
    <header className="site-header">
      <nav className="navbar navbar-expand-md navbar-dark bg-steel fixed-top">
        <div className="container">
          <Link className="navbar-brand mr-4" to="/">
            TalkitOut
          </Link>
          <button
            className="navbar-toggler"
            type="button"
            data-toggle="collapse"
            data-target="#navbarToggle"
            aria-controls="navbarToggle"
            aria-expanded="false"
            aria-label="Toggle navigation"
          >
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse" id="navbarToggle">
            <div className="navbar-nav mr-auto">
              <Link className="nav-item nav-link" to="/">
                Home
              </Link>
              <Link className="nav-item nav-link" to="/about">
                About
              </Link>
              <Link className="nav-item nav-link" to="/favourites">
                Favourites
              </Link>
              <Link
                className="nav-item nav-link"
                to="http://localhost:8000/whiteboardcollab/"
              >
                Whiteboard
              </Link>
              {isAuthenticated && (
                <Link
                  className="nav-item nav-link"
                  to={`http://localhost:8000/stream/user/${user.username}`}
                >
                  File Transfer
                </Link>
              )}
            </div>
            <div className="navbar-nav">
              {isAuthenticated ? (
                <>
                  <Link
                    className="nav-item nav-link"
                    to="http://localhost:8000/api/post/new/"
                  >
                    New Post
                  </Link>
                  <Link
                    className="nav-item nav-link"
                    to="http://localhost:8000/profile"
                  >
                    Profile
                  </Link>
                  <Link
                    className="nav-item nav-link"
                    to="http://localhost:8000/logout"
                  >
                    Logout
                  </Link>
                  <ThemeToggleButton></ThemeToggleButton>
                </>
              ) : (
                <>
                  <Link
                    className="nav-item nav-link"
                    to="http://localhost:8000/login"
                  >
                    Login
                  </Link>
                  <Link
                    className="nav-item nav-link"
                    to="http://localhost:8000/register"
                  >
                    Register
                  </Link>
                  <ThemeToggleButton></ThemeToggleButton>
                </>
              )}
            </div>
          </div>
        </div>
      </nav>
    </header>
  );
};

const Sidebar = ({ children, isAuthenticated }) => {
  return (
    <div className="col-md-4">
      <div className="content-section">
        <h3>Our Sidebar</h3>
        <p className="text-muted">
          You can put any information here you'd like.
        </p>
        <ul className="list-group">
          {isAuthenticated ? (
            <>
              <li className="list-group-item list-group-item-light">
                <Link to="/upvoted">Most Upvoted</Link>
              </li>
              <li className="list-group-item list-group-item-light">
                <Link to="http://localhost:8000/api/announcements">
                  Announcements
                </Link>
              </li>
            </>
          ) : (
            <>
              <li className="list-group-item list-group-item-light">
                Most Upvoted
              </li>
              <li className="list-group-item list-group-item-light">
                Announcements
              </li>
            </>
          )}
        </ul>
      </div>
      {children}
    </div>
  );
};

const Base = ({
  children,
  friends,
  friendsLastSeen,
  groupsList,
  othersList,
}) => {
  const [user, setUser] = useState("");
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    // Fetch user data or check authentication status
    // Update the 'user' state accordingly
    fetch("/api/current_user").then(async (response) => {
      if (response.status === 200) {
        response.json().then((data) => {
          console.log(data);
          setUser(data);
        });
      }
    });
    fetch("/api/is_authenticated").then(async (response) => {
      if (response.status === 200) {
        response.text().then((data) => {
          console.log("ISAUTH:", data);
          setIsAuthenticated(data === "true");
        });
      }
    });
  }, []);
  return (
    <>
      <Header user={user} isAuthenticated={isAuthenticated}></Header>
      <main role="main" className="container" style={{ marginTop: "5em" }}>
        <div className="row">
          <div className="col-md-8">
            {React.cloneElement(children, {
              user: user,
              isAuthenticated: isAuthenticated,
            })}
          </div>
          {friends && friendsLastSeen && groupsList && othersList ? (
            <Sidebar isAuthenticated={isAuthenticated}>
              <FriendsList
                friends={friends}
                friendsLastSeen={friendsLastSeen}
                currentUser={user}
              ></FriendsList>
              <GroupList
                groups={groupsList}
                isAuthenticated={isAuthenticated}
              ></GroupList>
              <OtherList othersList={othersList} currentUser={user}></OtherList>
            </Sidebar>
          ) : (
            <Sidebar isAuthenticated={isAuthenticated}></Sidebar>
          )}
        </div>
      </main>
      <Chatbot></Chatbot>
    </>
  );
};

export { Base, Sidebar };
