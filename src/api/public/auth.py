from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Request, status

from application.use_cases.auth.dto import TokenDTO
from application.use_cases.auth.login import LoginUseCase
from application.use_cases.auth.refresh import RefreshTokenUseCase
from application.use_cases.auth.register import RegisterUserUseCase
from config.containers import Container
from domain.validators.base import RefreshTokenDTO, UserLoginDTO, UserRegisterDTO

router = APIRouter(tags=["Authorization"], prefix="/auth")


@router.post("/register", status_code=status.HTTP_200_OK)
@inject
async def register(
    data: UserRegisterDTO = Depends(),
    use_case: RegisterUserUseCase = Depends(Provide[Container.register_use_case]),
) -> TokenDTO:
    return await use_case.execute(data)


@router.post("/login", status_code=status.HTTP_200_OK)
@inject
async def login(
    data: UserLoginDTO = Depends(),
    use_case: LoginUseCase = Depends(Provide[Container.login_use_case]),
) -> TokenDTO:
    return await use_case.execute(data)


@router.post("/refresh", status_code=status.HTTP_200_OK, response_model=TokenDTO)
@inject
async def refresh_token(
    request: Request,
    use_case: RefreshTokenUseCase = Depends(Provide[Container.refresh_token_use_case]),
) -> TokenDTO:
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        from fastapi import HTTPException

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Отсутствует заголовок Authorization или неверный формат",
        )

    refresh_token = auth_header.split(" ", 1)[1].strip()
    data = RefreshTokenDTO(refresh_token=refresh_token)
    return await use_case.execute(data)
