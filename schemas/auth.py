from pydantic import BaseModel
from models.user import User


class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterUserRequest(BaseModel):
    name: str
    email: str
    confirm_email: str
    password: str
    confirm_password: str
    
    
class ForgotPasswordRequest(BaseModel):
    email: str
    
class ValidateCodeRequest(BaseModel):
    token: str
    
class ResetPasswordRequest(BaseModel):
    new_password: str
    confirm_password: str
    
    


    
    
    
    
