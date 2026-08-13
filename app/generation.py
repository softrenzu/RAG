from app.llm import LLMClient
from app.schemas import Citation, SearchHit


class AnswerGenerator:
    def __init__(self, client: LLMClient):
        self.client = client

    async def generate(self, question: str, hits: list[SearchHit]) -> tuple[str, list[Citation]]:
        citations = []
        context_blocks = []
        for index, hit in enumerate(hits, start=1):
            source_id = f"S{index}"
            context_blocks.append(f"[{source_id}] {hit.title}\n{hit.text}")
            citations.append(Citation(
                source_id=source_id,
                document_id=hit.document_id,
                title=hit.title,
                chunk_index=hit.chunk_index,
                text=hit.text,
            ))
        context = "\n\n".join(context_blocks)
        system = "Use the supplied document context to answer the question. Include source markers such as [S1] where relevant."
        user = f"Question:\n{question}\n\nDocument context:\n{context}"
        answer = await self.client.complete(system, user)
        return answer.strip(), citations
