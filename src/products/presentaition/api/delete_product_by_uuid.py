from starlette import status

from src.products.presentaition.api.router import router


@router.delete("/{uuid}", status_code=status.HTTP_200_OK, response_model=None)
async def delete_product_by_uuid():
    pass
