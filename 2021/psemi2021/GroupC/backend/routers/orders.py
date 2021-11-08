from fastapi import APIRouter
from peewee import SqliteDatabase, Model, IntegerField, TextField


router = APIRouter()
db = SqliteDatabase('backend/db/c.db')


class Product(Model):
    pid = IntegerField(primary_key=True)
    name = TextField()
    price = IntegerField()
    stock = IntegerField()

    class Meta:
        database = db


class Orders(Model):
    oid = IntegerField(primary_key=True)
    id = IntegerField()
    pid = IntegerField()
    count = IntegerField()

    class Meta:
        database = db


def get_orders(user_id: int):
    dict = {}
    query = Orders.select().where(Orders.id == user_id)
    for order in query:
        product = Product.get(Product.pid == order.pid).name
        if product in dict.keys():
            dict[product] += order.count
        else:
            dict[product] = order.count
        
    return dict
