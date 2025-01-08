from typing import List
from pydantic import BaseModel, Field


class Question(BaseModel):
    question_type: str = Field(description="The type of question (Factual, Conceptual, Analytical).")
    question: str = Field(description="The question generated.")
    answer: str = Field(description="The answer of the question.")
    reference: str = Field(description="The reference text in the article from where the answer is generated.")
    

class QuestionAnswers(BaseModel):
    questions: List[Question] = Field(description="Set of questions generated")



prompt = """
I will provide an article text. Please analyze it in the following way:

1. First identify and list the key topics and main points of the article.

2. Then generate 5-8 questions that:
   - Cover different aspects of understanding (factual, conceptual, analytical)
   - Are arranged from simpler to more complex understanding
   - Include a mix of:
     * Factual questions about specific information
     * Conceptual questions about main ideas
     * Questions that connect different parts of the article
     * Questions that relate the content to broader implications

3. For each question:
   - Provide the correct answer
   - Indicate what type of understanding it tests
   - Include the relevant section of text that contains the answer

Format your response like this:

KEY TOPICS:
- Topic 1
- Topic 2
[etc.]

QUESTIONS:

1. [Question Type: Factual]
Q: [Question text]
A: [Answer]
Reference: "[relevant text from article]"

2. [Question Type: Conceptual]
[etc.]

Please ensure the questions are clear, unambiguous, and directly answerable from the article content.

Article text:

{article_text}

"""