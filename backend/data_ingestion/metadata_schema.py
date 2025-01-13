from pydantic import BaseModel
from typing import List


class ArticleMetadata(BaseModel):
    article_link: str
    article_title: str
    article_image_url: str
    article_publication_date: str