import os, asyncio
from langchain_core.prompts import ChatPromptTemplate

from model.llm import LLMManager
from model.chains import ChainManager
from model.schema import prompt, QuestionAnswers
from data_ingestion.vector_db import VectorDB
from data_ingestion.utils import retrieve_article_text


class Generator():
    def __init__(self):
        llm_manager = LLMManager()
        chain_manager = ChainManager()
        
        self.vector_db = VectorDB()
        self.llm = llm_manager.get_llm()
        self.chain = chain_manager.get_chain()

    async def generate_response(self, query):
        llm_response = self.chain.ainvoke({"question": query}, return_only_outputs = True)
        
        vector_store_response = self.vector_db.vector_store.asimilarity_search_with_score(query)

        print("Waiting for response generation...")

        answer, docs = await asyncio.gather(llm_response, vector_store_response)
        print("Got the response!")

        metadata = self.vector_db.create_vector_store_response(docs)
        print("Metadata created!")

        return answer["answer"], metadata
    

    def generate_questions(self, article_link):
        print("Generating questions from article link: ", article_link)
        article_text = retrieve_article_text(article_link)
        structured_llm = self.llm.with_structured_output(QuestionAnswers)
        prompt_template = ChatPromptTemplate.from_template(prompt)
        llm_prompt = prompt_template.format(article_text = article_text)
        response = structured_llm.invoke(llm_prompt)

        questions = []
        for index, question in enumerate(response.questions):
            quest = {}
            quest["question_type"] = question.question_type
            quest["question"] = question.question
            quest["answer"] = question.answer
            quest["reference"] = question.reference
            questions.append(quest)
            # print(f"Question #0{index + 1}")
            # print(f"Type: {question.question_type}")
            # print(f"Q: {question.question}")
            # print(f"Ans: {question.answer}")
            # print(f"Ref: {question.reference}\n")
        return questions

