#!/usr/bin/python3
"""Define the state class"""

import uuid
from models.base_model import BaseModel


class State(BaseModel):
    """Represents a state

    Attributes:
        name (str): state name
    """
    name = ""
