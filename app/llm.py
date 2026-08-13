import httpx

from app.config import Settings


class LLMClient:
    def __init__(self, settings: Settings):
        self.url = settings.llm_url
        self.model = settings.llm_model
        self.timeout = settings.request_timeout

    async def complete(self, system: str, user: str) -> str:
        body = {
            "model": self.model,
            "stream": False,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        }
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(self.url, json=body)
            response.raise_for_status()
            data = response.json()
        if "message" in data:
            return str(data["message"].get("content", ""))
        if "choices" in data and data["choices"]:
            return str(data["choices"][0].get("message", {}).get("content", ""))
        return str(data.get("response", ""))
