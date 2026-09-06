"""
Single place that constructs the LLM client. Keeping this separate
means swapping providers (Groq -> OpenAI -> local Ollama) later is a
one-file change, not a find-and-replace across the codebase. This is
a standard practice, not specific to this project.
"""
import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

_llm = None


def get_llm():
    global _llm
    if _llm is None:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError(
                "GROQ_API_KEY not set. Create a .env file with GROQ_API_KEY=your_key"
            )

        _llm = ChatGroq(
            model="openai/gpt-oss-20b",
            temperature=0,  # deterministic reasoning, not creative writing
            api_key=api_key,
            timeout=30,  # fail loudly instead of hanging forever on a slow response
            max_retries=1,  # low retry count so real errors surface fast, not hidden behind silent retries
            reasoning_effort="low",  # gpt-oss models spend tokens on hidden "thinking" by default;
            # low effort keeps enough reasoning for a simple task while leaving room for the actual answer
            max_tokens=600,  # hard cap so one call can't eat the whole per-minute token budget
        )
        
    return _llm
