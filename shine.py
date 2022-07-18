from lark import Lark, Transformer

# interpreter
def evaluate(program, value):
    if hasattr(value, "evaluate"):
        try:
            return value.evaluate(program)
        except:
            return value
    else:
        return value

class Program:
    def __init__(self, names):
        self.names = names

    def query(self, name):
        return evaluate(self, self.names[name])

    def __str__(self):
        return "\n".join(f"{pair[0]} := {pair[1]}" for pair in self.names.items())

class Expression:
    def __init__(self, lhs, operator, rhs):
        self.lhs, self.operator, self.rhs = lhs, operator, rhs

    def evaluate(self, program):
        return self.operator.evaluate(
            evaluate(program, self.lhs),
            evaluate(program, self.rhs)
        )

    def __str__(self):
        return f"({self.lhs} {self.operator} {self.rhs})"

class MulOperator:
    def evaluate(self, lhs, rhs):
        try:
            return lhs * rhs
        except:
            return Expression(lhs, self, rhs)

    def __str__(self):
        return "*"

class AddOperator:
    def evaluate(self, lhs, rhs):
        try:
            return lhs + rhs
        except:
            return Expression(lhs, self, rhs)

    def __str__(self):
        return "+"

class Name:
    def __init__(self, name):
        self.name = name

    def evaluate(self, program):
        return program.query(self.name)

    def __str__(self):
        return self.name

class ShineTransformer(Transformer):
    def name(self, tokens):
        return Name(str(tokens[0]))

    def number(self, tokens):
        return int(tokens[0])

    def mul(self, tokens):
        return MulOperator()

    def add(self, tokens):
        return AddOperator()

    def expression(self, tokens):
        return Expression(*tokens)

    def assignment(self, tokens):
        return (tokens[0].name, tokens[1])

    def program(self, tokens):
        assert len(set(map(lambda x: x[0], tokens))) == len(tokens) # consts
        return Program(dict(tokens))

with open("shine.lark") as f:
    grammar = f.read()

parser = Lark(
    grammar,
    parser="lalr", start="program", transformer=ShineTransformer()
)

with open("example.shine") as f:
    program = f.read()

ast = parser.parse(program)
print(ast)
for name in ast.names:
    print(name, "is", ast.query(name))