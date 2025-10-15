from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Request, status

from api.permissions.is_authenticated import is_authenticated
from application.use_cases.auth.me import GetCurrentUserUseCase
from application.use_cases.users.dto import UserDTO
from config.containers import Container

router = APIRouter(tags=["Public Profile"], prefix="/profile")


@router.get("/me", status_code=status.HTTP_200_OK, response_model=UserDTO)
@inject
@is_authenticated
async def me(
    request: Request,
    use_case: GetCurrentUserUseCase = Depends(
        Provide[Container.get_current_user_use_case]
    ),
) -> UserDTO:
    user = request.state.user

    return await use_case.execute(user.id)
