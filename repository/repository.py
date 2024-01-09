from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorCollection

from utils.mongo_utils import get_db_collection, get_filter, map
from models.models import User, Tweet
from models.models import UserUpdate, TweetUpdate


class Repository:
    _db_collections: list[AsyncIOMotorCollection]

    def __init__(self, db_collections: list[AsyncIOMotorCollection]):
        self._db_collections = db_collections


#User
    async def create(self, user: User) -> str:
        insert_result = await self._db_collections[1].insert_one(dict(user))
        return str(insert_result.inserted_id)

    async def get_all(self, collection: int) -> list[Tweet] | list[User]: # вся коллекция
        db = []
        async for obj in self._db_collections[collection].find():
            db.append(map(obj, self._db_collections[collection].name))
        return db

    async def get_by_id(self, id: str, collection: int) -> User | Tweet | None:
        print(f'Get {id} from {collection}')
        obj = await self._db_collections[collection].find_one(get_filter(id))
        return map(obj, self._db_collections[collection].name)

    async def update(self, id: str, obj, collection: int) -> User | Tweet | None:
        updated_obj = await self._db_collections[collection].find_one_and_replace(get_filter(id), dict(obj))
        return map(updated_obj, collection=str(collection))

    

    #MakeTweet
    async def create_tweet(self, post: Tweet) -> str:
        u = await self._db_collections[0].find_one(get_filter(post.user_id))

        u = map(u, self._db_collections[0])
        print(u)
        user_upd = UserUpdate(username=u.username, email=u.email, posts=u.posts)
        

        insert_result = await self._db_collections[0].insert_one(dict(post))

        if (user_upd.posts != None):
            user_upd.posts.append(str(insert_result.inserted_id))
        else:
            user_upd.posts = [str(insert_result.inserted_id)]
        
        updated_obj = await self._db_collections[0].find_one_and_replace(get_filter(post.user_id), dict(user_upd))
        
        return str(insert_result.inserted_id)



    async def delete_user(self, id: str) -> User | Tweet | None:
        db = map(await self._db_collections[0].find_one_and_delete(get_filter(id)), self._db_collections[0].name)
        return db
    
    async def delete_tweet(self, id: str) -> User | Tweet| None:
        db = map(await self._db_collections[0].find_one_and_delete(get_filter(id)), self._db_collections[1])
        return db


    @staticmethod
    async def get_instance(db_collections: list[AsyncIOMotorCollection] = Depends(get_db_collection)):
        db_coll = db_collections # await get_db_collection()
        r = Repository(db_coll)
        return r