from io import StringIO
from typing import Dict, List, Union

from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse

from textcraft.api.schema.chats import ChatList
from textcraft.vectors.es.es_online_chat import ESOnline
from textcraft.vectors.es.es_search import ESSearch
from textcraft.vectors.es.es_store import ESStore

es_router = APIRouter(prefix="/es", tags=["ES相关API"])


"""ES存储"""


@es_router.post("/store_chat", description="存储聊天记录")
async def store_chat(chats: ChatList):
    ESStore().store_chat(chats)
    return {"message": "Chat stored successfully!"}


@es_router.post("/file", description="存储文件记录")
async def store_file(file: UploadFile = File(...)):
    content = await file.read()
    try:
        decoded_content = content.decode("utf-8")
    except UnicodeDecodeError:
        return JSONResponse(content={"error": "Invalid file encoding"}, status_code=400)
    file_like_object = StringIO(decoded_content)
    ESStore(index_suffix="resource_").store_file(file_like_object)
    
    return {"message": "File stored successfully!"}


@es_router.post("/store_chat/online", description="存储在线客服聊天记录")
async def store_chat_online(chat: List[Dict[str, Union[str, Dict[str, str]]]]):
    ESOnline().online_chat(chat)
    return {"message": "Online chat save successfully!"}


"""ES查询"""


@es_router.get("/search_show", description="获取会话中的聊天记录")
async def search_show(size: int = 10):
    return ESStore().search_show(size)


@es_router.get("/similarity_search", description="按照得分排序返回结果")
async def similarity_search(query: str):
    return ESStore().similarity_search_score(query)


@es_router.get("/similarity_search/online", description="在线相似性搜索")
async def similarity_search_online(query: str):
    return ESOnline().similarity_search_score(query)


@es_router.get("/context_search/online", description="在线客服聊天记录上下文查询")
async def context_search_online(time: str, loginid: str):
    return ESSearch().bool_search(time, loginid)
