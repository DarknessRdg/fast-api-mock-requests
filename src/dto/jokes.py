from pydantic import BaseModel


class ResponseDto(BaseModel):
    pass


class JokeResponseDto(ResponseDto):
    joke: str
