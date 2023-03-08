#!/usr/bin/python3
"""Define the amenity class"""

from models.base_model import BaseModel
import uuid


class Amenity(BaseModel):
    """Represents an amenity

    Attributes:
        name (str): state name
    """
    name = ""
