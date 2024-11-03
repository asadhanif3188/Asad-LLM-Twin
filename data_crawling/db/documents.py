import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import uuid
from typing import List, Optional

# from errors import ImproperlyConfigured
from pydantic import UUID4, BaseModel, ConfigDict, Field

from pymongo import errors
from data_crawling.utils import get_logger

from mongo import connection 

_database = connection.get_database("scrabble")

logger = get_logger(__name__)

class BaseDocument(BaseModel):
    id: UUID4 = Field(default_factory=uuid.uuid4)

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    @classmethod
    def from_mongo(cls, data: dict):
        """Convert "_id" (str object) into "id" (UUID object)."""
        if not data:
            return data
        
        id = data.pop("_id", None)
        return cls(**dict(data, id=id))
    
    def to_mongo(self, **kwargs) -> dict:
        """Convert "id" (UUID object) into "_id" (str object)."""
        exclude_unset = kwargs.pop("exclude_unset", False)
        by_alias = kwargs.pop("by_alias", True)

        parsed = self.model_dump(
            exclude_unset = exclude_unset,
            by_alias = by_alias,
            **kwargs
        )

        if "_id" not in parsed and "id" in parsed:
            parsed["_id"] = str(parsed.pop("id"))
        
        return parsed
    
    def save(self, **kwargs):
        collection = _database[self._get_collection_name()]

        try:
            result = collection.insert_one(self.to_mongo(**kwargs))
        except errors.WriteError:
            logger.exception("Failed to insert document")
            return None