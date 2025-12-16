from pydantic import BaseModel


class ExampleRequest(BaseModel):
    """Request model for creating an example"""

    name: str
    description: str


class ExampleResponse(BaseModel):
    """Response model for example"""

    id: int
    name: str
    description: str

    class Config:
        from_attributes = True
