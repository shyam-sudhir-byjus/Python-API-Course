from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import Optional, List
from .. import models, schema, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schema.Vote, 
         db: Session = Depends(get_db), 
         curr_user: int = Depends(oauth2.get_current_user)):
    
    post_check = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post_check:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail="Post doesn't exist")
    
    vote_query = db.query(models.Vote).filter(
                                models.Vote.post_id == vote.post_id, 
                                models.Vote.user_id == curr_user.id)
    found_vote = vote_query.first()
    
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                                detail=f"User {curr_user.id} already voted on {vote.post_id}")
        new_vote = models.Vote(post_id=vote.post_id, user_id=curr_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Added vote successfully"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail="Vote doesn't exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Deleted vote successfully"}