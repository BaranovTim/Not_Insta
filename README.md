# NotInstagram

**NotInstagram** is a backend application developed for a photo-sharing social network. This project focuses on designing and implementing an API for uploading posts and their associated photos, as well as enabling users to comment on and like posts. The project is a practical application aimed at enhancing skills in API development and database integration, with potential use as a portfolio project.

The backend is powered by the **Django framework** in **Python**, and all data is managed using a **PostgreSQL database**.

## Key Features

### Posts
- Posts consist of text and a photo.
- The creation time of each post is stored.
- Posts can only be created by authorized users.
- Editing a post is restricted to its author.

### Comments
- Users can write comments on specific posts.
- Only authorized users can leave comments.
- Each comment includes text and the date it was created.

### Likes
- Users can react to posts by leaving a like.
- The total like count is displayed when viewing a post.

### API Design
- Endpoints and HTTP methods are carefully designed for ease of use and adherence to RESTful principles.

### Post Details
- Each post's details include its text, photo, and creation time.
- A list of associated comments is displayed with their content and creation dates.
- The like count for the post is also shown.

## Skills Developed
- Working with Django models for robust data representation.
- Implementing serializers to handle data input and output effectively.
- Designing RESTful APIs with endpoints and appropriate HTTP methods.
- Real-world application of backend development skills.

---
