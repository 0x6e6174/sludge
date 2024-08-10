from enum import Enum 

class ResponseCode(Enum):
    OK = (200, "OK")
    CREATED = (201, "Created")
    ACCEPTED = (202, "Accepted")
    NO_CONTENT = (204, "No Content")
    MOVED_PERMANENTLY = (301, "Moved Permanently")
    FOUND = (302, "Found")
    BAD_REQUEST = (400, "Bad Request")
    UNAUTHORIZED = (401, "Unauthorized")
    FORBIDDEN = (403, "Forbidden")
    NOT_FOUND = (404, "Not Found")
    METHOD_NOT_ALLOWED = (405, "Method Not Allowed")
    INTERNAL_SERVER_ERROR = (500, "Internal Server Error")
    NOT_IMPLEMENTED = (501, "Not Implemented")
    SERVICE_UNAVAILABLE = (503, "Service Unavailable")

    code: str
    message: int

    def __new__(cls, code, message):
        obj = object.__new__(cls)
        obj.code = code
        obj.message = message
        return obj

    def __str__(self):
        return f"{self.code} {self.message}"

    @classmethod
    def _missing_(cls, value):
        for member in cls:
            if member.code == value:
                return member
        return None

