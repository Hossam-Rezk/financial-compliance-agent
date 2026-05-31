import json
from datetime import datetime
from src.stores.llm.OllamaProvider import OllamaProvider
from src.stores.rules.RulesProvider import get_rules


class ReportGeneratorAgent:

    def __init__(self):
        self.ollama = OllamaProvider()

    async def run(
        self,
        query: str,
        project_id: str,
        scored_findings: list[dict],
    ) -> dict:
        severity_summary = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}
        for f in scored_findings:
            level = f.get("severity", "Low")
            if level in severity_summary:
                severity_summary[level] += 1

        if severity_summary["Critical"] > 0:
            overall_risk = "Critical"
        elif severity_summary["High"] > 0:
            overall_risk = "High"
        elif severity_summary["Medium"] > 0:
            overall_risk = "Medium"
        elif severity_summary["Low"] > 0:
            overall_risk = "Low"
        else:
            overall_risk = "None"

        if scored_findings:
            system_prompt = (
                "You are a compliance report writer. Write a concise executive "
                "summary (3-5 sentences) for a compliance review. Be factual, "
                "professional, and direct. Return only the summary text, no "
                "headings, no bullet points, no markdown."
            )

            findings_block = json.dumps(scored_findings, indent=2)
            user_prompt = f"""
The following compliance findings were identified for project '{project_id}':
{findings_block}

Overall risk level: {overall_risk}

Write a 3-5 sentence executive summary suitable for a compliance officer.
"""
            executive_summary = await self.ollama.generate(
                prompt=user_prompt,
                system_prompt=system_prompt,
            )
        else:
            executive_summary = (
                "No compliance violations or risks were identified in the "
                "reviewed document excerpts. The content appears to be "
                "consistent with the applicable compliance rules."
            )

        return {
            "project_id": project_id,
            "query": query,
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "total_findings": len(scored_findings),
            "severity_summary": severity_summary,
            "overall_risk": overall_risk,
            "executive_summary": executive_summary.strip(),
            "findings": scored_findings,
        }
