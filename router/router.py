from typing import Any

from bson import ObjectId
from fastapi import APIRouter, status, Depends
from pymemcache import HashClient
from starlette.responses import Response

from cache.memcached_utils import get_memcached_client
from repository.repository import Repository
from repository.search_repository import SearchStudentRepository
from models.models import User, Tweet
from models.models import UserUpdate, TweetUpdate

router = APIRouter()


@router.get("/")
async def root():

    return {"Hello": "World"}


@router.get("/user/all", tags=["User"])
async def get_all(repository: Repository = Depends(Repository.get_instance)) -> list[User] | list[Tweet]:
    return await repository.get_all(1)

@router.get("/tweet/all", tags=["tweet"])
async def get_all(repository: Repository = Depends(Repository.get_instance)) -> list[User] | list[Tweet]:
    return await repository.get_all(0)


@router.get("/debug_get/{collection}/{user_id}")
async def get(collection: int, user_id: str, repository: Repository = Depends(Repository.get_instance),
                                             memcached_client: HashClient = Depends(get_memcached_client)) -> User | Tweet:
    
    obj = await repository.get_by_id(id = user_id, collection = collection)
    return obj


@router.get("/user/filter", tags=["User"])
async def get_by_name(username: str, repository: SearchStudentRepository = Depends(SearchStudentRepository.get_instance)) -> Any:
    return await repository.find_by_username(username = username)


@router.get("/user/{user_id}", response_model=User, tags=["User"])
async def get_by_id(user_id: str,
                    repository: Repository = Depends(Repository.get_instance),
                    memcached_client: HashClient = Depends(get_memcached_client)) -> Any:
    if not ObjectId.is_valid(user_id):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)

    user = memcached_client.get(str(user_id))
    if user is not None:
        return user

    user = await repository.get_by_id(str(user_id), collection=0)
    if user is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    memcached_client.add(user_id, user)
    return user


@router.post("/user/", tags=["User"])
async def add_user(user: UserUpdate,
                      repository: Repository = Depends(Repository.get_instance),
                      search_repository: SearchStudentRepository = Depends(SearchStudentRepository.get_instance)) -> str:
    id = await repository.create(user)
    await search_repository.create(id, user)
    return id


@router.post("/tweet/", tags=["tweet"])
async def add_tweet(tweet: TweetUpdate,
                      repository: Repository = Depends(Repository.get_instance),
                      search_repository: SearchStudentRepository = Depends(SearchStudentRepository.get_instance)) -> str:
    id = await repository.create_tweet(tweet)
    await search_repository.create_tweet(id, tweet)
    return id


@router.delete("/user/{user_id}")
async def remove_user(user_id: str,
                         repository: Repository = Depends(Repository.get_instance),
                         search_repository: SearchStudentRepository = Depends(SearchStudentRepository.get_instance)) -> Response:
    if not ObjectId.is_valid(user_id):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    user = await repository.delete_user(user_id)
    if user is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    await search_repository.delete(user_id)
    return Response()


@router.delete("/tweet/{tweet_id}")
async def remove_tweet(tweet_id: str,
                         repository: Repository = Depends(Repository.get_instance),
                         search_repository: SearchStudentRepository = Depends(SearchStudentRepository.get_instance)) -> Response:
    if not ObjectId.is_valid(tweet_id):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    tweet = await repository.delete_tweet(tweet_id)
    if tweet is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    await search_repository.delete_tweet(tweet_id)
    return Response()


@router.put("/user/{user_id}", response_model=User)
async def update_user(user_id: str,
                         user_model: UserUpdate,
                         repository: Repository = Depends(Repository.get_instance),
                         search_repository: SearchStudentRepository = Depends(SearchStudentRepository.get_instance)) -> Any:
    if not ObjectId.is_valid(user_id):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    user = await repository.update(user_id, user_model)
    if user is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    await search_repository.update(user_id, user_model)
    return user
