from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from typing import List
from fastapi import FastAPI
from langserve import add_routes
from langserve import RemoteRunnable


import os
import getpass


os.environ['OPENAI_API_KEY'] = "sk-proj-xCb9h2MQc4zewTS06RbWT3BlbkFJfOPKAe6IZ6L1ylNB7BXV"


systemTemplate = "Translate the following into {language} :"
prompt_template = ChatPromptTemplate.from_messages([
    ('system', systemTemplate),
    ('user','text')
])

model = ChatOpenAI()

parser = StrOutputParser()

chain = prompt_template | model | parser

app = FastAPI(
    title="Langchain server",
    version="1.0",
    description="A simple API server using LangChain's Runnable Interface"
)

add_routes(
    app,
    chain,
    path="/chain",
)


if __name__ == "__main__":

    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
    remote_chain = RemoteRunnable("http://localhost:8000/chain/")
    remote_chain.invoke({"language": "italian", "text": "hi"})
