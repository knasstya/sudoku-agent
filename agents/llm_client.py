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
            temperature=0,
            api_key=api_key,
            timeout=30, 
            max_retries=1,  
            reasoning_effort="low", 
            max_tokens=600,  
        )
        
    return _llm
