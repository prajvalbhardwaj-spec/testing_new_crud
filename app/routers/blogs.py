from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas
from app.auth import get_current_user

router = APIRouter(prefix="/blogs", tags=["Blogs"])


@router.post("/", response_model=schemas.BlogResponse, status_code=status.HTTP_201_CREATED)
def create_blog(
    payload: schemas.BlogCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    blog = models.Blog(
        title=payload.title,
        content=payload.content,
        author_id=current_user.id
    )
    db.add(blog)
    db.commit()
    db.refresh(blog)
    return blog


@router.get("/", response_model=List[schemas.BlogListResponse])
def list_blogs(db: Session = Depends(get_db)):
    return db.query(models.Blog).order_by(models.Blog.created_at.desc()).all()


@router.get("/{blog_id}", response_model=schemas.BlogResponse)
def get_blog(blog_id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog


@router.put("/{blog_id}", response_model=schemas.BlogResponse)
def update_blog(
    blog_id: int,
    payload: schemas.BlogUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    if blog.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this blog")

    if payload.title is not None:
        blog.title = payload.title
    if payload.content is not None:
        blog.content = payload.content

    db.commit()
    db.refresh(blog)
    return blog


@router.delete("/{blog_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(
    blog_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    if blog.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this blog")
    db.delete(blog)
    db.commit()
