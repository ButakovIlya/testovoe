from typing import Optional

from common.dto import PostRead
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Form, Query, Request, Response, status

from api.admin.schemas import PostPut
from api.permissions.is_admin import is_admin
from application.use_cases.common.delete import ModelObjectDeleteUseCase
from application.use_cases.common.list import ModelObjectListUseCase
from application.use_cases.common.retrieve import ModelObjectRetrieveUseCase
from application.use_cases.common.update import ModelObjectUpdateUseCase
from application.use_cases.dto import CreatePostDTO
from application.use_cases.posts.create import PostCreateUseCase
from application.use_cases.posts.update import PostUpdateUseCase
from config.containers import Container
from domain.entities.enums import ModelType
from domain.validators.dto import PaginatedResponse

router = APIRouter(tags=["Posts"], prefix="/posts", dependencies=[Depends(is_admin)])


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


@router.get("/{post_id}", response_model=PostRead, status_code=status.HTTP_200_OK)
@inject
async def retrieve_post(
    post_id: int,
    request: Request,
    use_case: ModelObjectRetrieveUseCase = Depends(
        Provide[Container.object_retrieve_use_case]
    ),
) -> PostRead:
    """Получить пост по ID"""
    return await use_case.execute(
        obj_id=post_id,
        model_type=ModelType.POSTS,
        ObjectDTO=PostRead,
    )


@router.post("/", status_code=status.HTTP_200_OK)
@inject
async def create_post(
    request: Request,
    title: str = Form(...),
    body: Optional[str] = Form(None),
    category_id: int = Form(...),
    use_case: PostCreateUseCase = Depends(Provide[Container.post_create_use_case]),
):
    user_id: int = request.state.user.id
    data = CreatePostDTO(
        title=title, body=body, category_id=category_id, author_id=user_id
    )
    return await use_case.execute(data=data)


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_post(
    post_id: int,
    request: Request,
    use_case: ModelObjectDeleteUseCase = Depends(
        Provide[Container.object_delete_use_case]
    ),
) -> Response:
    """Удалить место"""
    await use_case.execute(
        obj_id=post_id,
        model_type=ModelType.POSTS,
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{post_id}", status_code=status.HTTP_200_OK)
@inject
async def update_post(
    post_id: int,
    data: PostPut,
    request: Request,
    use_case: PostUpdateUseCase = Depends(Provide[Container.post_update_use_case]),
) -> PostRead:
    return await use_case.execute(post_id, data)
