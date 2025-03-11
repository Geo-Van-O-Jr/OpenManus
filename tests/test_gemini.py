import pytest
from app.schema import Message
from app.llm_gemini import GeminiLLM
from app.config import GeminiSettings

@pytest.mark.asyncio
async def test_basic_chat():
    llm = GeminiLLM()  # Usa configuração "gemini" do config.toml
    messages = [Message(role="user", content="Quem é você?")]
    system_msgs = [
        Message(role="system", content="Você é um assistente chamado OpenManus, focado em ajudar com tarefas de programação.")
    ]
    response = await llm.ask(messages, system_msgs)
    assert "OpenManus" in response
    assert len(response) > 0

@pytest.mark.asyncio
async def test_programming_question():
    llm = GeminiLLM()
    messages = [Message(role="user", content="Como fazer um loop for em Python?")]
    response = await llm.ask(messages)
    assert "for" in response.lower()
    assert "python" in response.lower()

@pytest.mark.asyncio
async def test_error_handling():
    llm = GeminiLLM()
    messages = None
    with pytest.raises(ValueError):
        await llm.ask(messages)

@pytest.mark.asyncio
async def test_invalid_api_key():
    config = GeminiSettings(
        model="gemini-pro",
        api_key="invalid_key",
        max_tokens=4096,
        temperature=0.0
    )
    with pytest.raises(ValueError, match="Failed to initialize Gemini"):
        llm = GeminiLLM(llm_config=config)
