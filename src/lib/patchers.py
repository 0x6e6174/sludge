from .response import Response 

from typing import Callable, List

type Patcher = Callable[[Response, 'Request'], Response]

patchers: List[Patcher] = [
]
