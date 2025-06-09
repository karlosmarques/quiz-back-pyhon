from fastapi import APIRouter

order_router = APIRouter(prefix="/quizes", tags=["quizes"])


@order_router.get('/')
async def get_quizes():
    return {"mensagem":"lista de quizes"}