from datetime import date, datetime
from typing import Optional
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


app = FastAPI(
    title="FastAPI CRUD REST API",
    description="Simple in-memory CRUD API for blog posts.",
    version="1.0.0",
)


posts: list[dict] = []


class Post(BaseModel):
    id: Optional[str] = None
    title: str = Field(..., min_length=1, examples=["My first post"])
    author: str = Field(..., min_length=1, examples=["Osmar"])
    content: str = Field(..., min_length=1, examples=["FastAPI makes APIs quick to build."])
    created_at: Optional[date] = None
    published_at: Optional[datetime] = None
    published: bool = False


@app.get("/")
def read_root():
    return {"message": "FastAPI CRUD REST API is running"}


@app.get("/posts")
def get_posts():
    return posts


@app.post("/posts")
def create_post(post: Post):
    post.id = str(uuid4())
    post.created_at = date.today()
    post.published_at = datetime.now() if post.published else None

    post_dict = post.model_dump()
    posts.append(post_dict)
    return post_dict


@app.get("/posts/{post_id}")
def get_post(post_id: str):
    for post in posts:
        if post["id"] == post_id:
            return post

    raise HTTPException(status_code=404, detail="Post not found")


@app.put("/posts/{post_id}")
def update_post(post_id: str, updated_post: Post):
    for index, post in enumerate(posts):
        if post["id"] == post_id:
            updated_post.id = post_id
            updated_post.created_at = post["created_at"]
            updated_post.published_at = datetime.now() if updated_post.published else None

            post_dict = updated_post.model_dump()
            posts[index] = post_dict
            return post_dict

    raise HTTPException(status_code=404, detail="Post not found")


@app.delete("/posts/{post_id}")
def delete_post(post_id: str):
    for index, post in enumerate(posts):
        if post["id"] == post_id:
            deleted_post = posts.pop(index)
            return {"message": "Post deleted successfully", "post": deleted_post}

    raise HTTPException(status_code=404, detail="Post not found")
