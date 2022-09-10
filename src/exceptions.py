from fastapi import status


class BusinessException(Exception):
    def __init__(
        self,
        message: str = "Internal Server error",
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    ):
        self.message = message
        self.status_code = status_code

        super().__init__(self.message)
