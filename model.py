import asyncio
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains.qa_with_sources.retrieval import RetrievalQAWithSourcesChain

from data_ingestion.utils.utils import create_vector_store_response
from data_ingestion.vector_db import get_vector_store


llm = ChatOpenAI(model = "gpt-4o-mini", temperature = 0.8, max_tokens = 1024)
vector_store = get_vector_store()
retriever = vector_store.as_retriever()

chain = RetrievalQAWithSourcesChain.from_llm(llm = llm, retriever = retriever)
print("Got llm, vector store, and chain!")

async def generate_response(query):
    llm_response = chain.ainvoke({"question": query}, return_only_outputs = True)
    vector_store_response = vector_store.asimilarity_search_with_score(query)

    print("Waiting for response generation...")

    answer, docs = await asyncio.gather(llm_response, vector_store_response)
    print("Got the response!")

    metadata = create_vector_store_response(docs)
    print("Metadata created!")

    return answer["answer"], metadata
