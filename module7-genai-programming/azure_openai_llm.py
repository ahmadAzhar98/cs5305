import os

from langchain_openai import AzureChatOpenAI
from langchain.messages import HumanMessage

from dotenv import load_dotenv

load_dotenv()

def create_azure_llm(
    deployment_name: str = "gpt-4o-mini",
    temperature: float = 0.1,
):
    azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    azure_openai_api_key = os.getenv("AZURE_OPENAI_API_KEY")
    azure_openai_api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-08-01-preview")

    if not azure_openai_endpoint or not azure_openai_api_key:
        raise ValueError("Missing Azure OpenAI endpoint or API key in environment variables.")

    llm = AzureChatOpenAI(
        api_key=azure_openai_api_key,
        azure_endpoint=azure_openai_endpoint,
        azure_deployment=deployment_name,
        api_version=azure_openai_api_version,
        temperature=temperature,
    )
    return llm