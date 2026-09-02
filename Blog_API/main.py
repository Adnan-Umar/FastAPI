from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import engine, SessionLocal
import models, schemas
from auth import create_token, verify_token

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()

# Login API
@app.post("/login")
def login():
    return{
        "access_token":create_token({"user":"admin"}),
        "token_type": "bearer"
    }

# Home route
@app.get("/")
def home():
    return {
        "message": "Blog API Started"
    }

# Create blog (Protected)
@app.post("/blogs", response_model=schemas.BlogResponse)
def create_blog(blog: schemas.BlogCreate, db:Session = Depends(get_db), user = Depends(verify_token)):
    new_blog = models.Blog(
        title = blog.title,
        content = blog.content
    )

    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog

# Read all blogs
@app.get("/blogs", response_model=list[schemas.BlogResponse])
def get_blogs(page: int = 1,
             limit: int = 5,
             search: str = Query(default=""),
            db:Session = Depends(get_db)):
    query = db.query(models.Blog)

    if search:
        query = query.filter(models.Blog.title.like(f"%{search}"))

    total = query.count()
    start = (page - 1) * limit
    blogs = query.offset(start).limit(limit).all()

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "data": blogs
    }

# Read one blog
@app.get("/blogs/{id}", response_model=schemas.BlogResponse)
def get_blog(id:int, db:Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        raise HTTPException(
            status_code=404,
            detail=f"Blog not found with id: {id}"
        )

    return blog

# Update blog api (Protected)
@app.put("/blogs/{id}", response_model=schemas.BlogResponse)
def update_blog(id:int,blog:schemas.BlogCreate, db:Session = Depends(get_db), user = Depends(verify_token)):
    exiisting_blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not exiisting_blog:
        raise HTTPException(
            status_code=404,
            detail=f"Blog not found with id: {id}"
        )
    
    exiisting_blog.title = blog.title
    exiisting_blog.content = blog.content

    db.commit()
    db.refresh(exiisting_blog)

    return exiisting_blog

# Delete blog api (Protected)
@app.delete("/blogs/{id}")
def delete_blog(id:int, db:Session = Depends(get_db), user = Depends(verify_token)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(
            status_code=404,
            detail=f"Blog not found with id: {id}"
        )

    blog.delete()
    db.commit()

    return {
        "message": "Blog deleted Successfully"
    }