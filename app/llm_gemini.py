from typing import List, Optional, Union
import google.generativeai as genai
from google.api_core import exceptions
from app.schema import Message
from app.config import config, GeminiSettings

class GeminiLLM:
    def __init__(self, config_name: str = "gemini", llm_config: Optional[GeminiSettings] = None):
        if llm_config:
            self.config = llm_config
        else:
            gemini_config = config.llm.get(config_name)
            if not gemini_config:
                raise ValueError(f"Configuration '{config_name}' not found")
            
            self.config = GeminiSettings(
                model=gemini_config.model,
                api_key=gemini_config.api_key,
                max_tokens=gemini_config.max_tokens,
                temperature=gemini_config.temperature
            )
        
        # Validar API key
        if not self.config.api_key or len(self.config.api_key) < 10:
            raise ValueError("Invalid API key configuration")
            
        try:
            genai.configure(api_key=self.config.api_key)
            self.model = genai.GenerativeModel(self.config.model)
            # Fazer uma chamada de teste para validar a API key
            self.model.generate_content("test")
        except Exception as e:
            raise ValueError(f"Failed to initialize Gemini with provided API key: {str(e)}")

    async def ask(
        self,
        messages: List[Union[dict, Message]],
        system_msgs: Optional[List[Union[dict, Message]]] = None,
        stream: bool = True,
        temperature: Optional[float] = None,
    ) -> str:
        if messages is None:
            raise ValueError("Messages cannot be None")
            
        # Converter mensagens para formato do Gemini
        formatted_messages = self._format_messages(messages, system_msgs)
        
        # Configurar parâmetros
        generation_config = {
            "temperature": temperature or self.config.temperature,
            "max_output_tokens": self.config.max_tokens,
        }
        
        try:
            # Fazer a chamada ao Gemini
            response = await self.model.generate_content_async(
                formatted_messages,
                generation_config=generation_config,
                stream=False  # Desabilitar streaming por enquanto
            )
            
            # Aguardar a resposta completa
            await response.resolve()
            return response.text
        except Exception as e:
            raise Exception(f"Gemini API error: {str(e)}")

    def _format_messages(
        self, 
        messages: List[Union[dict, Message]], 
        system_msgs: Optional[List[Union[dict, Message]]] = None
    ) -> str:
        formatted = []
        
        # Adicionar system messages primeiro
        if system_msgs:
            for msg in system_msgs:
                if isinstance(msg, dict):
                    formatted.append(f"System: {msg['content']}")
                else:
                    formatted.append(f"System: {msg.content}")
        
        # Adicionar mensagens do usuário
        for msg in messages:
            if isinstance(msg, dict):
                formatted.append(f"User: {msg['content']}")
            else:
                formatted.append(f"User: {msg.content}")
                
        return "\n".join(formatted)
