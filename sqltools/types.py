from enum import Enum, auto

class State(Enum):
    ROOT = auto()
    SELECT = auto()
    WHERE = auto()
    FROM = auto()
    GROUP_BY = auto()
    ORDER_BY = auto()
    LIMIT = auto()
    HAVING = auto()
    COL = auto()
    OP = auto()
    AGG = auto()
    TERMINAL = auto()
    TABLE = auto()
    LOGIC = auto()
    NONE = auto()
    IUE = auto()    

class Seq(Enum):
    copy = auto()
    copyandchange = auto()
    remove = auto()