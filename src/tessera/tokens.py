from enum import Enum, auto #importuje enum klasu koju koristimo da obelezimo sve vrste tokena
from dataclasses import dataclass #dekorator i generisanje boilerplace funkcija
                                  #__eq__(), __init__(), etc..

class TokenType(Enum):
    # kljucne reci
    DEF = auto()
    RETURN = auto()
    CONST = auto()
    IF = auto()
    ELIF = auto()
    ELSE = auto()
    WHILE = auto()
    FOR = auto()
    BREAK = auto()
    CONTINUE = auto()
    AND = auto()
    OR = auto()
    NOT = auto()
    TRUE = auto()
    FALSE = auto()
    INT_KW = auto()
    FLOAT_KW = auto()
    BOOL_KW = auto()
    VOID_KW = auto()

    # literali i imena
    INT_LIT = auto()
    FLOAT_LIT = auto()
    IDENT = auto()
    HOLE = auto()

    # operatori
    PLUS = auto()      # +
    MINUS = auto()     # -
    MUL = auto()       # *
    DIV = auto()       # /
    MOD = auto()       # %
    EQ = auto()        # =
    EQ_EQ = auto()     # ==
    NOT_EQ = auto()    # !=
    LT = auto()        # <
    LT_EQ = auto()     # <=
    GT = auto()        # >
    GT_EQ = auto()     # >=
    ARROW = auto()     # ->

    # interpunkcija
    LPAREN = auto()    # (
    RPAREN = auto()    # )
    LCURLY = auto()    # {
    RCURLY = auto()    # }
    COMMA = auto()     # ,
    SEMI = auto()      # ;

    # kraj ulaza
    EOF = auto()

@dataclass(frozen=True) #frozen daje da nakon sto se napravi instanca ne moze da se menja
class Token:
    kind: TokenType #token se sastoji od type-a odnosno kind
    text: str #samog teksta
    line: int #linije na kojoj se nalazi
    column: int #i pozicije u liniji odnosno kolona

KEYWORDS = { #recnik/mapa kljucnih reci iz source koda koja ih povezuje sa tipom
    "def": TokenType.DEF,
    "return": TokenType.RETURN,
    "const": TokenType.CONST,
    "if": TokenType.IF,
    "elif": TokenType.ELIF,
    "else": TokenType.ELSE,
    "while": TokenType.WHILE,
    "for": TokenType.FOR,
    "break": TokenType.BREAK,
    "continue": TokenType.CONTINUE,
    "and": TokenType.AND,
    "or": TokenType.OR,
    "not": TokenType.NOT,
    "True": TokenType.TRUE,
    "False": TokenType.FALSE,
    "int": TokenType.INT_KW,
    "float": TokenType.FLOAT_KW,
    "bool": TokenType.BOOL_KW,
    "void": TokenType.VOID_KW,
}

SINGLE_CHAR_TOKENS = {
    "+": TokenType.PLUS,
    "-": TokenType.MINUS,
    "*": TokenType.MUL,
    "/": TokenType.DIV,
    "%": TokenType.MOD,
    "=": TokenType.EQ,
    "<": TokenType.LT,
    ">": TokenType.GT,
    "(": TokenType.LPAREN,
    ")": TokenType.RPAREN,
    "{": TokenType.LCURLY,
    "}": TokenType.RCURLY,
    ",": TokenType.COMMA,
    ";": TokenType.SEMI,
}

TWO_CHAR_TOKENS = {
    "->": TokenType.ARROW,
    "==": TokenType.EQ_EQ,
    "!=": TokenType.NOT_EQ,
    "<=": TokenType.LT_EQ,
    ">=": TokenType.GT_EQ,
}
