from fastapi import FastAPI, File, UploadFile, HTTPException 
from fastapi.responses import JSONResponse, FileResponse
import bson
import os
import uuid
from db1 import UserDB, image_db


app = FastAPI(title='User Registration with 2 databases', version='0.0.1')
server_url = 'http://localhost:7000'
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
    profile_picture = bson.Binary(profile_picture.file.read())
    user_id = str(uuid.uuid4())
    user_db = UserDB()
    resp = user_db.add_user(full_name, email, password, phone, user_id)
    if resp.get('status') != 'error':
        image_db.insert_one({
            'user_id': user_id,
            'image': profile_picture,
            'file_name': file_name
        })
    return resp

@app.get('/get_user')
def get_user(email: str, password: str):
    user_db = UserDB()
    resp = user_db.get_user(email, password)
    if resp.get('user_details') is not None:
        user_id = resp.get('user_details').get('user_id')
        image_data = image_db.find_one({'user_id': user_id})
        file_name = image_data.get('file_name')
        with open(file_name, 'wb') as f:
            f.write(image_data.get('image'))
        
        return JSONResponse({
            'user_details': resp.get('user_details'),
            'image_source': server_url + '/get_image/' + user_id + '/' + file_name
        })
        
    else:
        raise HTTPException(status_code=404, detail="User not found")


@app.get("/get_image/{user_id}/{image_name}")
def get_image(user_id: str, image_name: str):
    file_path = os.path.join(os.getcwd(), image_name)
    response = FileResponse(file_path, media_type='image/jpg', filename=image_name, headers={'content-type': 'image/jpg'})
    return response



if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=7000)