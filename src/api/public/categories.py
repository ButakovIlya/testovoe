from common.dto import CategoryRead, PostRead
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query, Request, status

from application.use_cases.categories.list_posts import PostByCategoryUseCase
from application.use_cases.common.list import ModelObjectListUseCase
from config.containers import Container
from domain.entities.enums import ModelType
from domain.validators.dto import PaginatedResponse

router = APIRouter(tags=["Public Category"], prefix="/categories")


@router.get(
    "/", response_model=PaginatedResponse[CategoryRead], status_code=status.HTTP_200_OK
)
@inject
async def list_categories(
    request: Request,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    use_case: ModelObjectListUseCase = Depends(Provide[Container.object_list_use_case]),
) -> PaginatedResponse[CategoryRead]:
    return await use_case.execute(
        request=request,
        ObjectDTO=CategoryRead,
        model_type=ModelType.CATEGORIES,
        page=page,
        page_size=page_size,
    )


@router.get(
    "/{title_slug}/posts",
    response_model=PaginatedResponse[PostRead],
    status_code=status.HTTP_200_OK,
)
@inject
async def list_posts_by_category(
    title_slug: str,
    request: Request,
    use_case: PostByCategoryUseCase = Depends(
        Provide[Container.post_by_category_use_case]
    ),
) -> PaginatedResponse[PostRead]:
    return await use_case.execute(
        request=request,
        category_name=title_slug,
    )
