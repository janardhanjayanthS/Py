from pydantic import BaseModel, Field


class Query(BaseModel):
    """
    pydantic model for user query
    """

    query: str = Field(min_length=1)
