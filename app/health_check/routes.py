from fastapi import APIRouter

description = """
# Health check 
this rout purpose is to check the healt of the api
"""

router = APIRouter(
    prefix="/",
    tags=["health_check"],
    responses={
        200: {
            "description": description
        }
    }
)


@router.get("/")
def health_check():
    return {
        "message": "hello world"
    }
