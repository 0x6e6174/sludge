from enum import Enum 

class Method(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"

    method: str 

    def __new__(cls, method):
        obj = object.__new__(cls)
        obj.method = method 
        return obj 

    def __str__(self): 
        return self.method
