from utils.sanitize import sanitize_user, sanitize_token
from repositories.user_repository import get_user_by_email, insert_user, get_user_by_id, update_password
from repositories.token_repository import get_token
from services.user_service import generate_hashed_password, check_password
from services.email_service import send_email
from services.token_service import generate_user_token, revoke_token
from models.user import User
from jinja2 import Template


def register_user(name: str, email: str, confirmation_email: str, password: str, confirm_password: str) -> dict:

    if email != confirmation_email:
        return {"error": "Emails não conferem"}
    
    if password != confirm_password:
        return {"error": "Senhas não conferem"}

    existing_user = get_user_by_email(email=email)

    if existing_user:
        return {"error": "Usuário já cadastrado com este email"}


    hashed_password = generate_hashed_password(password=password)

    new_user = insert_user(name=name, email=email, password=hashed_password)

    if not new_user:
        return {"error": "Erro ao cadastrar usuário"}

    return {"error": None, "user": sanitize_user(new_user)}


def login_user(email: str, password: str) -> dict:
    existing_user = get_user_by_email(email=email)

    if not existing_user:
        return {"error": "Usuário não encontrado"}

    if not check_password(plain_password=password, hashed_password=existing_user.password):
        return {"error": "Senha inválida"}

    token = generate_user_token(user=existing_user, token_type="Bearer")

    if not token:
        return {"error": "Erro ao gerar token"}

    return {"error": None, "token": sanitize_token(token), "user": sanitize_user(existing_user)}




def send_user_forgot_password(data: dict) -> None:
    token = data.get("token", None)
    email = data.get("user",  None).email
    name = data.get("user", None).name

    if not token or not email or not name:
        return

    template_file_path = "./assets/templates/recovery-password.html"

    with open(template_file_path, "r", encoding="utf-8") as file:
        template_email = file.read()
        
    template = Template(template_email)
    
    content = template.render(name=name, token=token)
    send_email(email=email, content=content.strip(),
               subject="Recuperação de senha")


def logout_user(token: str) -> None:
    revoke_token(token=token)


def forgot_password_service(email: str) -> dict:
    user = get_user_by_email(email=email)

    if not user:
        return {"error": "Usuário não encontrado"}

    token = generate_user_token(user=user, token_type="RecoverPassword")

    if not token:
        return {"error": "Erro ao gerar token"}

    return {"error": None, "token": token.token, "user": user}


def validate_code_service(token: str) -> dict:
    token_to_validate = get_token(token=token)

    if not token_to_validate:
        return {"error": "Codigo inválido ou não encontrado"}

    if token_to_validate.token != token:
        return {"error": "Código inválido"}

    user = get_user_by_id(user_id=token_to_validate.user_id)

    access_token = generate_user_token(user=user, token_type="Bearer")

    return {"error": None, "access_token": sanitize_token(access_token), "validated_token": token_to_validate.token, "user": sanitize_user(user)}


def reset_password_service(new_password: str, confirm_password: str, user: User) -> dict:

    if new_password != confirm_password:
        return {"error": "Senhas não conferem"}

    if not user:
        return {"error": "Usuário não encontrado"}

    hashed_password = generate_hashed_password(password=new_password)

    user.password = hashed_password

    updated_user = update_password(user.id, hashed_password)

    if not updated_user:
        return {"error": "Erro ao atualizar senha"}

    return {"error": None}
