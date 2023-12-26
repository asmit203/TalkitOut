import { HomePage } from "./blog/home";
import { PostDetailPage } from "./blog/post_detail";
import { FavouritesPage } from "./blog/favourites";
import { BrowserRouter, Form, Route, Routes } from "react-router-dom";
import { AnnouncementsPage } from "./blog/announcement";
import { DeletePostForm } from "./blog/post_confirm_delete";
import { UserPosts } from "./blog/user_posts";
import { UpvotedPosts } from "./blog/upvotedposts";
import { AboutPage } from "./blog/about";
import NotFound from "./404-page";

function App() {
  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/post/:id" element={<PostDetailPage />} />
          <Route path="/post/:id/delete/" element={<DeletePostForm />} />

          <Route path="/favourites/" element={<FavouritesPage />} />
          <Route path="/announcements/" element={<AnnouncementsPage />} />
          <Route path="/user/:username" element={<UserPosts />} />
          <Route path="/upvoted/" element={<UpvotedPosts />} />
          <Route path="/about/" element={<AboutPage />} />


          <Route path="*" element={<NotFound/>}/>
        </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;
