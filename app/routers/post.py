from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List
from .. import models, schema, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/",response_model=List[schema.PostOut])
def get_posts(db: Session = Depends(get_db), 
            curr_user:int = Depends(oauth2.get_current_user),
            limit:int = 10, skip:int = 0,
            search: Optional[str] = ""):
    
    
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")) \
                            .join(models.Vote, models.Vote.post_id == models.Post.id, 
                                isouter=True).group_by(models.Post.id) \
                            .filter(models.Post.title.contains(search)) \
                                .limit(limit).offset(skip).all()
    return results

    # posts = db.query(models.Post).filter(models.Post.title.contains(search)) \
    #                             .limit(limit).offset(skip).all()
    # return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.PostResponse)
def create_posts(post: schema.CreatePost, 
                 db: Session = Depends(get_db), 
                 curr_user:int = Depends(oauth2.get_current_user)):
    
    new_post = models.Post(owner_id=curr_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
        
        
@router.get("/{id}", response_model=schema.PostOut)
def get_post(id: int, db: Session = Depends(get_db), curr_user:int = Depends(oauth2.get_current_user)):
    
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")) \
                            .join(models.Vote, models.Vote.post_id == models.Post.id, 
                                isouter=True).group_by(models.Post.id) \
                            .filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")
    
    return post
    

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), curr_user:int = Depends(oauth2.get_current_user)):
    
    deleted_post_query = db.query(models.Post).filter(models.Post.id == id)
    deleted_post = deleted_post_query.first()
    if not deleted_post_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")
    
    if deleted_post.owner_id != curr_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete others posts")
    
    deleted_post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schema.PostResponse)
def update_post(id: int, post: schema.UpdatePost, db: Session = Depends(get_db), curr_user:int = Depends(oauth2.get_current_user)):
    
    updated_post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = updated_post_query.first()
    
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")
    
    if updated_post.owner_id != curr_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update others posts")
    
    updated_post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return updated_post_query.first()