import asyncio
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.qa_with_sources.retrieval import RetrievalQAWithSourcesChain

from data_ingestion.utils.utils import create_vector_store_response, retrieve_article_text
from data_ingestion.vector_db import get_vector_store
from model.schema import QuestionAnswers, prompt


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


def generate_questions(article_link):
    print("Generating questions from article link: ", article_link)
    article_text = retrieve_article_text(article_link)
    structured_llm = llm.with_structured_output(QuestionAnswers)
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
    
