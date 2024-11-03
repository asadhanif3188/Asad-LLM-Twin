import time
from abc import ABC, abstractmethod
from tempfile import mkdtemp

from db.documents import BaseDocument


class BaseCrawler(ABC):
    model: type[BaseDocument]