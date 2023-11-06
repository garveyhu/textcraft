from typing import Dict, List, Union

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from textcraft.vectors.pinecone_qa import vector_qa
from textcraft.vectors.pinecone_store import similarity_search, store_paragraphs

complex_router = APIRouter(prefix="/complex", tags=["complex"])


@complex_router.get("/pinecone/qa")
async def pinecone_qa(text: str):
    return vector_qa(text)


@complex_router.post("/pinecone/store")
async def pinecone_store(paragraphs: List[Dict[str, Union[str, Dict[str, str]]]]):
    result = store_paragraphs(paragraphs)
    if result is None:
        return JSONResponse(content={"error": "Invalid file format"}, status_code=400)
    return JSONResponse(content="success", status_code=200)


@complex_router.get("/pinecone/similarity_search")
async def pinecone_similarity_search(text: str):
    return similarity_search(text)
