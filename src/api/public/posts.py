from common.dto import PostRead
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query, Request, status

from application.use_cases.common.list import ModelObjectListUseCase
from application.use_cases.posts.retrieve import PostRetriveUseCase
from config.containers import Container
from domain.entities.enums import ModelType
from domain.validators.dto import PaginatedResponse

router = APIRouter(tags=["Public Post"], prefix="/posts")


@router.get(
    "/", response_model=PaginatedResponse[PostRead], status_code=status.HTTP_200_OK
)
@inject
async def list_posts(
    request: Request,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    use_case: ModelObjectListUseCase = Depends(Provide[Container.object_list_use_case]),
) -> PaginatedResponse[PostRead]:
    """Получить список постов"""
    return await use_case.execute(
        request=request,
        ObjectDTO=PostRead,
        model_type=ModelType.POSTS,
        page=page,
        page_size=page_size,
    )


@router.get("/{title_slug}", response_model=PostRead, status_code=status.HTTP_200_OK)
@inject
async def retrieve_post(
    title_slug: str,
    request: Request,
    use_case: PostRetriveUseCase = Depends(Provide[Container.post_retrieve_use_case]),
) -> PostRead:
    return await use_case.execute(title_slug)
