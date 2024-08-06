from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, oauth2, schemes
from ..dbconfig import get_db


router = APIRouter(
    prefix="/vote",
    tags=['vote']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemes.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post_data = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist")
    vote_query = db.query(models.Votes).filter(
        models.Votes.post_id == vote.post_id, models.Votes.user_id == int(current_user.id))
    found_vote = vote_query.first()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already voted")
        new_vote = models.Votes(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "success"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="vote does not exist")

        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully deleted"}