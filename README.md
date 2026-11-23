# APS 4 – API de Eventos Acadêmicos com Autenticação e Segurança

Continuação da APS 3. O projeto mantém a API de eventos acadêmicos com FastAPI, SQLite e SQLAlchemy e acrescenta cadastro de usuários, hash seguro de senhas com Argon2, autenticação JWT, proteção de rotas e autorização por perfil.

## 1. Funcionalidades preservadas da APS 3
- CRUD de eventos e participantes.
- Inscrição de participantes em eventos, com verificação de existência, duplicidade e capacidade.
- Persistência SQLite/SQLAlchemy e relacionamentos Evento–Inscrição–Participante.
- Relatórios dinâmicos de ocupação, categorias e cursos.
- Validação Pydantic e tratamento de erros HTTP.

## 2. Novos recursos da APS 4
- Cadastro público de usuário comum em `POST /usuarios`.
- Senhas armazenadas somente como hash Argon2; nunca são devolvidas pela API.
- Login em `POST /auth/login`, com token JWT assinado (HS256) e validade configurável (padrão: 30 minutos).
- Consulta do usuário autenticado em `GET /auth/me`.
- Dependências centralizadas para validar token e exigir perfil administrador.
- Perfis `administrador` e `usuario`.

## 3. Tecnologias
Python 3.10+, FastAPI, SQLite, SQLAlchemy ORM 2.x, Pydantic 2, argon2-cffi (Argon2), PyJWT e Uvicorn.

## 4. Estrutura
```text
APS4_API_Eventos/
├── main.py
├── database.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
├── controller/
│   ├── evento_controller.py
│   ├── participante_controller.py
│   ├── relatorio_controller.py
│   ├── usuario_controller.py
│   └── auth_controller.py
├── model/
│   ├── evento.py
│   ├── participante.py
│   ├── inscricao.py
│   └── usuario.py
├── schema/
│   ├── evento_schema.py
│   ├── participante_schema.py
│   ├── inscricao_schema.py
│   └── usuario_schema.py
├── service/
│   ├── evento_service.py
│   ├── participante_service.py
│   ├── relatorio_service.py
│   └── usuario_service.py
└── security/
    └── security.py
```

## 5. Instalação e execução
No terminal, dentro da pasta do projeto:

### Windows
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Linux/macOS
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Copie `.env.example` para `.env`, gere uma chave com `python -c "import secrets; print(secrets.token_urlsafe(48))"`, cole-a em `SECRET_KEY` e defina a senha do administrador. Use uma chave secreta aleatória com pelo menos 32 caracteres. Em seguida, execute:
```bash
uvicorn main:app --reload
```
Swagger: http://127.0.0.1:8000/docs

O banco `eventos_academicos.db` é criado automaticamente na pasta do projeto. Não apague esse arquivo se quiser preservar os dados da APS 3.

## 6. Configuração da chave secreta e administrador inicial
A chave JWT não deve ser publicada no GitHub. A aplicação carrega o arquivo `.env` local (ignorado pelo Git) ou as variáveis do sistema. Copie `.env.example` para `.env` e configure valores próprios. Alternativamente, configure no ambiente:

**PowerShell (Windows):**
```powershell
$env:SECRET_KEY="gere-uma-chave-aleatoria-longa-e-secreta"
$env:ACCESS_TOKEN_EXPIRE_MINUTES="30"
$env:ADMIN_NOME="Administrador Inicial"
$env:ADMIN_EMAIL="admin@exemplo.com"
$env:ADMIN_PASSWORD="DefinaUmaSenhaForte123!"
uvicorn main:app --reload
```

**Linux/macOS:**
```bash
export SECRET_KEY="gere-uma-chave-aleatoria-longa-e-secreta"
export ACCESS_TOKEN_EXPIRE_MINUTES="30"
export ADMIN_NOME="Administrador Inicial"
export ADMIN_EMAIL="admin@exemplo.com"
export ADMIN_PASSWORD="DefinaUmaSenhaForte123!"
uvicorn main:app --reload
```

O administrador inicial é criado somente se `ADMIN_NOME`, `ADMIN_EMAIL` e `ADMIN_PASSWORD` estiverem configurados e o e-mail ainda não existir (a senha deve ter pelo menos 8 caracteres). Essa é a estratégia controlada de provisionamento administrativo. Troque os exemplos por valores próprios. A aplicação não inicia se `SECRET_KEY` estiver ausente ou tiver menos de 32 caracteres. Isso evita executar a API com uma chave padrão conhecida.

## 7. Cadastro de usuários e login

### Criar usuário comum – POST `/usuarios`
```json
{
  "nome": "Aluno Exemplo",
  "email": "aluno@exemplo.com",
  "senha": "senha_segura123"
}
```
A resposta contém somente `id`, `nome`, `email` e `perfil`. O perfil é sempre `usuario`; campos extras como `perfil: administrador` enviados pelo cliente não concedem privilégios. A senha precisa ter pelo menos 8 caracteres e não pode ser composta apenas de espaços. E-mail duplicado retorna `409`.

### Login – POST `/auth/login`
```json
{
  "email": "aluno@exemplo.com",
  "senha": "senha_segura123"
}
```
Resposta:
```json
{
  "access_token": "<JWT gerado pela API>",
  "token_type": "bearer"
}
```
Credenciais incorretas retornam `401` com mensagem genérica.

### Usar token
No Swagger, clique em **Authorize** e informe o token recebido (conforme o esquema Bearer exibido), ou envie o cabeçalho:
```text
Authorization: Bearer <access_token>
```

### Meus dados – GET `/auth/me`
Exige token válido e retorna id, nome, e-mail e perfil do usuário identificado pelo token. Não aceita um ID de usuário fornecido pelo cliente.

## 8. Perfis e permissões
| Operação | Público | Usuário autenticado | Administrador |
|---|---:|---:|---:|
| Listar/consultar eventos | Sim | Sim | Sim |
| Cadastrar/atualizar/excluir eventos | Não | Não | Sim |
| Listar/consultar participantes | Não | Sim | Sim |
| Cadastrar/alterar/excluir participantes | Não | Não | Sim |
| Realizar inscrição | Não | Sim | Sim |
| Consultar inscritos de um evento | Não | Não | Sim |
| Consultar relatórios | Não | Não | Sim |
| Cadastrar usuário comum | Sim | Sim | Sim |
| Login | Sim | Sim | Sim |
| Consultar `/auth/me` | Não | Sim | Sim |

Usuários comuns podem consultar os dados dos participantes (necessário para identificar o `participante_id` ao realizar inscrições), mas não podem alterá-los. A autorização é aplicada no servidor por dependências FastAPI. Usuário autenticado sem permissão recebe `403`.

## 9. Rotas completas
| Método | Rota | Acesso |
|---|---|---|
| POST | `/usuarios` | Público – cria perfil usuario |
| POST | `/auth/login` | Público |
| GET | `/auth/me` | Autenticado |
| GET | `/eventos` | Público |
| GET | `/eventos/{evento_id}` | Público |
| POST | `/eventos` | Administrador |
| PUT | `/eventos/{evento_id}` | Administrador |
| DELETE | `/eventos/{evento_id}` | Administrador |
| POST | `/participantes` | Administrador |
| GET | `/participantes` | Autenticado |
| GET | `/participantes/{participante_id}` | Autenticado |
| PUT | `/participantes/{participante_id}` | Administrador |
| DELETE | `/participantes/{participante_id}` | Administrador |
| POST | `/eventos/{evento_id}/inscricoes/{participante_id}` | Autenticado |
| GET | `/eventos/{evento_id}/inscricoes` | Administrador |
| GET | `/relatorios/eventos/ocupacao` | Administrador |
| GET | `/relatorios/eventos/categorias` | Administrador |
| GET | `/relatorios/participantes/cursos` | Administrador |

**Observação sobre inscrições:** a rota existente da APS 3 recebe `participante_id` no caminho. Nesta versão, qualquer usuário autenticado pode invocá-la; a regra de associação entre a conta de usuário e o cadastro de participante não existia no modelo da APS 3. Para um sistema real, o próximo refinamento seria relacionar `Usuario` a `Participante` e derivar o participante diretamente da conta autenticada.

## 10. Relatórios preservados
- `GET /relatorios/eventos/ocupacao`: capacidade, inscritos, vagas e percentual de ocupação.
- `GET /relatorios/eventos/categorias`: quantidade de eventos, capacidade e inscrições por categoria.
- `GET /relatorios/participantes/cursos`: participantes e inscrições por curso.

Todos são calculados a partir dos registros SQLite via SQLAlchemy, sem listas fixas.

## 11. Códigos de erro
- `401 Unauthorized`: credenciais inválidas, token ausente, inválido ou expirado.
- `403 Forbidden`: usuário autenticado sem permissão administrativa.
- `404 Not Found`: evento ou participante inexistente.
- `409 Conflict`: e-mail duplicado, inscrição repetida ou evento sem vagas.
- `422 Unprocessable Entity`: dados enviados não passam na validação Pydantic. A resposta informa o campo e o motivo, mas não devolve o valor enviado, para que senhas digitadas nunca sejam retornadas pela API.

As respostas públicas nunca incluem senha ou hash.

## 12. Roteiro de testes exigido pela APS 4
1. `POST /usuarios`: cadastrar usuário e conferir que a resposta não contém senha nem hash.
2. Conferir no banco que `senha_hash` contém um hash Argon2, não a senha original.
3. Repetir cadastro com o mesmo e-mail: esperar `409`.
4. `POST /auth/login` com dados corretos: esperar token e `token_type: bearer`.
5. Login com senha errada: esperar `401` e mensagem genérica.
6. Chamar uma rota protegida sem token: esperar `401`.
7. Chamar `GET /auth/me` com token válido: esperar `200` e dados do próprio usuário.
8. Usar token adulterado ou expirado: esperar `401`.
9. Com token de usuário comum, tentar `POST /eventos`: esperar `403`.
10. Com token de administrador provisionado por variáveis de ambiente, cadastrar/alterar/excluir evento: esperar sucesso.
11. Com token de administrador, executar CRUD de participantes e consultar os três relatórios.
12. Testar inscrição com usuário autenticado e verificar duplicidade/capacidade; reiniciar a aplicação e confirmar que eventos, participantes, inscrições e usuários persistem.

## 13. Arquitetura e responsabilidades
- **Controller:** rotas HTTP e dependências de autenticação/autorização.
- **Model:** tabelas SQLAlchemy e relacionamentos.
- **Schema:** validação e contratos de entrada/saída Pydantic.
- **Service:** regras de negócio, persistência e autenticação de credenciais.
- **Security:** hash Argon2, criação/validação JWT e dependências de usuário/perfil.
- **Database:** conexão e sessões SQLite.

## 14. GitHub e entrega
Entregar o código-fonte completo, `requirements.txt`, este `README.md` e o link do repositório atualizado. Antes de enviar:
1. Teste os cenários no Swagger.
2. Configure segredo próprio no ambiente e não faça commit de `.env`.
3. Confira que `.env` e `eventos_academicos.db` estão ignorados pelo Git.
4. Substitua abaixo pelo link real do repositório:

https://github.com/leonardofigura-coder/APS4_Backend_Leonardo_Figura
