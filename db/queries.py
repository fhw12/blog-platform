from db.models import Base, User, Post, Comment
from sqlalchemy import create_engine
from sqlalchemy import select, desc
from sqlalchemy.orm import Session
from hashlib import sha256

engine = create_engine('sqlite:///main.db')
Base.metadata.create_all(engine)


# user
def add_user(username: str, password: str, role: str):
    with Session(engine) as session:
        password_hash = sha256(password.encode()).hexdigest()
        session.add(
            User(
                username=username,
                password=password_hash,
                role=role,
            )
        )
        session.commit()
        session.close()


def get_users():
    with Session(engine) as session:
        return session.scalars(
            select(User)
        ).all()


def get_user_by_id(user_id: int):
    with Session(engine) as session:
        return session.scalar(
            select(User)
                .where(User.id == user_id)
        )


def get_user_by_username(username: str):
    with Session(engine) as session:
        return session.scalar(
            select(User)
                .where(User.username == username)
        )


def set_user_password_by_username(username: str, new_password: str):
    with Session(engine) as session:
        new_password_hash = sha256(new_password.encode()).hexdigest()
        user = session.scalar(
            select(User)
                .where(User.username == username)
        )
        user.password = new_password_hash
        session.commit()


# post
def add_post(title: str, content: str):
    with Session(engine) as session:
        session.add(
            Post(
                title=title,
                content=content,
            )
        )
        session.commit()


def get_posts():
    with Session(engine) as session:
        return session.scalars(
            select(Post).order_by(desc(Post.id))
        ).all()


def get_posts_on_page(page_id: int):
    max_posts_on_page = 4
    posts = get_posts()
    start_index = (page_id - 1) * max_posts_on_page
    end_index = start_index + max_posts_on_page
    return posts[start_index:end_index]


def get_number_of_pages():
    max_posts_on_page = 4
    posts = get_posts()
    return (len(posts) + max_posts_on_page - 1) // max_posts_on_page


def get_post_by_id(post_id: int):
    with Session(engine) as session:
        return session.scalar(
            select(Post)
                .where(Post.id == post_id)
        )


def delete_post_by_id(post_id: int):
    with Session(engine) as session:
        post =  session.scalar(
            select(Post)
                .where(Post.id == post_id)
        )
        session.delete(post)
        session.commit()


def update_post_by_id(post_id: int, title: str, content: str):
    with Session(engine) as session:
        post =  session.scalar(
            select(Post)
                .where(Post.id == post_id)
        )
        post.title = title
        post.content = content
        session.commit()


# comment
def add_comment(post_id: str, content: str, creator_id: int):
    with Session(engine) as session:
        session.add(
            Comment(
                postId=post_id,
                content=content,
                creatorId=creator_id,
            )
        )
        session.commit()


def get_comments_by_post_id(post_id: int):
    with Session(engine) as session:
        return session.scalars(
            select(Comment)
                .where(Comment.postId == post_id)
                .order_by(desc(Comment.id))
        ).all()


def delete_comment_by_id(comment_id: int):
    with Session(engine) as session:
        comment =  session.scalar(
            select(Comment)
                .where(Comment.id == comment_id)
        )
        session.delete(comment)
        session.commit()