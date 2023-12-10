
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import os
import uuid
from db2 import UserDB


app = FastAPI(title='User Registration with 2 databases', version='0.0.1')
server_url = '***'
# Ex server_url = 'http://localhost:7000'

@app.get('/ping')
def ping():
    return {'ping': 'pong'}

@app.post('/register')
def register_user(
        full_name: str,
        email: str,
        password: str,
        phone: str,
        profile_picture: UploadFile = File(...)
    ):
    file_name = profile_picture.filename
    profile_picture = profile_picture.file.read()
    user_id = str(uuid.uuid4())
    user_db = UserDB()
    resp = user_db.add_user(full_name, email, password, phone, user_id, profile_picture, file_name)
    return resp

@app.get('/get_user')
def get_user(email: str, password: str):
    user_db = UserDB()
    resp = user_db.get_user(email, password)
    return resp


@app.get("/get_image/{user_id}/{image_name}")
def get_image(user_id: str, image_name: str):
    file_path = os.path.join(os.getcwd(), image_name)
    response = FileResponse(file_path, media_type='image/jpg', filename=image_name, headers={'content-type': 'image/jpg'})
    return response



if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=7000)