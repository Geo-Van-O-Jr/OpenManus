# Guia de Configuração e Testes do OpenManus

## 1. Configuração do Ambiente

### 1.1 Instalação com UV (Recomendado)

```bash
# 1. Instalar UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Clonar o repositório
git clone https://github.com/mannaandpoem/OpenManus.git
cd OpenManus

# 3. Criar e ativar ambiente virtual
uv venv
# Windows:
.venv\Scripts\activate
# Unix/MacOS:
# source .venv/bin/activate

# 4. Instalar dependências
uv pip install -r requirements.txt
```

### 1.2 Configuração do Arquivo config.toml

1. Copie o arquivo de exemplo:
```bash
cp config/config.example.toml config/config.toml
```

2. Configure suas credenciais no `config/config.toml`:
```toml
[llm.gemini]
model = "gemini-pro"
api_key = "sua-chave-api-aqui"
max_tokens = 4096
temperature = 0.0
```

## 2. Estrutura de Testes

### 2.1 Organização
- Testes ficam no diretório `tests/`
- Arquivos de teste seguem o padrão `test_*.py`
- Configurações do pytest em `pytest.ini`

### 2.2 Executando Testes

```bash
# Windows
.venv\Scripts\pytest tests/test_gemini.py -v

# Unix/MacOS
.venv/bin/pytest tests/test_gemini.py -v

# Com ambiente virtual ativado
pytest tests/test_gemini.py -v
```

### 2.3 Exemplo de Teste

```python
import pytest
from app.schema import Message
from app.llm_gemini import GeminiLLM

@pytest.mark.asyncio
async def test_basic_chat():
    llm = GeminiLLM()
    messages = [Message(role="user", content="Teste")]
    response = await llm.ask(messages)
    assert len(response) > 0
```

## 3. Boas Práticas

1. **Isolamento**: Cada teste deve ser independente
2. **Nomeação**: Use nomes descritivos para os testes
3. **Assertions**: Verifique resultados específicos
4. **Tratamento de Erros**: Inclua testes para casos de erro
5. **Documentação**: Comente casos complexos

## 4. Troubleshooting

### Problemas Comuns

1. **Erro de Ambiente Virtual**:
   - Verifique se está ativado corretamente
   - Confirme o caminho dos executáveis

2. **Falha nas Credenciais**:
   - Verifique `config.toml`
   - Confirme validade da API key

3. **Dependências**:
   - Atualize requirements: `uv pip install -r requirements.txt`
   - Verifique conflitos de versão

## 5. CI/CD

- Testes automáticos via GitHub Actions
- Pre-commit hooks para qualidade de código
- Verificação de tipos com mypy