class Token:
    def __init__(self, kind, value, line):
        self.kind = kind
        self.value = value
        self.line = line
        
class Lexer:
    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.start = -1
        self.current = -1
        self.line = 1

    def scan_tokens(self):
        while (not self.at_end()):
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token('EOF', None, self.line))

    def scan_token(self):
        c = self.advance()
        match c:
            case ',':
                self.add_token('COMMA', None)
            case '{':
                self.add_token('LEFT BRACE', None)
            case '}':
                self.add_token('RIGHT BRACE', None)
            case ':':
                self.add_token('COLON', None)

            case '>':
                while self.peek() != '\n' and not self.at_end():
                    self.advance()

            case ' ' | '\r' | '\t':
                pass
            case '\n':
                self.line += 1

            case _:
                if c.isdigit():
                    self.number()
                else:
                    raise ValueError(f'unexpected character {c} in line {self.line}')

    def number(self):
        while self.peek().isdigit():
            self.advance()

        if self.peek() == '.' and self.peek_next().isdigit():
            self.advance()
            while self.peek().isdigit():
                self.advance()

        self.add_token('NUMBER', int(self.source[start, current]))

    def add_token(self, kind, value):
        self.tokens.append(Token(kind, value, self.line))

    def advance(self):
        self.current += 1
        return self.source[self.current]

    def at_end(self):
        return self.current >= len(self.source)-1

    def match(self, expected):
        if self.at_end(): return False
        if self.source[self.current] != expected: return False

        self.current += 1
        return True

    def peek(self):
        if self.at_end(): return '\0'
        return self.source[self.current]

    def peek_next(self):
        if self.current+1 >= len(self.source): return '\0'
        return self.source[current+1]
        

class VM:
    def __init__(self):
        pass


code = open('code.txt', 'r').read()
lexer = Lexer(code)
lexer.scan_tokens()
