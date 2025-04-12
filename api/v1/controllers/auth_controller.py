from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from schemas.auth import LoginRequest, RegisterUserRequest, ForgotPasswordRequest, ValidateCodeRequest, ResetPasswordRequest
from services.auth_service import register_user, login_user, send_user_forgot_password, logout_user, forgot_password_service, validate_code_service, reset_password_service
from services.token_service import revoke_token
router = APIRouter()


@router.post("/login")
def login(login_request: LoginRequest):
    login_data = login_user(email=login_request.email,
                            password=login_request.password)
    if login_data["error"]:
        return JSONResponse(status_code=400, content={"message": login_data["error"]})

    return JSONResponse(status_code=200, content={"message": "Usuário logado com sucesso!", "access_token": jsonable_encoder(login_data["token"]), "user": jsonable_encoder(login_data["user"])})


@router.post("/register")
def register(register_request: RegisterUserRequest):

    register_data = register_user(name=register_request.name, email=register_request.email,
                                  confirmation_email=register_request.confirm_email, 
                                  password=register_request.password, confirm_password=register_request.confirm_password)
    if register_data["error"]:
        return JSONResponse(status_code=400, content={"message": register_data["error"]})

    return JSONResponse(status_code=201, content={"message": "Usuário cadastrado com sucesso!", "user": jsonable_encoder(register_data["user"])})


@router.post("/logout")
def logout(request: Request, background_tasks: BackgroundTasks):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return JSONResponse(status_code=401, content={"message": "Token não fornecido"})
    token = auth_header.split(" ")[1]
    background_tasks.add_task(logout_user, token)
    return JSONResponse(status_code=200, content={"message": "Logout realizado com sucesso!"})


@router.post("/forgot_password")
def forgot_password(forgot_password_request: ForgotPasswordRequest, background_tasks: BackgroundTasks):
    forgot_password_data = forgot_password_service(
        email=forgot_password_request.email)
    if forgot_password_data["error"]:
        return JSONResponse(status_code=400, content={"message": forgot_password_data["error"]})
    background_tasks.add_task(send_user_forgot_password, forgot_password_data)
    return JSONResponse(status_code=200, content={"message": "Código enviado com sucesso!"})


@router.post("/validate_code")
def validate_code(validate_code_request: ValidateCodeRequest, background_tasks: BackgroundTasks):
    validate_code_data = validate_code_service(
        token=validate_code_request.token)

    if validate_code_data["error"]:
        return JSONResponse(status_code=400, content={"message": validate_code_data["error"]})

    background_tasks.add_task(
        revoke_token, validate_code_data["validated_token"])

    return JSONResponse(status_code=200, content={"message": "Código validado com sucesso!",
                                                  "access_token": jsonable_encoder(validate_code_data["access_token"]), "user": jsonable_encoder(validate_code_data["user"])})


@router.put("/reset_password")
def reset_password(reset_password_request: ResetPasswordRequest, request: Request):
    user = request.state.user
    reset_password_data = reset_password_service(
        new_password=reset_password_request.new_password,
        confirm_password=reset_password_request.confirm_password,
        user=user)
    if reset_password_data["error"]:
        return JSONResponse(status_code=400, content={"message": reset_password_data["error"]})

    return JSONResponse(status_code=200, content={"message": "Senha atualizada com sucesso!"})
