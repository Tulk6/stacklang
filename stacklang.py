import enum

class TokenKind(enum.Enum):
    #Literals
    INTEGER = 1
    FLOAT = 38
    STRING = 2
    STRING_CONTINUATION = 3
    IDENTIFIER = 4
    LABEL = 5

    #keywords
    STRUCT = 6
    FUNC = 7
    END = 8

    #datatypes
    LIST = 9
    DICT = 10

    #builtins
    NEW = 11
    DEFINE = 12
    LOOKUP = 33

    INDEX = 13
    GET = 39
    SET = 40
    APPEND = 41
    LENGTH = 14
    NEXT = 15
    IN = 16

    SUM = 17
    SUBTRACT = 18
    DIVIDE = 19
    MULTIPLY = 20

    SUMEQ = 21
    SUBEQ = 22
    DIVEQ = 23
    MLTEQ = 24

    AND = 25
    NOT = 26
    OR = 27
    XOR = 28
    EQUAL = 29

    POP = 30
    SWAP = 31
    ROTATE = 32
    DUPLICATE = 33

    REFERENCE = 35

    CALL = 36

    RETURN = 37

class Token:
    def __init__(self, kind, lexeme, literal, line):
        self.kind = kind
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __repr__(self):
        if self.literal is not None:
            return f'<{self.kind.name} {self.literal}>'
        else:
            return f'<{self.kind.name}>'

class Lexer:
    def __init__(self, source):
        self.source = source
        self.tokens = []

        self.line = 0

    def is_literal(self, word):
        prefix = word[0]
        body = word[1:]
        
        try:
            number = int(word)
        except ValueError:
            try:
                number = float(word)
            except ValueError:
                pass
            else:
                return Token(TokenKind.FLOAT, word, number, self.word_index)
        else:
            return Token(TokenKind.INTEGER, word, number, self.word_index)
        
        if len(word) > 1: 
            if prefix == '@':
                return Token(TokenKind.IDENTIFIER, word, body, self.word_index)
            elif prefix == '$':
                return Token(TokenKind.LABEL, word, body, self.word_index)
            elif prefix == "'":
                return Token(TokenKind.STRING_CONTINUATION, word, body, self.word_index)
            elif prefix == '"':
                return Token(TokenKind.STRING, word, body, self.word_index)

        return False

    def is_keyword(self, word):
        keywords = {
            #defines
            'STRUCT': Token(TokenKind.STRUCT, word, None, self.word_index),
            'FUNC': Token(TokenKind.FUNC, word, None, self.word_index),
            'END': Token(TokenKind.END, word, None, self.word_index),
            #datatypes
            'List': Token(TokenKind.LIST, word, None, self.word_index),
            'Dict': Token(TokenKind.DICT, word, None, self.word_index),
            #functions

            #structs/variables
            'new': Token(TokenKind.NEW, word, None, self.word_index),
            'define': Token(TokenKind.DEFINE, word, None, self.word_index),
            'lookup': Token(TokenKind.LOOKUP, word, None, self.word_index),

            #object spec
            'index': Token(TokenKind.INDEX, word, None, self.word_index),
            'get': Token(TokenKind.GET, word, None, self.word_index),
            'set': Token(TokenKind.SET, word, None, self.word_index),
            'length': Token(TokenKind.LENGTH, word, None, self.word_index),
            'next': Token(TokenKind.NEXT, word, None, self.word_index),
            'in': Token(TokenKind.IN, word, None, self.word_index),
            'append': Token(TokenKind.APPEND, word, None, self.word_index),

            #maths
            '+': Token(TokenKind.SUM, word, None, self.word_index),
            'add': Token(TokenKind.SUM, word, None, self.word_index),
            '-': Token(TokenKind.SUBTRACT, word, None, self.word_index),
            'subtract': Token(TokenKind.SUBTRACT, word, None, self.word_index),
            '/': Token(TokenKind.DIVIDE, word, None, self.word_index),
            'divide': Token(TokenKind.DIVIDE, word, None, self.word_index),
            '*': Token(TokenKind.MULTIPLY, word, None, self.word_index),
            'multiply': Token(TokenKind.MULTIPLY, word, None, self.word_index),

            '+=': Token(TokenKind.SUMEQ, word, None, self.word_index),
            '-=': Token(TokenKind.SUBEQ, word, None, self.word_index),
            '*=': Token(TokenKind.MLTEQ, word, None, self.word_index),
            '/=': Token(TokenKind.DIVEQ, word, None, self.word_index),

            #logic
            'and': Token(TokenKind.AND, word, None, self.word_index),
            '&': Token(TokenKind.AND, word, None, self.word_index),
            'or': Token(TokenKind.OR, word, None, self.word_index),
            '|': Token(TokenKind.OR, word, None, self.word_index),
            'not': Token(TokenKind.NOT, word, None, self.word_index),
            '!': Token(TokenKind.NOT, word, None, self.word_index),
            'xor': Token(TokenKind.XOR, word, None, self.word_index),
            '^': Token(TokenKind.XOR, word, None, self.word_index),
            'equal': Token(TokenKind.EQUAL, word, None, self.word_index),
            '==': Token(TokenKind.EQUAL, word, None, self.word_index),

            #stack
            'pop': Token(TokenKind.POP, word, None, self.word_index),
            'swap': Token(TokenKind.SWAP, word, None, self.word_index),
            'rotate': Token(TokenKind.ROTATE, word, None, self.word_index),
            'duplicate': Token(TokenKind.DUPLICATE, word, None, self.word_index),
            'dup': Token(TokenKind.DUPLICATE, word, None, self.word_index),

            'reference': Token(TokenKind.REFERENCE, word, None, self.word_index),
            '->': Token(TokenKind.REFERENCE, word, None, self.word_index),

            'call': Token(TokenKind.CALL, word, None, self.word_index),

            'return': Token(TokenKind.RETURN, word, None, self.word_index)
            }
        
        if word in keywords.keys():
            return keywords[word]
        else:
            return False

    def is_comment(self, word):
        return (len(word) != 0 and word[0] == '>')

    def scan(self):
        words = self.source.split()
        for self.word_index, word in enumerate(words):
            if token := self.is_literal(word):
                self.tokens.append(token)
            elif token := self.is_keyword(word):
                self.tokens.append(token)
            elif token := self.is_comment(word):
                pass
            else:
                raise SyntaxError(word)


class Struct:
    def __init__(self, fields):
        self.fields = fields

    def get(self, field):
        return self.fields[field]

    def set(self, field, value):
        if field in self.fields.keys():
            self.fields[field] = value

    def new(self):
        return Struct(self.fields.copy())

    def __repr__(self):
        return f"<STRUCT {self.fields}>"

class List:
    def __init__(self, values=None):
        if values is None:
            self.values = []
        else:
            self.values = values

    def index(self, index):
        return self.values[index]

    def append(self, value):
        self.values.append(value)

    def new(self):
        return List(values=self.values.copy())

    def __repr__(self):
        return f"<LIST {','.join([repr(v) for v in self.values])}>"


class Interpreter:
    def __init__(self, tokens):
        self.tokens = tokens

    def push_jump(self, index):
        self.jump_stack.append(index)

    def pop_jump(self):
        return self.jump_stack[-1]

    def push(self, value):
        self.program_stack.append(value)

    def pop(self):
        return self.program_stack.pop(-1)

    def peek(self, i=1):
        return self.program_stack[-i]

    def rotate(self):
        tail = self.program_stack.pop(-2)
        self.program_stack.append(tail)

    def interpret(self):
        self.token_index = 0
        self.halt = False
        
        self.program_stack = []
        self.return_stack = []
        
        self.jump_stack = []
        
        self.definitions = {'List': List()}

        self.find_definitions()
        print(self.definitions)

        self.token_index = self.definitions['main']+1
        while not self.halt and self.token_index < len(self.tokens):
            token = self.tokens[self.token_index]
            self.interpret_token(token)
            self.token_index += 1

    def find_definitions(self):
        while not self.halt and self.token_index < len(self.tokens):
            token = self.tokens[self.token_index]

            if token.kind is TokenKind.FUNC:
                function_name = self.advance().literal
                self.definitions[function_name] = self.token_index

            elif token.kind is TokenKind.STRUCT:
                struct_fields = {}
                struct_name = self.advance().literal
                next_token = self.advance()
                while next_token.kind is not TokenKind.END: 
                    if next_token.kind is TokenKind.LABEL:
                        field_name = next_token.literal
                        field_value = self.advance().literal
                        struct_fields[field_name] = field_value
                    next_token = self.advance()

                self.definitions[struct_name] = Struct(struct_fields)

            self.token_index += 1

    def interpret_token(self, token):
        print(self.program_stack)
        print(token)
        if token.kind in (TokenKind.FLOAT, TokenKind.INTEGER, TokenKind.STRING, TokenKind.LABEL):
            self.push(token.literal)
        elif token.kind is TokenKind.STRING_CONTINUATION:
            self.program_stack[-1] = str(self.program_stack[-1]) + ' '+token.literal
        elif token.kind is TokenKind.IDENTIFIER:
            label = token.literal
            self.push(self.definitions[label])
            

        elif token.kind is TokenKind.NEW:
            struct_template = self.pop()
            self.push(struct_template.new())

        elif token.kind is TokenKind.GET:
            field_name = self.pop()
            struct = self.peek()
            self.push(struct.get(field_name))
        elif token.kind is TokenKind.SET:
            field_value = self.pop()
            field_name = self.pop()
            struct = self.peek()
            struct.set(field_name, field_value)

        elif token.kind is TokenKind.INDEX:
            index = self.pop()
            _list = self.peek()
            self.push(_list.index(index))
        elif token.kind is TokenKind.APPEND:
            value = self.pop()
            _list = self.peek()
            _list.append(value)

        elif token.kind is TokenKind.SUM:
            self.push(self.pop()+self.pop())
        elif token.kind is TokenKind.MULTIPLY:
            self.push(self.pop()*self.pop())
        elif token.kind is TokenKind.DIVIDE:
            self.push((1/self.pop())*self.pop())
        elif token.kind is TokenKind.SUBTRACT:
            self.push(-self.pop()+self.pop())

        elif token.kind is TokenKind.DEFINE:
            label = self.pop()
            data = self.pop()
            self.definitions[label] = data

        elif token.kind is TokenKind.LOOKUP:
            label = self.pop()
            self.push(self.definitions[label])

        elif token.kind is TokenKind.CALL:
            function_index = self.pop()
            self.push_jump(self.token_index)
            self.token_index = function_index
        elif token.kind is TokenKind.RETURN:
            return_index = self.pop_jump()
            self.token_index = return_index

        elif token.kind is TokenKind.POP:
            self.pop()
        elif token.kind is TokenKind.ROTATE:
            self.rotate()

    def advance(self):
        self.token_index += 1
        token = self.tokens[self.token_index]
        return token


source = open('source.txt', 'r').read()

lexer = Lexer(source)
lexer.scan()

interpreter = Interpreter(lexer.tokens)
interpreter.interpret()
print(interpreter.program_stack)
