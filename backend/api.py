import uvicorn
from fastapi import FastAPI, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from routers import auth, orders


api = FastAPI()
api.include_router(auth.router)
api.include_router(orders.router)


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

    class Config:
        orm_mode = True


class User(BaseModel):
    name: str

    class Config:
        orm_mode = True


@api.post("/token", response_model=Token)
async def login(form: OAuth2PasswordRequestForm = Depends()):
    """トークン発行"""
    user = auth.authenticate(form.username, form.password)
    return auth.create_tokens(user.id)


@api.get("/refresh_token", response_model=Token)
async def refresh_token(current_user: User = Depends(auth.get_current_user_with_refresh_token)):
    """リフレッシュトークンでトークンを再取得"""
    return auth.create_tokens(current_user.id)


@api.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(auth.get_current_user)):
    """ログイン中のユーザーを取得"""
    return current_user


@api.post("/orders/{user_name}")
async def get_orders(user_name: str, request: Request):
    # トークン取得
    token = request.cookies.get(user_name + "_token")
    # user id取得
    user_id = auth.get_current_user_id(token)
    # orders辞書取得
    user_orders = orders.get_orders(user_id)
    print("\n========== Debug ==========")
    print("APIサーバに送られてきたトークン: ")
    print(str(token))
    print("デコードしたトークンから、ユーザ名を抽出し、DBからユーザIDを入手: ")
    print(str(user_id))
    return user_orders


@api.get("/")
async def root():
    return {"api": "(￣▽￣)~*"}

if __name__ == '__main__':
    uvicorn.run(api, host="127.0.0.1", port=8008)
