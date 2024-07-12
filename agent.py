from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub

from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
import bs4

import json

load_dotenv()
gpt = ChatOpenAI(model="gpt-3.5-turbo")

# query = """
# Vou viajar para Londres em agosto de 2024. 
# Quero que faça um roteiro de viagem para mim com eventos que irão ocorrer na data da viagem e com o preço da passagem de São Paulo para Londres em dólares.
# """

def researchAgent(query, llm):
    tools = load_tools(['ddg-search', 'wikipedia'], llm=llm)
    prompt = hub.pull('hwchase17/react')

    agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, prompt=prompt) # verbose=False
    web_context = agent_executor.invoke({"input": query})
    
    return web_context['output']

# print(researchAgent(query, gpt))

def loadData(): 
    web_paths = [
        "https://www.dicasdeviagem.com/inglaterra",
        "https://www.dicasdeviagem.com/alemanha",  
        "https://www.dicasdeviagem.com/portugal",
        "https://www.dicasdeviagem.com/brasil",
        "https://www.dicasdeviagem.com/caribe/"
    ]
    
    loader = WebBaseLoader(
        web_paths=web_paths,
        bs_kwargs=dict(parse_only=bs4.SoupStrainer(class_=("postcontentwrap", "pagetitleloading background-imaged loading-dark")))
    )
    
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    
    vectorStore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())
    
    retriever = vectorStore.as_retriever()
    return retriever

def getRelevantDocs(query):
    retriever = loadData()
    
    relevant_documents = retriever.invoke(query)   
    return relevant_documents

def supervisorAgent(query, llm, webContext, relevant_documents):
    prompt_template = """
    Você é um gerente de uma agência de viagens. Sua resposta final deverá ser um roteiro de viagem completo e detalhado.
    Utilize o contexto de eventos e preços de passagens, o input do usuário e também os documentos importantes para elaborar o roteiro.
    Contexto: {webContext}
    Documento relevantes: {relevant_documents}
    Usuário: {query}
    Assistente:
    """
    
    prompt = PromptTemplate(
        input_variables=['webContext', 'relevant_documents', 'query'],
        template=prompt_template
    )
    
    sequence = RunnableSequence(prompt | llm)
    response = sequence.invoke({"webContext": webContext, "relevant_documents": relevant_documents, "query": query})
    
    return response

def getResponse(query, llm):
    webContext = researchAgent(query, llm)
    
    relevant_documents = getRelevantDocs(query)
    
    response = supervisorAgent(query, llm, webContext, relevant_documents)
    
    return response

# print(getResponse(query, gpt).content)

def lambdaHandler(event, context):
    # query = event.get("question")
    
    body = json.loads(event.get('body', {}))
    
    query = body.get('question', 'question parameter not recognized')
    response = getResponse(query, gpt).content
    
    print(response)
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",  # Permitir todos os domínios, ajuste conforme necessário
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type"
        },
        "body": json.dumps ({
            "message": "Task completed succesfuly",
            "details": response,
        }, indent=4)
    }
    