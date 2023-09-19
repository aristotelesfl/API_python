from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
import uuid
app = FastAPI()

SECRET = str(uuid.uuid4())

manager = LoginManager(SECRET, '/login')

DB = {
    'user':{
        'turma_api@gmail.com':{
            'name': 'super módulo',
            'password': '1234'
        }
    }
}

@manager.user_loader()
def query_user(user_id: str):
    return DB['user'].get(user_id)

@app.post('/login')
def login(data: OAuth2PasswordRequestForm = Depends()):
    email = data.username
    password = data.password

    user = query_user(email)

    if not user:
        raise InvalidCredentialsException
    elif password != user['password']:
        raise InvalidCredentialsException

    acess_token = manager.create_access_token(
        data={'sub': email}
    )
    return {'acess_token': acess_token}

@app.get('/protected')
def protected_rout(user = Depends(manager)):
    print(user)
    return {"user": user}