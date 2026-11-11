"""Reply drafts for the support queue, on the OpenAI Python SDK."""

from openai import OpenAI

MODEL = "gpt-4o-mini"

_client: OpenAI | None = None


def configure(api_key: str, api_base: str | None = None) -> None:
    global _client
    _client = OpenAI(api_key=api_key, base_url=api_base)


def _drafting_client() -> OpenAI:
    """The configured client, or one built from the environment."""
    if _client is None:
        return OpenAI()
    return _client


def draft_reply(ticket: str, tone: str = "friendly") -> str:
    response = _drafting_client().chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": f"Write a short, {tone} reply to a customer."},
            {"role": "user", "content": ticket},
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()


def classify(ticket: str) -> str:
    response = _drafting_client().chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": f"One word category for: {ticket}"}],
        max_tokens=3,
    )
    return response.choices[0].message.content.strip().lower()
