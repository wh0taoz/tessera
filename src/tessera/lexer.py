from tessera.tokens import TokenType, Token, KEYWORDS, SINGLE_CHAR_TOKENS, TWO_CHAR_TOKENS

class LexError(Exception):
    pass

class Lexer:
    #inicijalizuje pocetne vrednosti pozicije, reda i kolone
    def __init__(self, source):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1

    #proverava da li smo stigli do kraja 
    def at_end(self):
        return self.pos >= len(self.source) #vraca da li smo stigli do kraja source-a

    #koji je trenutni karakter na kojem smo
    def current(self):
        if self.at_end():
            return ""
        return self.source[self.pos]

    #nastavi dalje samo ukoliko nismo vec na kraju, uz obradu kraja reda
    def advance(self):
        if self.at_end():
            return
        current_char = self.current()
        if current_char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        self.pos += 1

    #koji je sledeci, ali samo ako sledeci nije kraj
    def peek(self):
        if self.pos+1 >= len(self.source):
            return ""
        return self.source[self.pos+1]

    def tokenize(self):
        tokens = []
        while not self.at_end():
            ch = self.current()

            if ch.isspace(): #isspace gleda space, tab, etc...
                self.advance() #ignorisemo whitespace
                continue

            if ch.isdigit():
                line = self.line
                column = self.column
                start = self.pos
                while self.current().isdigit():
                    self.advance()
                tokens.append(Token(TokenType.INT_LIT, self.source[start:self.pos], line, column))
                continue

            if ch.isalpha() or ch == "_":
                line = self.line
                column = self.column
                start = self.pos
                while self.current().isalnum() or self.current() == "_":
                    self.advance()
                word = self.source[start:self.pos]
                kind = KEYWORDS.get(word, TokenType.IDENT) #lookup gde je drugi argument default ukoliko ne nadje word
                tokens.append(Token(kind, word, line, column))
                continue

            pair = ch + self.peek() #prvo probamo duzi token da li postoji
            if pair in TWO_CHAR_TOKENS:
                line = self.line
                column = self.column
                self.advance()
                self.advance()
                tokens.append(Token(TWO_CHAR_TOKENS[pair], pair, line, column))
                continue

            if ch in SINGLE_CHAR_TOKENS: #ako ne proveravamo ovo
                line = self.line
                column = self.column
                self.advance()
                tokens.append(Token(SINGLE_CHAR_TOKENS[ch], ch, line, column))
                continue

            raise LexError(f"unknown char {ch!r} at line {self.line} in column {self.column}") #!r samo daje da je char u navodnicima
        tokens.append(Token(TokenType.EOF, "", self.line, self.column)) #nakon sto prodjemo kroz source dodajemo end of file token u nasu listu tokena
        return tokens