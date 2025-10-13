from langchain_google_genai import ChatGoogleGenerativeAI
from mcp_kms import config


model = ChatGoogleGenerativeAI(model=config.model, google_api_key=config.google_api_key)
