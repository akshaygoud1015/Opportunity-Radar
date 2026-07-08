"""Extracts a structured skills list from a raw job description using Claude's
tool use -- this is the agentic-orchestration piece of the project: instead of
parsing free text with regex, we force the model to return a validated schema.
"""

import anthropic

from app.config import settings
from app.schemas import SkillExtractionResult

_EXTRACTION_TOOL = {
    "name": "record_skills",
    "description": "Record the technical skills required or preferred for this job posting.",
    "input_schema": {
        "type": "object",
        "properties": {
            "required_skills": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Technical skills explicitly required (languages, frameworks, tools, platforms).",
            },
            "nice_to_have_skills": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Technical skills listed as a plus/bonus/preferred but not required.",
            },
        },
        "required": ["required_skills", "nice_to_have_skills"],
    },
}


class SkillExtractor:
    def __init__(self, api_key: str | None = None):
        self.client = anthropic.Anthropic(api_key=api_key or settings.anthropic_api_key)

    def extract(self, job_description: str) -> SkillExtractionResult:
        response = self.client.messages.create(
            model=settings.anthropic_model,
            max_tokens=1024,
            tools=[_EXTRACTION_TOOL],
            tool_choice={"type": "tool", "name": "record_skills"},
            messages=[
                {
                    "role": "user",
                    "content": (
                        "Extract the technical skills from this job description. "
                        "Only list concrete technical skills (languages, frameworks, "
                        "databases, cloud platforms, tools) -- not soft skills or "
                        "generic phrases like 'team player'.\n\n"
                        f"Job description:\n{job_description}"
                    ),
                }
            ],
        )

        for block in response.content:
            if block.type == "tool_use" and block.name == "record_skills":
                return SkillExtractionResult(**block.input)

        # Shouldn't happen with tool_choice forcing the tool, but fail loudly
        # rather than silently returning something wrong.
        raise RuntimeError("Claude did not return the expected record_skills tool call")
