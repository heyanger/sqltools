from sqltools.tree import *
from sqltools.types import *
from sqltools.utils import *

class Serializer:
    @staticmethod
    def serialize(node):
        if node is None:
            return ""

        if node.value is not None:
            str = node.type.name + '[' + node.value + ']'
        else:
            str = node.type.name

        if len(node.children) != 0:
            str = str + '('

        for idx, c in enumerate(node.children):
            str = str + Serializer.serialize(c)
            if idx < len(node.children) - 1:
                str = str + ','

        if len(node.children) != 0:
            str = str + ')'

        return str

    @staticmethod
    def deserialize(str):
        rest = str.find('(')
        if rest == -1:
            rest = len(str)
        valuel = str[:rest].find('[')
        valuer = str[:rest].rfind(']')

        if valuel == -1 or valuer == -1:
            root = TreeNode(Serializer.getState(str[:rest]))
        else:
            root = TreeNode(Serializer.getState(str[:valuel]), value=str[valuel+1:valuer])

        content = Serializer.smart_split(remove_front_parenthesis(str), ',')
        if len(content) == 1 and content[0] == str:
            return root

        for c in content:
            root.children.append(Serializer.deserialize(c))

        return root

    def getState(str):
        if str == "ROOT":
            return State.ROOT
        elif str == "NONE":
            return State.NONE
        elif str == "SELECT":
            return State.SELECT
        elif str == "WHERE":
            return State.WHERE
        elif str == "COL":
            return State.COL
        elif str == "GROUP BY":
            return State.GROUP_BY
        elif str == "TERMINAL":
            return State.TERMINAL
        elif str == "LIMIT":
            return State.LIMIT
        elif str == "AGG":
            return State.AGG
        elif str == "OP":
            return State.OP
        elif str == "ORDER BY":
            return State.ORDER_BY
        elif str == "HAVING":
            return State.HAVING

    def smart_split(str, splitter):
        paren_count = 0
        bracket_count = 0
        start = 0
        end = 0
        strlist = []

        for end in range(len(str)):
            if str[end] == '(':
                paren_count += 1
            elif str[end] == ')':
                paren_count -= 1
            elif str[end] == '[':
                bracket_count += 1
            elif str[end] == ']':
                bracket_count -= 1
            elif str[end] == splitter and paren_count == 0 and bracket_count == 0:
                strlist.append(str[start:end])
                start = end + 1

        strlist.append(str[start:end+1])
        return strlist
