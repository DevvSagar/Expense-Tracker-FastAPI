from pydantic import BaseModel , Field , EmailStr , field_validator , ValidationInfo


class Login(BaseModel):
    email: EmailStr
    password: str = Field(...,min_length=8,max_length=128)


class Register(BaseModel):
    name: str = Field(...,min_length=2,max_length=101)
    email: EmailStr
    password: str = Field(...,min_length=8,max_length=128)
    confirm_password: str = Field(...,min_length=8,max_length=128)

    @field_validator("confirm_password")
    @classmethod
    def passwords_match(cls, v, info:ValidationInfo):
        password = info.data.get("password")
        if password == v:
            return v
        raise ValueError("password do not match !!!")
