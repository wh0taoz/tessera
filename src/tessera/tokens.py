from enum import Enum, auto #importuje enum klasu koju koristimo da obelezimo sve vrste tokena

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
