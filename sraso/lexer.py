from enum import Enum

class TokenType(Enum):
    TOKEN_WORD = 'TOKEN_WORD'
    TOKEN_PIPE = 'TOKEN_PIPE'
    TOKEN_COLON = 'TOKEN_COLON'
    TOKEN_COMMA = 'TOKEN_COMMA'
    TOKEN_LPAREN = 'TOKEN_LPAREN'
    TOKEN_RPAREN = 'TOKEN_RPAREN'
    TOKEN_EQUALS = 'TOKEN_EQUALS'
    TOKEN_NUMBER = 'TOKEN_NUMBER'
    TOKEN_LBRACE = 'TOKEN_LBRACE'
    TOKEN_RBRACE = 'TOKEN_RBRACE'
    TOKEN_STRING = 'TOKEN_STRING'
    TOKEN_LBRACKET = 'TOKEN_LBRACKET'
    TOKEN_RBRACKET = 'TOKEN_RBRACKET'
    TOKEN_SEMICOLON = 'TOKEN_SEMICOLON'


class Lexer:
    def __init__(self, text):
        self.text = text
        self.index = 0
        self.text = text
        self.tokens = []

    def lex(self):
        while self.index < len(self.text):
            self.tokenize()
            self.next()
        return self.tokens

    def next(self):
        self.index += 1

    def curr(self):
        return self.text[self.index]

    def ahead(self):
        return self.text[self.index + 1]

    def tokenize(self):
        while self.curr() == ' ':
            self.next()

        pos_start = self.index

        if self.curr() == ',':
            return self.tokens.append({
            'type': TokenType.TOKEN_COMMA,
            'value': self.curr()
            })
        elif self.curr() == ';':
            return self.tokens.append({
            'type': TokenType.TOKEN_SEMICOLON,
            'value': self.curr()
            })
        elif self.curr() == ':':
            return self.tokens.append({
            'type': TokenType.TOKEN_COLON,
            'value': self.curr()
            })
        elif self.curr() == '=':
            return self.tokens.append({
            'type': TokenType.TOKEN_EQUALS,
            'value': self.curr()
            })
        elif self.curr() == '[':
            return self.tokens.append({
            'type': TokenType.TOKEN_LBRACKET,
            'value': self.curr()
            })
        elif self.curr() == ']':
            return self.tokens.append({
            'type': TokenType.TOKEN_RBRACKET,
            'value': self.curr()
            })
        elif self.curr() == '{':
            return self.tokens.append({
            'type': TokenType.TOKEN_LBRACE,
            'value': self.curr()
            })
        elif self.curr() == '}':
            return self.tokens.append({
            'type': TokenType.TOKEN_RBRACE,
            'value': self.curr()
            })
        elif self.curr() == '(':
            return self.tokens.append({
            'type': TokenType.TOKEN_LPAREN,
            'value': self.curr()
            })
        elif self.curr() == ')':
            return self.tokens.append({
            'type': TokenType.TOKEN_RPAREN,
            'value': self.curr()
            })

        if self.curr() == '"' or self.curr() == "'":
            quote_type = self.curr()
            self.next()
            while self.curr() != quote_type and self.index < len(self.text):
                self.next()

            if self.curr() == quote_type:
                return self.tokens.append({
                'type': TokenType.TOKEN_STRING,
                'value': self.text[pos_start + 1:self.index]
                })
            else:
                raise Exception('unclosed string')

        if self.curr().isdigit():
            while self.index + 1 < len(self.text) and self.ahead().isdigit():
                self.next()

            return self.tokens.append({
            'type': TokenType.TOKEN_NUMBER,
            'value': int(self.text[pos_start:self.index + 1])
            })

        if self.curr().isalpha():

            while self.index + 1 < len(self.text) and self.ahead().isalpha():
                self.next()

            return self.tokens.append({
            'type': TokenType.TOKEN_WORD,
            'value': self.text[pos_start:self.index + 1]
            })