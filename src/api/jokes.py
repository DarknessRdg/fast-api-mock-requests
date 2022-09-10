from fastapi import APIRouter, Depends

from src.dto.jokes import JokeResponseDto
from src.services.jokes import JokeService

router = APIRouter(prefix='/jokes')


@router.get('/')
def get_joke(service: JokeService = Depends()) -> JokeResponseDto:
    return JokeResponseDto(joke=service.random())
