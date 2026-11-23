from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

class UsuarioCadastro(BaseModel):
    nome: str = Field(min_length=1, max_length=150)
    email: EmailStr
    senha: str = Field(min_length=8, max_length=128)

    @field_validator("nome")
    @classmethod
    def nome_nao_vazio(cls, valor):
        valor = valor.strip()
        if not valor:
            raise ValueError("O nome não pode ser vazio.")
        return valor

    @field_validator("senha")
    @classmethod
    def senha_nao_vazia(cls, valor):
        if not valor.strip():
            raise ValueError("A senha não pode ser composta apenas de espaços.")
        return valor

class UsuarioResposta(BaseModel):
    id: int
    nome: str
    email: EmailStr
    perfil: str
    model_config = ConfigDict(from_attributes=True)

class LoginEntrada(BaseModel):
    email: EmailStr
    senha: str = Field(min_length=1, max_length=128)

class TokenResposta(BaseModel):
    access_token: str
    token_type: str = "bearer"
