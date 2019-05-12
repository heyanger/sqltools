from enum import Enum, auto

class State(Enum):
    ROOT = auto()
    SELECT = auto()
    WHERE = auto()
    GROUP = auto()
    ORDER = auto()

    IUEN = auto()
    KW = auto()
    COL = auto()
    OP = auto()
    AGG = auto()
    TERMINAL = auto()
    LOGIC = auto()
    DAL = auto()
    HAVING = auto()
    
