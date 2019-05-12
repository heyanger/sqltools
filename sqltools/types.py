from enum import Enum, auto

class State(Enum):
    ROOT = auto()
    SELECT = auto()
    WHERE = auto()
    GROUP = auto()
    ORDER = auto()
    LIMIT = auto()
    HAVING = auto()
    COL = auto()
    OP = auto()
    AGG = auto()
    TERMINAL = auto()

    
