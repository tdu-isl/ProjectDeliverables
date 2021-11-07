from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt
from peewee import SqliteDatabase, Model, AutoField, CharField, TextField


router = APIRouter()

db = SqliteDatabase('backend/db/c.db')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(Model):
    id = AutoField(primary_key=True)
    name = CharField(100)
    password = CharField(100)
    refresh_token = TextField(null=True)

    class Meta:
        database = db


def authenticate(name: str, password: str):
    print("\n========== Debug ==========")
    print("認証開始")
    print("user name = " + name + ", password = " + password)
    user = User.get(name=name)
    if user.password != password:
        raise HTTPException(status_code=401, detail='パスワード不一致')
    print("認証できました")
    return user


def create_tokens(user_id: int):
    print("トークンを生成しています...")
    sss = 30
    print("有効期間を" + str(sss) + "秒間に設定しています")
    # ペイロード作成
    access_payload = {
        'token_type': 'access_token',
        'exp': datetime.utcnow() + timedelta(seconds=sss),
        'user_id': user_id,
    }
    refresh_payload = {
        'token_type': 'refresh_token',
        'exp': datetime.utcnow() + timedelta(days=90),
        'user_id': user_id,
    }

    # トークン作成
    access_token = jwt.encode(access_payload, 'SECRET_KEY123', algorithm='HS256')
    refresh_token = jwt.encode(refresh_payload, 'SECRET_KEY123', algorithm='HS256')

    # DBにリフレッシュトークンを保存
    User.update(refresh_token=refresh_token).where(User.id == user_id).execute()

    print("   生成した accessトークン：")
    print(access_token)
    print("   生成した refreshトークン：")
    print(refresh_token)

    return {'access_token': access_token, 'refresh_token': refresh_token, 'token_type': 'bearer'}


def get_current_user_from_token(token: str, token_type: str):
    # トークンをデコードしてペイロードを取得。有効期限と署名は自動で検証される。
    payload = jwt.decode(token, 'SECRET_KEY123', algorithms=['HS256'])

    # トークンタイプが一致することを確認
    if payload['token_type'] != token_type:
        raise HTTPException(status_code=401, detail=f'トークンタイプ不一致')

    # DBからユーザーを取得
    user = User.get_by_id(payload['user_id'])

    # リフレッシュトークンの場合、受け取ったものとDBに保存されているものが一致するか確認
    if token_type == 'refresh_token' and user.refresh_token != token:
        print(user.refresh_token, '¥n', token)
        raise HTTPException(status_code=401, detail='リフレッシュトークン不一致')

    return user


def get_current_user_id(token: str = Depends(oauth2_scheme)):
    u = get_current_user_from_token(token, 'access_token')
    return u.id


async def get_current_user(token: str = Depends(oauth2_scheme)):
    return get_current_user_from_token(token, 'access_token')


async def get_current_user_with_refresh_token(token: str = Depends(oauth2_scheme)):
    return get_current_user_from_token(token, 'refresh_token')
