from langchain.chains.qa_with_sources.retrieval import RetrievalQAWithSourcesChain
from backend.model.llm import LLMManager

class ChainManager():
    def __init__(self):
        llm_manager = LLMManager()
        self.llm = llm_manager.get_llm()
        self.retriever = llm_manager.get_retriever()
        self.chain = RetrievalQAWithSourcesChain.from_llm(llm=self.llm, retriever=self.retriever)

    def get_chain(self):
        return self.chain