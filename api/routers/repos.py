from fastapi import APIRouter, HTTPException


router = APIRouter(
    tags=["repos"],
)


@router.get("/top100")
async def repos_top100_list():
    pass


@router.get("{owner}/{repo}/activity")
async def repo_activity():
    pass

