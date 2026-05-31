import json
from src.stores.llm.OllamaProvider import OllamaProvider
from src.stores.rules.RulesProvider import get_rules


class ComplianceCheckerAgent:

    def __init__(self):
        self.ollama = OllamaProvider()

    async def run(self, chunks: list[dict]) -> list[dict]:
        rules = get_rules()

        rules_block = "\n".join(f"- {rule}" for rule in rules)
        chunks_block = "\n\n".join(
            f"[Chunk {c['chunk_order']}]: {c['chunk_text']}" for c in chunks
        )

        system_prompt = (
            "You are a financial compliance expert. Your job is to review "
            "document excerpts and identify violations or risks against a "
            "given set of compliance rules. Be precise and conservative — "
            "only flag genuine concerns, not speculative ones. "
            "Always respond with valid JSON only, no explanation outside the JSON."
        )

        user_prompt = f"""
You are given the following compliance rules:
{rules_block}

And the following document excerpts:
{chunks_block}

For each compliance rule that is violated or at risk based on the excerpts,
return a JSON array of objects with this exact structure:
{{
  "rule": "<the exact rule text>",
  "finding": "<one sentence explaining what in the document violates or risks this rule>",
  "chunk_text": "<the exact chunk text that triggered this finding>",
  "chunk_order": <the chunk order number as an integer>
}}

If no violations are found, return an empty JSON array: []
Return only the JSON array, no markdown, no explanation.
"""

        response = await self.ollama.generate(
            prompt=user_prompt,
            system_prompt=system_prompt,
        )

        try:
            findings = json.loads(response.strip())
            if not isinstance(findings, list):
                findings = []
        except json.JSONDecodeError:
            findings = []

        return findings
