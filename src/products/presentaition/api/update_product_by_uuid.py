from starlette import status

from src.products.presentaition.api.router import router


@router.put("/{uuid}", status_code=status.HTTP_200_OK, response_model=None)
async def update_product_by_uuid():
    pass
