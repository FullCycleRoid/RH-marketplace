from starlette import status

from src.products.presentaition.api.router import router


@router.get("/{uuid}", status_code=status.HTTP_200_OK, response_model=None)
async def get_product_by_uuid():
    pass
