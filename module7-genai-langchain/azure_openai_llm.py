import os

from langchain_openai import AzureChatOpenAI, ChatOpenAI
from langchain_openai.embeddings import AzureOpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv() 

azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
azure_openai_api_key = os.getenv("AZURE_OPENAI_API_KEY")
azure_openai_api_version = os.getenv("AZURE_OPENAI_API_VERSION")
azure_openai_embedding_deployment = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT")

def create_azure_embedding():   
    embedding=AzureOpenAIEmbeddings(
                    azure_endpoint=azure_openai_endpoint,
                    azure_deployment=azure_openai_embedding_deployment,
                    openai_api_key=azure_openai_api_key,
                    openai_api_version=azure_openai_api_version
    )
    
    return embedding

def create_azure_llm(dep_type="chat", api="azure"):
    """
    Create Azure OpenAI LLM instance
    
    Args:
        dep_type: "chat" or "audio" - determines which deployment to use
        api: "azure" for Azure OpenAI or "openai" for standard OpenAI API
    """
    load_dotenv()

    azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    azure_openai_api_key = os.getenv("AZURE_OPENAI_API_KEY")
    azure_openai_api_version = os.getenv("AZURE_OPENAI_API_VERSION")

    deployment = f"AZURE_OPENAI_{dep_type.upper()}_DEPLOYMENT"
    azure_openai_deployment = os.getenv(deployment)

    if not azure_openai_endpoint or not azure_openai_api_key:
        raise ValueError("Missing Azure OpenAI endpoint or API key in environment variables.")

    if not azure_openai_deployment:
        raise ValueError(f"Missing AZURE_OPENAI_{dep_type.upper()}_DEPLOYMENT in environment variables.")

    print(f"Using {dep_type} deployment: {azure_openai_deployment}")
    print(f"Endpoint: {azure_openai_endpoint}")
    print(f"API Version: {azure_openai_api_version}")

    llm = AzureChatOpenAI(
        api_key=azure_openai_api_key,
        azure_endpoint=azure_openai_endpoint,
        azure_deployment=azure_openai_deployment,
        api_version=azure_openai_api_version,
        temperature=0.9
    )

    return llm