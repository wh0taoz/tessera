import sys
from pathlib import Path

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

    #ni u jendnom trenutku se ne menja ch da ukoliko jedan test fail-uje ostane konzistentnost
    def tokenize(self):
        tokens = []
        while not self.at_end():
            ch = self.current()

            if ch.isspace(): #isspace gleda space, tab, etc...
                self.advance() #ignorisemo whitespace
                continue

            if ch.isdigit(): #provera za int i float literale
                line = self.line
                column = self.column
                start = self.pos
                while self.current().isdigit():
                    self.advance()
                kind = TokenType.INT_LIT
                if self.current() == '.' and self.peek().isdigit():
                    self.advance()
                    while self.current().isdigit():
                        self.advance()
                    kind = TokenType.FLOAT_LIT
                tokens.append(Token(kind, self.source[start:self.pos], line, column))
                continue

            if ch.isalpha() or ch == "_": #provera za kljucne reci i ident
                line = self.line
                column = self.column
                start = self.pos
                while self.current().isalnum() or self.current() == "_":
                    self.advance()
                word = self.source[start:self.pos]
                kind = KEYWORDS.get(word, TokenType.IDENT) #lookup gde je drugi argument default ukoliko ne nadje word
                tokens.append(Token(kind, word, line, column))
                continue

            pair = ch + self.peek() #provera za poredjenja; prvo probamo duzi token da li postoji
            if pair in TWO_CHAR_TOKENS:
                line = self.line
                column = self.column
                self.advance()
                self.advance()
                tokens.append(Token(TWO_CHAR_TOKENS[pair], pair, line, column))
                continue

            if ch in SINGLE_CHAR_TOKENS: #provera za poredjenja
                line = self.line
                column = self.column
                self.advance()
                tokens.append(Token(SINGLE_CHAR_TOKENS[ch], ch, line, column))
                continue
            if ch == "?":
                line = self.line
                column = self.column
                start = self.pos
                self.advance()
                while self.current().isalnum() or self.current() == "_":
                    self.advance()
                tokens.append(Token(TokenType.HOLE, self.source[start:self.pos], line, column))
                continue

            if ch == "#":
                while not self.at_end() and self.current() != '\n':
                    self.advance()
                continue

            raise LexError(f"unknown char {ch!r} at line {self.line} in column {self.column}") #!r samo daje da je char u navodnicima
        tokens.append(Token(TokenType.EOF, "", self.line, self.column)) #nakon sto prodjemo kroz source dodajemo end of file token u nasu listu tokena
        return tokens


#pokrece se samo kad se fajl pokrene direktno: python src/tessera/lexer.py examples/max.tsr
#generisano pomocu claude-a
if __name__ == "__main__":
    source = Path(sys.argv[1]).read_text(encoding="utf-8")
    for t in Lexer(source).tokenize():
        print(f"{t.line}:{t.column}\t{t.kind.name:<10} {t.text!r}")