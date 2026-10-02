## Como Executar

### 1. Pré-requisitos
- Python 3.10+ (ou [uv](https://github.com/astral-sh/uv))

### 2. Configurar o Ambiente

#### Opção A: Usando `uv` (Recomendado)
```bash
# Criar ambiente virtual e instalar dependências
uv venv
uv pip install -r requirements.txt
```

#### Opção B: Usando `venv` e `pip` tradicional
```bash
python3 -m venv .venv
source .venv/bin/activate  # No Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Criar Usuário Administrador

Execute o comando CLI para cadastrar um administrador (a senha será solicitada de forma segura e oculta no terminal):

```bash
# Com uv:
uv run flask create-user admin

# Ou com ambiente virtual ativado:
flask create-user admin
```

### 4. Executar a Aplicação

```bash
# Com uv:
uv run flask run

# Ou com ambiente virtual ativado:
flask run
```

A aplicação estará acessível em: `http://127.0.0.1:5000/`

---

## Rotas Principais

- **Loja (Pública)**: `http://127.0.0.1:5000/main/v1/`
- **API REST (Pública)**: `http://127.0.0.1:5000/api/v1/product/`
- **Login Administrativo**: `http://127.0.0.1:5000/login`
- **Painel Administrativo (Protegido)**: `http://127.0.0.1:5000/admin/`
- **Logout**: `http://127.0.0.1:5000/logout`
