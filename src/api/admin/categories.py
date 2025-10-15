from common.dto import CategoryRead
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Form, Query, Request, Response, status

from api.admin.schemas import CategoryPut
from api.permissions.is_admin import is_admin
from application.use_cases.categories.create import CategoryCreateUseCase
from application.use_cases.categories.update import CategoryUpdateUseCase
from application.use_cases.common.create import ModelObjectCreateUseCase
from application.use_cases.common.delete import ModelObjectDeleteUseCase
from application.use_cases.common.list import ModelObjectListUseCase
from application.use_cases.common.retrieve import ModelObjectRetrieveUseCase
from application.use_cases.common.update import ModelObjectUpdateUseCase
from application.use_cases.dto import CreateCategoryDTO
from application.use_cases.posts.create import PostCreateUseCase
from config.containers import Container
from domain.entities.category import Category
from domain.entities.enums import ModelType
from domain.validators.dto import PaginatedResponse

router = APIRouter(
    tags=["Categories"], prefix="/categories", dependencies=[Depends(is_admin)]
)


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
    "/{category_id}", response_model=CategoryRead, status_code=status.HTTP_200_OK
)
@inject
async def retrieve_category(
    category_id: int,
    request: Request,
    use_case: ModelObjectRetrieveUseCase = Depends(
        Provide[Container.object_retrieve_use_case]
    ),
) -> CategoryRead:
    """Получить пост по ID"""
    return await use_case.execute(
        obj_id=category_id,
        model_type=ModelType.CATEGORIES,
        ObjectDTO=CategoryRead,
    )


@router.post("/", status_code=status.HTTP_200_OK)
@inject
async def create_category(
    request: Request,
    name: str = Form(...),
    use_case: CategoryCreateUseCase = Depends(
        Provide[Container.category_create_use_case]
    ),
) -> CategoryRead:
    data = CreateCategoryDTO(
        name=name,
    )
    return await use_case.execute(data)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_category(
    category_id: int,
    request: Request,
    use_case: ModelObjectDeleteUseCase = Depends(
        Provide[Container.object_delete_use_case]
    ),
) -> Response:
    """Удалить место"""
    await use_case.execute(
        obj_id=category_id,
        model_type=ModelType.CATEGORIES,
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{category_id}", status_code=status.HTTP_200_OK)
@inject
async def update_category(
    category_id: int,
    data: CategoryPut,
    request: Request,
    use_case: CategoryUpdateUseCase = Depends(
        Provide[Container.category_update_use_case]
    ),
) -> CategoryRead:
    return await use_case.execute(category_id, data)
