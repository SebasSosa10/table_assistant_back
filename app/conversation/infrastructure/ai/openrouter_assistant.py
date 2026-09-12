import httpx

from conversation.domain.ports.assistant_port import AssistantPort
from conversation.infrastructure.ai.prompts import SYSTEM_PROMPT
from shared.config.settings import settings
from shared.exceptions import AssistantError


class OpenRouterAssistant(AssistantPort):
    def complete(self, messages: list[dict]) -> str:
        if not settings.openrouter_api_key:
            raise AssistantError("Falta OPENROUTER_API_KEY en el archivo .env")

        payload = {
            "model": settings.openrouter_model,
            "messages": [{"role": "system", "content": SYSTEM_PROMPT}, *messages],
        }
        headers = {
            "Authorization": f"Bearer {settings.openrouter_api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "Table Assistant",
        }

        try:
            response = httpx.post(
                f"{settings.openrouter_base_url}/chat/completions",
                json=payload,
                headers=headers,
                timeout=60.0,
            )
            response.raise_for_status()
            data = response.json()
            content = data["choices"][0]["message"]["content"]
        except httpx.HTTPStatusError as exc:
            raise AssistantError(
                f"OpenRouter respondió {exc.response.status_code}: {exc.response.text}"
            ) from exc
        except (httpx.HTTPError, KeyError, IndexError, TypeError) as exc:
            raise AssistantError("No se pudo obtener una respuesta de la IA") from exc

        if not content:
            raise AssistantError("La IA devolvió una respuesta vacía")
        return content
