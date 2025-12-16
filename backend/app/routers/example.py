from fastapi import APIRouter

from backend.app.models.example import ExampleRequest, ExampleResponse

router = APIRouter()


@router.get("/", response_model=list[ExampleResponse])
async def get_examples():
    """Get all examples"""
    return [
        ExampleResponse(id=1, name="Example 1", description="First example"),
        ExampleResponse(id=2, name="Example 2", description="Second example"),
    ]


@router.post("/", response_model=ExampleResponse)
async def create_example(example: ExampleRequest):
    """Create a new example"""
    # This is a placeholder - implement your logic here
    return ExampleResponse(id=1, name=example.name, description=example.description)


@router.get("/{example_id}", response_model=ExampleResponse)
async def get_example(example_id: int):
    """Get a specific example by ID"""
    return ExampleResponse(
        id=example_id,
        name=f"Example {example_id}",
        description=f"Description for example {example_id}",
    )
