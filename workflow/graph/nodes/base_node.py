from abc import ABC,abstractmethod
from pydantic import BaseModel
from typing import TypedDict

class BaseNode(ABC):
    @abstractmethod
    def execute(self,state:BaseModel|TypedDict):
        pass