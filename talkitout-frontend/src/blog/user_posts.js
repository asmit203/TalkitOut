import React, { useEffect, useState } from "react";
import { Base } from "./base";
import { useParams, useSearchParams } from "react-router-dom";

const PostList = ({ username }) => {
  const [posts, setPosts] = useState([]);
  const [pageObj, setPageObj] = useState({ paginator: { count: 0 } });
  const [isPaginated, setIsPaginated] = useState(false);
  const [searchParams, setSearchParams] = useSearchParams();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(
          `/api/user/${username}?page=${searchParams.get("page") || 1}`
        );
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }

        const data = await response.json();
        setPosts(data.results);
        data.page_range = Array.from(
          { length: Math.ceil(data.count / 5) },
          (_, index) => index + 1
        );
        data.number = parseInt(searchParams.get("page") || 1);
        console.log(data);

        setPageObj(data);
        setIsPaginated(data.count > 5);
        // setIsPaginated(data.length > 0 && "page" in data[0]); // Adjust based on your API response structure
        // setPageObj(data[0]?.page); // Assuming the page information is included in the first item
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, [username, searchParams]);

  return (
    <div>
      <h1 className="mb-3">
        Posts by {username} ({pageObj.count})
      </h1>
      {posts.map((post) => (
        <article key={post.id} className="media content-section">
          <div className="media-body">
            <div className="article-metadata">
              <img
                className="rounded-circle article-img"
                src={post.author.profile.image}
                alt={`${post.author.username}'s profile`}
              />
              <a className="mr-2" href={`/user/${post.author.username}`}>
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
            />
          </div>
        </article>
      ))}
      {isPaginated && (
        <div>
          {pageObj.previous && (
            <>
              <a className="btn btn-outline-info mb-4" href="?page=1">
                First
              </a>
              <a
                className="btn btn-outline-info mb-4"
                href={`?page=${pageObj.previous.split("=")[1] || 1}`}
              >
                Previous
              </a>
            </>
          )}
          {pageObj.page_range.map((num) => (
            <React.Fragment key={num}>
              {pageObj.number === num && (
                <a className="btn btn-info mb-4" href={`?page=${num}`}>
                  {num}
                </a>
              )}
              {num > pageObj.number - 3 &&
                num < pageObj.number + 3 &&
                pageObj.number !== num && (
                  <a
                    className="btn btn-outline-info mb-4"
                    href={`?page=${num}`}
                  >
                    {num}
                  </a>
                )}
            </React.Fragment>
          ))}
          {pageObj.next && (
            <>
              <a
                className="btn btn-outline-info mb-4"
                href={`?page=${pageObj.next.split("=")[1]}`}
              >
                Next
              </a>
              <a
                className="btn btn-outline-info mb-4"
                href={`?page=${Math.ceil(pageObj.count / 5)}`}
              >
                Last
              </a>
            </>
          )}
        </div>
      )}
    </div>
  );
};

const UserPosts = ({ user, isAuthenticated }) => {
  const queryParam = useParams().username;

  return (
    <Base>
      <PostList username={queryParam}></PostList>
    </Base>
  );
};
export { UserPosts };
