from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time 

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
 
while True:   
    try:
        conn = psycopg2.connect(host='localhost',database='fastapiDB',
                    user='postgres',password='shyampassword', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("DB Connection Success..")
        break
        
    except Exception as e:
        print("Connection Failed")
        print(e)
        time.sleep(2)

# my_posts = [
#     {
#         "title": "post 1",
#         "content": "content for post 1",
#         "id": 1
#     },
#     {
#         "title": "post 2",
#         "content": "content for post 2",
#         "id": 2
#     },
#     {
#         "title": "post 3",
#         "content": "content for post 3",
#         "id": 3
#     },
# ]

# def find_post(ID):
#     for post in my_posts:
#         if post['id'] == ID:
#             return post
  
@app.get("/posts")
def get_posts():
    cursor.execute('''SELECT * FROM posts''')
    posts = cursor.fetchall()
    return {"data": posts}
    

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute('''INSERT INTO posts (title, content, published) 
                      VALUES (%s,%s,%s) RETURNING * ''',(post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}

        
@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute('''SELECT * FROM posts WHERE id = %s''', (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")
    return {"data": post}
    

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute('''DELETE FROM posts WHERE id = %s RETURNING *''', (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute('''UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *''', (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")
    conn.commit()
    return {"data": updated_post}
    
    
    

    