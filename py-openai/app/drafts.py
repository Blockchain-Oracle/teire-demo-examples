"""Reply drafts for the support queue, on the OpenAI Python SDK."""

from openai import OpenAI

MODEL = "gpt-4o-mini"

_client: OpenAI | None = None


def configure(api_key: str, api_base: str | None = None) -> None:
    """Build the shared client; 1.x removed 0.28's module-level openai.api_key/openai.api_base."""
    global _client
    # max_retries=0 keeps 0.28's default of never retrying a failed request.
    if api_base:
        _client = OpenAI(api_key=api_key, base_url=api_base, max_retries=0)
    else:
        _client = OpenAI(api_key=api_key, max_retries=0)


def _configured_client() -> OpenAI:
    if _client is None:
        raise RuntimeError("configure() must be called before drafting")
    return _client


def draft_reply(ticket: str, tone: str = "friendly") -> str:
    client = _configured_client()
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": f"Write a short, {tone} reply to a customer."},
            {"role": "user", "content": ticket},
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()


def classify(ticket: str) -> str:
    client = _configured_client()
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": f"One word category for: {ticket}"}],
        max_tokens=3,
    )
    return response.choices[0].message.content.strip().lower()
