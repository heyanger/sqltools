from enum import Enum

class State(Enum):
    ROOT = 1
    GROUP_BY = 2
    ORDER_BY = 3
    LIMIT = 4
    HAVING = 5
    COL = 6
    OP = 7
    AGG = 8
    TERMINAL = 9
    TABLE = 10
    LOGIC = 11
    NONE = 12
    IUE = 13
    JOIN = 14
    DISTINCT = 15
    SELECT = 16
    WHERE = 17
    FROM = 18

class Seq(Enum):
    copy = 1
    copyandchange = 2
    remove = 3
