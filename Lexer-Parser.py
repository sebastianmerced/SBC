
import client as client
INTEGER, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, EOF, MOD = (
    'INTEGER', 'PLUS', 'MINUS', 'MUL', 'DIV', '(', ')', 'EOF', 'MOD'
)


class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):

        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()


class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Invalid character. Verify grammar.')

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)
#Tokenizer
    def get_next_token(self):
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())
            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(MUL, '*')

            if self.current_char == '/':
                self.advance()
                return Token(DIV, '/')

            if self.current_char == '%':
                self.advance()
                return Token(MOD, '%')

            self.error()

        return Token(EOF, None)


#parser
class AST(object):
    pass
class UnaryOp(AST):
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr

class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def warning(self):
        raise Exception('Invalid syntax.Please remember to enter equation as you would in your everyday calculator.')

    def remove(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.warning()

    def factor(self):
        token = self.current_token
        if token.type == PLUS:
            self.remove(PLUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == MINUS:
            self.remove(MINUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == INTEGER:
            self.remove(INTEGER)
            return Num(token)
        elif token.type == LPAREN:
            self.remove(LPAREN)
            node = self.expr()
            self.remove(RPAREN)
            return node
    def term(self):
        node = self.factor()

        while self.current_token.type in (MUL, DIV, MOD):
            token = self.current_token
            if token.type == MUL:
                self.remove(MUL)
            elif token.type == DIV:
                self.remove(DIV)
            elif token.type == MOD:
                self.remove(MOD)

            node = BinOp(left=node, op=token, right=self.factor())

        return node

    def expr(self):
        node = self.term()
        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.remove(PLUS)
            elif token.type == MINUS:
                self.remove(MINUS)
            node = BinOp(left=node, op=token, right=self.term())
        return node

    def parse(self):
        return self.expr()




#  INTERPRETER
#  Since it will just evaluate arithmetic expressions and the parser
# makes sure they are enter correctly we use python method eval() which
# takes a string assuming it is in proper format and calculates it
def interpret(text):
    return client.client(text)




def main():
    print("SBC is a programming language that solves arithmetic equations for you. It uses remote computation(servers) without the need for you to create them.")
    print("Remember to use the same grammar as you would in a calculator.To exit type QUIT")
    while True:
        try:
            text = input('SBC> ')
        except EOFError:
            break
        if not text:
            continue
        if(text.lower()=="quit"):
            quit()
        lexer = Lexer(text)
        parser = Parser(lexer)
        result = interpret(text)
        print(result)


if __name__ == '__main__':
    main()
