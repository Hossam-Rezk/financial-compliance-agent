import json
from src.stores.llm.OllamaProvider import OllamaProvider


class RiskScorerAgent:

    SEVERITY_LEVELS = ["Critical", "High", "Medium", "Low"]

    def __init__(self):
        self.ollama = OllamaProvider()

    async def run(self, findings: list[dict]) -> list[dict]:
        if not findings:
            return []

        system_prompt = (
            "You are a financial risk assessment specialist. You receive "
            "compliance findings and assign each one a severity level and "
            "a brief rationale. Severity must be exactly one of: "
            "Critical, High, Medium, Low. "
            "Always respond with valid JSON only, no explanation outside the JSON."
        )

        findings_block = json.dumps(findings, indent=2)

        user_prompt = f"""
You are given the following compliance findings:
{findings_block}

For each finding, assign a severity level and a one-sentence rationale.
Severity must be exactly one of: Critical, High, Medium, Low.

Return a JSON array where each object has all the original fields plus:
{{
  "severity": "<Critical | High | Medium | Low>",
  "rationale": "<one sentence explaining the severity assignment>"
}}

Return only the JSON array, no markdown, no explanation.
"""

        response = await self.ollama.generate(
            prompt=user_prompt,
            system_prompt=system_prompt,
        )

        try:
            scored = json.loads(response.strip())
            if not isinstance(scored, list):
                scored = findings
        except json.JSONDecodeError:
            scored = findings

        return scored
