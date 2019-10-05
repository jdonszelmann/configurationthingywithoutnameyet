from typing import TextIO

from lark import Lark, Token, Transformer, v_args
from lark.indenter import Indenter
from lark.tree import Tree
from functools import partial


class EXTENDS:
    pass

class ConfigIndenter(Indenter):
    NL_type = '_NEWLINE'
    OPEN_PAREN_types = ['LPAR', 'LSQB', 'LBRACE']
    CLOSE_PAREN_types = ['RPAR', 'RSQB', 'RBRACE']
    INDENT_type = '_INDENT'
    DEDENT_type = '_DEDENT'
    tab_len = 4


class TreeToConfig(Transformer):
    @v_args(inline=True)
    def string(self, s):
        return s[1:-1].replace('\\"', '"')

    def block(self, s):
        name = s[0]
        res = {}
        for item in s[1:]:
            if isinstance(item, Tree) and item.data == "extends":
                res[item.children[0]] = EXTENDS
            else:
                res[item[0]] = item[1]
        return [name, res]

    def map(self, s):
        res = {}
        for item in s:
            if isinstance(item, Tree) and item.data == "extends":
                res[item] = None
            else:
                res[item[0]] = item[1]
        return res

    input = map
    pair = tuple
    list = list
    line = tuple
    FLOAT_NUMBER = float
    BIN_NUMBER = partial(int, base=2)
    OCT_NUMBER = partial(int, base=8)
    DEC_NUMBER = partial(int, base=10)
    HEX_NUMBER = partial(int, base=16)
    NAME = str
    none = lambda self, _: None
    boolean = bool


def find_key(config: dict, key_to_find):

    for key, value in config.items():
        if key == key_to_find:
            return value

        if isinstance(value, dict):
            res = find_key(value, key_to_find)
            if res:
                return res
    return None

def apply_extends(config: dict, origconfig=None):
    if origconfig == None:
        origconfig = config

    scopes_to_import = []

    for key, value in dict(config).items():
        if value == EXTENDS:
            scope = find_key(origconfig, key)
            scopes_to_import.append(scope)
            del config[key]

        if isinstance(value, dict):
            apply_extends(value, origconfig=origconfig)

    for scope in scopes_to_import:
        for key, value in scope.items():
            if key not in config:
                config[key] = value

    return config


def loads(string: str):
    parser = Lark.open(
        'grammar.lark',
        parser='lalr',
        rel_to=__file__,
        postlex=ConfigIndenter(),
        start='input',
    )
    ast = parser.parse(string)
    config = TreeToConfig(visit_tokens=True).transform(ast)
    return apply_extends(config)


def load(file: TextIO):
    contents = file.read()
    return loads(file)


if __name__ == "__main__":
    pass
