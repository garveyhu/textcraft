from fastapi import APIRouter, Body

from textcraft.chains.extraction_chain_Kor import ExtractionChain

extraction_router = APIRouter(prefix="/extraction", tags=["提取API"])


"""信息提取"""


@extraction_router.post("/call", description="信息提取")
async def extraction(
    text: str = Body(..., embed=True),
    schema: str = Body(..., embed=True),
    prompt: str = Body(..., embed=True),
):
    return ExtractionChain().extraction(text=text, schema=schema, prompt=prompt)
