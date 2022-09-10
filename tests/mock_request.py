import requests
from requests import Response, PreparedRequest
from fastapi import status


class MachRequestStrategy:
    def __init__(self, value):
        self.value = value

    def match(self, prep: PreparedRequest) -> bool:
        raise NotImplemented(
            "Implement how it should match with given value "
            "remember to use `self.value` to compare with any "
            "of request attribute"
        )


class MachByMethod(MachRequestStrategy):
    def match(self, prep: PreparedRequest) -> bool:
        return prep.method.upper() == self.value.upper()


class MachByUrl(MachRequestStrategy):
    def match(self, prep: PreparedRequest) -> bool:
        return prep.url == self.value


class MathByBaseUrl(MachRequestStrategy):
    def match(self, prep: PreparedRequest) -> bool:
        return prep.url.startswith(self.value)


class HandleRequest:
    def __init__(
        self,
            method,
            path,
            status_code=status.HTTP_200_OK,
            response_body=None,
            response_encoding="utf-8"
    ):
        self.match_by: list[MachRequestStrategy] = [
            MachByMethod(method),
            MachByUrl(path)
        ]

        self.method = method
        self.path = path
        self._status_code = status_code
        self._response_body = response_body
        self._response_encoding = response_encoding

    def status_code(self, status_code):
        self._status_code = status_code
        return self

    def response_body(self, response_body):
        self._response_body = response_body
        return self

    def response_encoding(self, response_encoding):
        self._response_encoding = response_encoding
        return self

    def add_match_by(self, mach: MachRequestStrategy):
        self.match_by.append(mach)
        return self

    def match(self, prep: PreparedRequest):
        return all(it.match(prep) for it in self.match_by)

    def get_response(self, prepared_request: PreparedRequest) -> Response:
        response = Response()

        response.status_code = self._status_code
        response.url = self.path
        response.request = prepared_request
        response.encoding = self._response_encoding
        response.raw = self._response_body

        return response


class RequestBox(list[Response]):
    def get_request(self, method, path):
        matches_by = [MachByMethod(method), MachByUrl(path)]

        def matches_all(prep):
            return all(map(lambda it: it.match(prep), matches_by))

        found = filter(matches_all, self)
        if found:
            raise ValueError()

        return next(found)


class RequestInterceptor:
    def __init__(self, real_http_send, ignore_by: list[MachRequestStrategy]):
        self.real_http_send = real_http_send

        self.request_box: RequestBox = RequestBox()
        self._handle_box: list[HandleRequest] = []
        self._ignore: list[MachRequestStrategy] = ignore_by

    def handle(self, *args, **kwargs):
        handle = HandleRequest(*args, **kwargs)
        self._handle_box.append(handle)

    def get(self, path):
        return self.handle("GET", path)

    def __call__(self, prep: PreparedRequest, *args, **kwargs) -> Response:
        if self._should_ignore(prep):
            session = requests.Session()
            return self.real_http_send(session, prep, *args, **kwargs)

        handler = self._get_handler(prep)
        response = handler.get_response(prep)
        self.request_box.append(response)
        return response

    def _should_ignore(self, prep: PreparedRequest):
        return any(filter(lambda it: it.match(prep), self._ignore))

    def _get_handler(self, prep: PreparedRequest):
        handle_request = filter(lambda it: it.match(prep), self._handle_box)
        if not any(handle_request):
            raise ValueError(f"No handle prepared for {prep}")

        return next(handle_request)


class RequestBoxAdapter:
    def __init__(self):
        pass

