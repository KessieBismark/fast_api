from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func

from ..schemes import PostBase as Post, PostData, PostOut
from typing import List, Optional
from sqlalchemy.orm import Session
from .. import models, oauth2
from ..dbconfig import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Post']  # for the docs UI to tag each api
)


@router.get("/sqldb")
def test_posts(db: Session = Depends(get_db)):
    post = db.query(models.Post).all()
    return post


# , response_model=PostData // helps you to return the data that you only want to return


@router.get("/", response_model=List[PostOut])
# @router.get("/")
async def root(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10,
               skip: int = 0, search: Optional[str] = ""):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # print(posts)
    # post = db.query(models.Post).all()
    post = db.query(models.Post).filter(
        models.Post.owner_id == str(current_user.id)).filter(
        models.Post.title.contains(search)).limit(
        limit).offset(skip).all()

    results = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(
        models.Votes, models.Votes.post_id == int(
            models.Post.id), isouter=True).group_by(models.Post.id).filter(
        models.Post.owner_id == str(current_user.id)).filter(
        models.Post.title.contains(search)).limit(
        limit).offset(skip).all()

    return results


@router.get("/", response_model=List[PostData])
def get_post(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()

    post = db.query(models.Post).all()
    print(post)
    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostData)
# def create_post(payload: dict = Body(...)):   # this code retrieves data from user
# validating the data
def create_post(post: Post, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):  # this code retrieves data from user
    print(current_user)
    # print(post)
    # # to convert to a dictionary
    # print(post.model_dump())
    # # convert to dict nd add an id to it
    # post_dict = post.model_dump()
    # post_dict['id'] = randrange(0, 10000)
    # my_posts.routerend(post_dict)

    # cursor.execute("""
    #     INSERT INTO posts (title, content, published)
    #     VALUES (%s, %s, %s)
    #     RETURNING *
    # """, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)

    # other way
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # print(id)
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (id,))
    # new_post = cursor.fetchone()
    # print(new_post)
    # print(id)
    # post = find_post(id)
    new_post = db.query(models.Post).filter(models.Post.id == id).first()  # .all()  for pulling more than one

    results = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(
        models.Votes, models.Votes.post_id == int(
            models.Post.id), isouter=True).group_by(
        models.Post.id).filter(models.Post.id == id).first()

    if not new_post:

        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": "post with {id} not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")
    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""delete FROM posts WHERE id = %s returning *""", (id,))
    # new_post = cursor.fetchone()
    # conn.commit()
    # print(new_post)
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    # index = find_index_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform action")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=PostData)
def update_post(id: int, post: Post, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""Update  posts set title= %s, published= %s, content= %s WHERE id = %s returning *""",
    #                (post.title, post.published, post.content, id))
    # new_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_posts = post_query.first()
    if not updated_posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")

    if updated_posts.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform action")

    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()
