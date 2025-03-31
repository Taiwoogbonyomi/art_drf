# Art

## project goals
This project provides a Django Rest Framework API for the [ArtConnect React web app](https://arts-8a67ad6d4259.herokuapp.com/).

The primary goal of ArtConnect is:
1) Provide a Platform for Artists to showcase their artwork and creative processes.
2) Enable users to share art-related posts, updates, and inspirations.
3) Facilitate artist meetups, workshops, and online collaborations.
4) Encourage meaningful interactions through discussions and event sharing.

## Table of contents
- [Art_Drf](#art_drf)
  * [Project goals](#project-goals)
  * [Table of contents](#table-of-contents)
  * [Planning](#planning)
    + [Data models](#data-models)
      - [**Home**](#--home--)
      - [**Profile**](#--profile--)
      - [**Post**](#--post--)
      - [**Comments**](#--Comments--)
    + [**Category**](#--category--)
    + [**Followers**](#--followers--)
  * [API endpoints](#api-endpoints)
  * [Frameworks, libraries and dependencies](#frameworks--libraries-and-dependencies)
    + [django-cloudinary-storage](#django-cloudinary-storage)
    + [dj-allauth](#dj-allauth)
    + [dj-rest-auth](#dj-rest-auth)
    + [djangorestframework-simplejwt](#djangorestframework-simplejwt)
    + [dj-database-url](#dj-database-url)
    + [psychopg2](#psychopg2)
    + [python-dateutil](#python-dateutil)
    + [django-recurrence](#django-recurrence)
    + [django-filter](#django-filter)
    + [django-cors-headers](#django-cors-headers)
     * [Testing](#testing)
    + [Manual testing](#manual-testing)
    + [Automated tests](#automated-tests)
    + [Python validation](#python-validation)


  ### Data models
This art blog is built around a structured database that allows users to share their artwork, engage with others through likes and comments, follow their favorite artists, and potentially join events. The models ensure that content is well-organized, interactive, and community-driven, fostering a dynamic art-sharing experience.

Data model schema were planned in parallel with the API endpoints, using an entity relationship diagram.

Custom models implemented for ArtConnect are:

#### **Profile Model**
Extends the built-in user model to store additional details about each user. Also helps personalize user accounts with avatars and bios.
The fields are:
- user: A one-to-one relationship with Django’s User model.

- bio: A text field allowing users to add a short description about themselves.

- avatar: An image field for profile pictures.

- location: An optional field for users to add their location.

- created_at: A timestamp that records when the profile was created.

#### **Post Model**
Represents a piece of art content shared by a user. Allows users to share their artwork and engage with others, supports likes and comments to encourage interaction.

its fields are:

- owner: A foreign key linking the post to the user who created it.

- title: A short, descriptive title for the artwork.

- content: A text field for an optional description or artist’s thoughts.

- image: The main image of the post, showcasing the artwork.

- category: A foreign key linking the post to a Category.

- likes_count: A counter that tracks the number of likes on the post.

- comments_count: A counter tracking the number of comments.

- created_at: A timestamp recording when the post was created.

- updated_at: A timestamp for tracking modifications.


#### **Category Model**
Groups posts into predefined categories based on the type of art. Helps organize artwork for better user experience and ensures posts are grouped under relevant themes.

its fields are:
- name: A unique name for the category (e.g., Portrait, Landscape, Digital Art).

- description: An optional text field describing the category.

- created_at: A timestamp tracking when the category was created.

#### **Comment Model**
Enables users to interact with posts by leaving comments. Users can interact with posts through feedback and discussions.

its fields are:
- owner: A foreign key linking the comment to the user who wrote it.

- post: A foreign key linking the comment to the related post.

- content: The text body of the comment.

- parent: A self-referential field that allows comments to be replies to other comments (nested comments).

- created_at: A timestamp tracking when the comment was made.

- updated_at: A timestamp for tracking comment edits.

#### **Like Model**
Tracks user likes on posts and comments to measure engagement and enhances the interactive experience of the platform.

its fields are:
- owner: A foreign key linking the like to the user who made it.

- post: A foreign key linking the like to a specific post (if applicable).

- comment: A foreign key linking the like to a specific comment (if applicable).

- created_at: A timestamp recording when the like was made.

#### **Follower Model**
Manages the relationships between users, allowing them to follow each other. It prevents self-following and duplicate follows through validation.

its fields are:
- owner: A foreign key linking the follower to the user who is following.

- followed: A foreign key linking the user being followed.

- created_at: A timestamp tracking when the follow action occurred.

##
# API Endpoints

## **User & Authentication**
| Method | Endpoint | Description |
|--------|---------|-------------|
| `POST` | `/api/auth/register/` | Register a new user |
| `POST` | `/api/auth/login/` | Log in a user |
| `POST` | `/api/auth/logout/` | Log out the current user |
| `GET`  | `/api/auth/user/` | Retrieve the currently logged-in user |
| `PUT`  | `/api/auth/user/update/` | Update user profile details |
| `DELETE` | `/api/auth/user/delete/` | Delete a user account |

## **Profile Management**
| Method | Endpoint | Description |
|--------|---------|-------------|
| `GET`  | `/api/profiles/` | Get a list of all user profiles |
| `GET`  | `/api/profiles/{id}/` | Retrieve a specific user profile |
| `PUT`  | `/api/profiles/{id}/edit/` | Edit a user's profile |
| `PUT`  | `/api/profiles/{id}/avatar/` | Update profile avatar |
| `GET`  | `/api/profiles/{id}/followers/` | Get followers of a specific profile |

## **Posts**
| Method | Endpoint | Description |
|--------|---------|-------------|
| `GET`  | `/api/posts/` | Get a list of all posts |
| `POST` | `/api/posts/create/` | Create a new post |
| `GET`  | `/api/posts/{id}/` | Retrieve a specific post |
| `PUT`  | `/api/posts/{id}/edit/` | Update a post |
| `DELETE` | `/api/posts/{id}/delete/` | Delete a post |

## **Categories**
| Method | Endpoint | Description |
|--------|---------|-------------|
| `GET`  | `/api/categories/` | Get a list of all categories |
| `POST` | `/api/categories/create/` | Create a new category |
| `GET`  | `/api/categories/{id}/` | Retrieve a specific category |
| `PUT`  | `/api/categories/{id}/edit/` | Update a category |
| `DELETE` | `/api/categories/{id}/delete/` | Delete a category |

## **Comments**
| Method | Endpoint | Description |
|--------|---------|-------------|
| `GET`  | `/api/comments/` | Get all comments |
| `POST` | `/api/comments/create/` | Create a new comment |
| `GET`  | `/api/comments/{id}/` | Retrieve a specific comment |
| `PUT`  | `/api/comments/{id}/edit/` | Edit a comment |
| `DELETE` | `/api/comments/{id}/delete/` | Delete a comment |

## **Likes**
| Method | Endpoint | Description |
|--------|---------|-------------|
| `GET`  | `/api/likes/` | Get all likes |
| `POST` | `/api/likes/create/` | Like a post or comment |
| `DELETE` | `/api/likes/{id}/delete/` | Remove a like |

## **Follow/Unfollow**
| Method | Endpoint | Description |
|--------|---------|-------------|
| `GET`  | `/api/follows/` | Get all follow relationships |
| `POST` | `/api/follows/create/` | Follow a user |
| `DELETE` | `/api/follows/{id}/delete/` | Unfollow a user |

# Database Schema

### Explanations of Relationships
- Users & Posts: A user can create many posts (One-to-Many).

- Users & Comments: A user can comment on many posts (One-to-Many).

- Users & Likes: A user can like many posts (One-to-Many).

- Users & Follows: Users can follow each other (Self-referential Many-to-Many).

- Posts & Comments: A post can have multiple comments (One-to-Many).

- Comments & CommentLikes: Users can like comments (One-to-Many).

- Users & Events: Users can host events (One-to-Many).

- Users & Event Registrations: Users can register for events (Many-to-Many through EventRegistration).