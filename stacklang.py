import enum

class TokenKind(enum.Enum):
    #Literals
    NUMBER = 1
    STRING = 2
    STRING_CONTINUATION = 3
    IDENTIFIER = 4
    LABEL = 5

class Token:
    def __init__(self, kind, lexeme, literal, line):
        self.kind = kind
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __repr__(self):
        return f'{self.kind.name} {self.literal}'

class Lexer:
    def __init__(self, source):
        self.source = source
        self.tokens = []

        self.line = 0

    def is_literal(self, word):
        prefix = word[0]
        body = word[1:]
        if prefix == '@':
            return Token(TokenKind.IDENTIFIER, word, body, self.word_index)
        elif prefix == '$':
            return Token(TokenKind.LABEL, word, body, self.word_index)
        elif prefix == "'":
            return Token(TokenKind.STRING_CONTINUATION, word, body, self.word_index)
        elif prefix == '"':
            return Token(TokenKind.STRING, word, body, self.word_index)
        else:
            try:
                number = float(word)
                return Token(TokenKind.NUMBER, word, number, self.word_index)
            except ValueError:
                pass

        return False

    def scan(self):
        words = self.source.split()
        for self.word_index, word in enumerate(words):
            if token := self.is_literal(word):
                self.tokens.append(token)


source = open('source.txt', 'r').read()

lexer = Lexer(source)
lexer.scan()

print(lexer.tokens)
        
