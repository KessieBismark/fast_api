from fastapi import FastAPI, Response, status, HTTPException
from typing import Optional

from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [
    {
        "title": "top coders",
        "content": "check",
        "published": True,
        "rating": '',
        "id": 6579
    },
    {
        "title": "top coders",
        "content": "check",
        "published": True,
        "rating": '',
        "id": 5365
    },
    {
        "title": "top coders",
        "content": "check",
        "published": True,
        "rating": '',
        "id": 6381
    },
    {
        "title": "top coders",
        "content": "check",
        "published": True,
        "rating": '',
        "id": 2830
    },
    {
        "title": "top coders",
        "content": "check",
        "published": True,
        "rating": '',
        "id": 4544
    }
]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


@app.get("/")
async def root():
    return {"message": "hello world "}


@app.get("/posts")
def get_post():
    return {"data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
# def create_post(payload: dict = Body(...)):   # this code retrieves data from user
# validating the data
def create_post(post: Post):  # this code retrieves data from user

    print(post)
    # to convert to a dictionary
    print(post.model_dump())
    # convert to dict nd add an id to it
    post_dict = post.model_dump()
    post_dict['id'] = randrange(0, 10000)
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    print(id)
    post = find_post(id)
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": "post with {id} not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")
    return {"data": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    if not index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if not index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")
    post_dict = post.model_dump()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data": my_posts}
