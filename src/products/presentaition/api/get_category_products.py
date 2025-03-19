from starlette import status

from src.products.presentaition.api.router import router


@router.get("/{category}", status_code=status.HTTP_200_OK, response_model=None)
async def get_category_products():
    pass
