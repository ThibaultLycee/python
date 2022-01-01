##########################################
#   IMPORTS
##########################################

import string_with_arrows as swa
import string

##########################################
#   CONSTANTS
##########################################

DIGITS = "0123456789"
LETTERS = string.ascii_letters
LETTERS_DIGITS = LETTERS + DIGITS

##########################################
#   ERROR
##########################################

class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.error_name = error_name
        self.details = details
        self.pos_start = pos_start
        self.pos_end = pos_end
    
    def as_string(self):
        res = f'{self.error_name} : {self.details}\n\tFile: {self.pos_start.fn}, line {self.pos_start.ln + 1}'
        res += '\n' + swa.string_with_arrows(self.pos_start.ftxt, self.pos_start.col, self.pos_end.col)
        return res

class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, "Illegal Character", details)

class InvalidSyntaxError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, "Invalid Syntax", details)

class RTError(Error):
    def __init__(self, pos_start, pos_end, details, context):
        super().__init__(pos_start, pos_end, "Runtime Error", details)
        self.context = context

    def as_string(self):
        res = self.generate_traceback()
        res += f'{self.error_name} : {self.details}\n'
        res += swa.string_with_arrows(self.pos_start.ftxt, self.pos_start.col, self.pos_end.col)
        return res
    
    def generate_traceback(self):
        result = ""
        pos = self.pos_start
        ctx = self.context

        while ctx:
            result += f'\tFile {pos.fn}, line {str(pos.ln + 1)}, in {ctx.display_name}\n'
            pos = ctx.parent_entry_pos
            ctx = ctx.parent
        return "Traceback (most recent call):\n" + result

##########################################
#   POSITION
##########################################

class Position:
    def __init__(self, index, ln, col, file_name, file_text):
        self.index = index
        self.ln = ln
        self.col = col
        self.fn = file_name
        self.ftxt = file_text
    
    def advance(self, curr_char=None):
        self.index += 1
        self.col += 1
        if curr_char == '\n':
            self.ln += 1
            self.col = 0
    
    def copy(self):
        return Position(self.index, self.ln, self.col, self.fn, self.ftxt)

##########################################
#   TOKENS
##########################################

TT_INT = "INT"
TT_FLOAT = "FLOAT"
TT_PLUS = "PLUS"
TT_MIN = "MIN"
TT_MUL = "MUL"
TT_POW = "POW"
TT_ROOT = "ROOT"
TT_DIV = "DIV"
TT_IDIV = "IDIV"
TT_MOD = "MOD"
TT_LPAREN = "LPAREN"
TT_RPAREN = "RPAREN"
TT_EQ = "EQ"
TT_INDENTIFIER = "IDENTIFIER"
TT_KEYWORD = "KEYWORD"

TT_EOF = "EOF"

KEYWORDS = [
    'INT',
    'FLOAT'
]

class Token:
    def __init__(self, type_, value=None, pos_start=None, pos_end=None):
        self.type = type_
        self.value = value
        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()
        if pos_end: self.pos_end = pos_end
    
    def __repr__(self):
        return f'{self.type}:{self.value}' if self.value else self.type
    
    def matches(self, type_, value=None):
        return self.type == type_ and self.value == value

##########################################
#   LEXER
##########################################

class Lexer:
    def __init__(self, file_name, text):
        self.text = text
        self.pos = Position(-1, 0, -1, file_name, text)
        self.curr_char = None
        self.advance()
        self.fn = file_name
    
    def advance(self):
        self.pos.advance(self.curr_char)
        self.curr_char = self.text[self.pos.index] if self.pos.index < len(self.text) else None

    def makeTokens(self):
        tokens = []
        while self.curr_char != None:
            if self.curr_char in ' \t':
                self.advance()
            elif self.curr_char in DIGITS + ".":
                tokens.append(self.makeNumber())
            elif self.curr_char in LETTERS + "_":
                tokens.append(self.makeIdentifier())
            elif self.curr_char == "+":
                tokens.append(Token(TT_PLUS, pos_start=self.pos))
                self.advance()
            elif self.curr_char == "-":
                tokens.append(Token(TT_MIN, pos_start=self.pos))
                self.advance()
            elif self.curr_char == "*":
                tokens.append(self.makeMultToken())
            elif self.curr_char == "/":
                tokens.append(self.makeDivToken())
            elif self.curr_char == "(":
                tokens.append(Token(TT_LPAREN, pos_start=self.pos))
                self.advance()
            elif self.curr_char == ")":
                tokens.append(Token(TT_RPAREN, pos_start=self.pos))
                self.advance()
            elif self.curr_char == "%":
                tokens.append(Token(TT_MOD, pos_start=self.pos))
                self.advance()
            elif self.curr_char == "=":
                tokens.append(Token(TT_EQ, pos_start=self.pos))
                self.advance()
            else:
                pos_start = self.pos.copy()
                char = self.curr_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, f"'{char}'")

        tokens.append(Token(TT_EOF, pos_start=self.pos))

        return tokens, None
    
    def makeDivToken(self):
        symbol = ""
        pos_start = self.pos.copy()
        while self.curr_char != None and self.curr_char in "*/":
            symbol += self.curr_char
            self.advance()
        if symbol == "//": return Token(TT_IDIV, pos_start=pos_start, pos_end=self.pos)
        return Token(TT_DIV, pos_start=pos_start, pos_end=self.pos)

    def makeMultToken(self):
        symbol = ""
        pos_start = self.pos.copy()
        while self.curr_char != None and self.curr_char in "*/":
            symbol += self.curr_char
            self.advance()
        if symbol == "**": return Token(TT_POW, pos_start=pos_start, pos_end=self.pos)
        elif symbol == "*/": return Token(TT_ROOT, pos_start=pos_start, pos_end=self.pos)
        else: return Token(TT_MUL, pos_start=pos_start)

    def makeNumber(self):
        num_str = ""
        dot_count = 0
        pos_start = self.pos.copy()
        while self.curr_char != None and self.curr_char in  DIGITS + ".":
            if self.curr_char == ".":
                if dot_count == 1: break
                dot_count += 1
                num_str += '.' if len(num_str) < 0 else '0.'
            else: num_str += self.curr_char
            self.advance()
        
        if dot_count == 0: return Token(TT_INT, int(num_str), pos_start, self.pos)
        else: return Token(TT_FLOAT, float(num_str), pos_start, self.pos)

    def makeIdentifier(self):
        identifier = ""
        pos_start = self.pos.copy()
        while self.curr_char != None and self.curr_char in LETTERS_DIGITS + "_":
            identifier += self.curr_char
            self.advance()
        
        tok_type = TT_KEYWORD if identifier in KEYWORDS else TT_INDENTIFIER
        return Token(tok_type, identifier, pos_start, self.pos)

##########################################
#   NODES
##########################################

class NumberNode:
    def __init__(self, tok):
        self.tok = tok

        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return f'{self.tok}'

class BinOpNode:
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node

        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end
    
    def __repr__(self):
        return f'({self.left_node}, {self.op_tok}, {self.right_node})'

class UnaryOpNode:
    def __init__(self, op_tok, node):
        self.op_tok = op_tok
        self.node = node

        self.pos_start = self.op_tok.pos_start
        self.pos_end = self.node.pos_end
    
    def __repr__(self):
        return f'({self.op_tok}, {self.node})'

class VarAccessNode:
    def __init__(self, var_name_tok):
        self.var_name_tok = var_name_tok

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.var_name_tok.pos_end

class VarAssignNode:
    def __init__(self, var_name_tok, value_node, var_type):
        self.var_name_tok = var_name_tok
        self.value_node = value_node
        self.var_type = var_type

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.var_name_tok.pos_end

##########################################
#   PARSE RESULT
##########################################

class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None
        self.advance_count = 0
    
    def register_advancement(self, res):
        self.advance_count += 1

    def register(self, res):
        self.advance_count += res.advance_count
        if res.error: self.error = res.error
        return res.node

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        if not self.error or self.advance_count == 0:
            self.error = error
        return self

##########################################
#   PARSER
##########################################

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.advance()

    def advance(self):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens): self.curr_token = self.tokens[self.tok_idx]
        return self.curr_token

    def parse(self):
        res = self.expression()
        if not res.error and self.curr_token.type != TT_EOF:
            return res.failure(
                InvalidSyntaxError(self.curr_token.pos_start, self.curr_token.pos_end,
                "Expected '+', '-', '*' or '/'"))
        return res

    def power(self):
        return self.bin_op(self.atom, [TT_POW], self.factor)

    def atom(self):
        res = ParseResult()
        tok = self.curr_token

        if tok.type in [TT_INT, TT_FLOAT]:
            res.register_advancement(self.advance())
            return res.success(NumberNode(tok))
        
        elif tok.type == TT_INDENTIFIER:
            res.register_advancement(self.advance())
            return res.success(VarAccessNode(tok))

        elif tok.type == TT_LPAREN:
            res.register_advancement(self.advance())
            expr = res.register(self.expression())
            if res.error: return res
            if self.curr_token.type == TT_RPAREN:
                res.register_advancement(self.advance())
                return res.success(expr)
            else:
                return res.failure(
                    InvalidSyntaxError(self.curr_token.pos_start, self.curr_token.pos_end,
                    "Expected ')'"))
        
        else:
            return res.failure(
                InvalidSyntaxError(tok.pos_start, tok.pos_end,
                "Expected int, float, identifier, '+', '-' or '('")
            )

    def factor(self):
        res = ParseResult()
        tok = self.curr_token

        if tok.type in [TT_PLUS, TT_MIN]:
            res.register_advancement(self.advance())
            factor = res.register(self.factor())
            if res.error: return res
            return res.success(UnaryOpNode(tok, factor))
        
        return self.power()

    def term(self):
        return self.bin_op(self.factor, [TT_MUL, TT_DIV, TT_POW, TT_ROOT, TT_IDIV, TT_MOD])

    def expression(self):
        res = ParseResult()

        if self.curr_token.matches(TT_KEYWORD, 'INT'):
            res.register_advancement(self.advance())

            if self.curr_token.type != TT_INDENTIFIER:
                return res.failure(InvalidSyntaxError(
                    self.curr_token.pos_start, self.curr_token.pos_end,
                    "Expected identifier"
                ))
            var_name = self.curr_token
            res.register_advancement(self.advance())

            if self.curr_token.type != TT_EQ:
                return res.failure(InvalidSyntaxError(
                    self.curr_token.pos_start, self.curr_token.pos_end,
                    "Expected '='"
                ))
            
            res.register_advancement(self.advance())
            expr = res.register(self.expression())
            if res.error: return res
            if isinstance(expr, VarAccessNode) and global_symbol_table.get_type(expr.var_name_tok.value) != TT_INT:
                return res.failure(InvalidSyntaxError(
                    expr.pos_start, expr.pos_end,
                    "Expected integer"
                ))
            if (isinstance(expr, VarAccessNode) and global_symbol_table.get_type(expr.var_name_tok.value) == TT_INT) or expr.tok.type == TT_INT:
                return res.success(VarAssignNode(var_name, expr, TT_INT))
            return res.failure(InvalidSyntaxError(
                expr.pos_start, expr.pos_end,
                "Expected integer"
            ))
        
        if self.curr_token.matches(TT_KEYWORD, 'FLOAT'):
            res.register_advancement(self.advance())

            if self.curr_token.type != TT_INDENTIFIER:
                return res.failure(InvalidSyntaxError(
                    self.curr_token.pos_start, self.curr_token.pos_end,
                    "Expected identifier"
                ))
            var_name = self.curr_token
            res.register_advancement(self.advance())

            if self.curr_token.type != TT_EQ:
                return res.failure(InvalidSyntaxError(
                    self.curr_token.pos_start, self.curr_token.pos_end,
                    "Expected '='"
                ))
            
            res.register_advancement(self.advance())
            expr = res.register(self.expression())
            if res.error: return res
            return res.success(VarAssignNode(var_name, expr, TT_FLOAT))

        node = res.register(self.bin_op(self.term, [TT_PLUS, TT_MIN]))
        if res.error:
            return res.failure(InvalidSyntaxError(
                self.curr_token.pos_start, self.curr_token.pos_end,
                "Expected 'number', int, float, identifier, '+', '-' or '('"
            ))

        return res.success(node)

    def bin_op(self, func_a, ops, func_b=None):
        if not func_b: func_b = func_a
        res = ParseResult()
        left = res.register(func_a())
        if res.error: return res

        while self.curr_token.type in ops:
            op_tok = self.curr_token
            res.register_advancement(self.advance())
            right = res.register(func_b())
            if res.error: return res
            left = BinOpNode(left, op_tok, right)
        return res.success(left)

##########################################
#   RUNTIME RESULT
##########################################

class RTResult:
    def __init__(self):
        self.value = None
        self.error = None
    
    def register(self, res):
        if res.error: self.error = res.error
        return res.value
    
    def succes(self, value):
        self.value = value
        return self
    
    def faillure(self, error):
        self.error = error
        return self

##########################################
#   VALUES
##########################################

class Number:
    def __init__(self, value):
        self.value = value
        self.set_pos()
        self.set_context()

    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self
    
    def get_int(self):
        return Number(int(self.value)).set_pos(self.pos_start, self.pos_end).set_context(self.context)
    
    def get_float(self):
        return Number(float(self.value)).set_pos(self.pos_start, self.pos_end).set_context(self.context)

    def copy(self):
        return Number(self.value).set_pos(self.pos_start, self.pos_end).set_context(self.context)

    def set_context(self, context=None):
        self.context = context
        return self

    def added_to(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None
    
    def subbed_to(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None
    
    def multed_to(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None

    def dived_to(self, other):
        if isinstance(other, Number):
            if other.value == 0: 
                return None, RTError(
                    other.pos_start, other.pos_end,
                    "Division by zero", self.context
                )
            return Number(self.value / other.value).set_context(self.context), None
    
    def powed_to(self, other):
        if isinstance(other, Number):
            if other.value == 0 and self.value == 0:
                return None, RTError(
                    self.pos_start, other.pos_end,
                    "Zero to the power of zero", self.context
                )
            return Number(self.value ** other.value).set_context(self.context), None
    
    def rooted_to(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RTError(
                    other.pos_start, other.pos_end,
                    "0th-root", self.context
                )
            if self.value < 0:
                return None, RTError(
                    self.pos_start, self.pos_end,
                    "Complex number !", self.context
                )
            return Number(self.value ** (1 / other.value)).set_context(self.context), None
    
    def idived_to(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RTError(
                    other.pos_start, other.pos_end,
                    "Division by zero", self.context
                )
            return Number(self.value // other.value).set_context(self.context), None
    
    def moded_to(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RTError(
                    other.pos_start, other.pos_end,
                    "Modulo by zero", self.context
                )
            return Number(self.value % other.value).set_context(self.context), None
    
    def __repr__(self):
        return str(self.value)

##########################################
#   CONTEXT
##########################################

class Context:
    def __init__(self, display_name, parent=None, parent_entry_pos=None):
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos
        self.symbol_table = None

##########################################
#   SYMBOL TABLE
##########################################

VAR_TYPES = (TT_INT, TT_FLOAT)

class SymbolTable:
    def __init__(self):
        self.symbols = {}
        self.type_table = {}
        self.parent = None
    
    def get(self, var_name):
        for type_ in VAR_TYPES:
            value = self.symbols.get((type_, var_name), None)
            if value != None:
                if type_ == TT_FLOAT:
                    value = value.get_float()
                return value
        
        if value == None and self.parent:
            return self.parent.get(var_name)

    def get_type(self, var_name):
        return self.type_table.get(var_name, None)

    def set(self, tok_type, var_name, value):
        for type_, name in self.symbols.keys():
            if name == var_name:
                del self.symbols[(type_, name)]
                break
        self.symbols[(tok_type, var_name)] = value
        self.type_table[var_name] = tok_type
    
    def remove(self, name):
        del self.symbols[name]

##########################################
#   INTERPRETER
##########################################

class Interpreter:
    def visit(self, node, context):
        method_name = f"visit_{type(node).__name__}"
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)
    
    def no_visit_method(self, node, context):
        raise Exception(f'No visit_{type(node).__name__} method defined')

    def visit_VarAssignNode(self, node, context):
        res = RTResult()

        var_name = node.var_name_tok.value
        value = res.register(self.visit(node.value_node, context))
        if res.error: return res

        context.symbol_table.set(node.var_type, var_name, value)
        return res.succes(value)

    def visit_VarAccessNode(self, node, context):
        res = RTResult()

        var_name = node.var_name_tok.value
        value = context.symbol_table.get(var_name)

        if not value:
            return res.faillure(RTError(
                node.pos_start, node.pos_end,
                f'{var_name} is not defined', context
            ))

        value = value.copy().set_pos(node.pos_start, node.pos_end)
        return res.succes(value)
    
    def visit_NumberNode(self, node, context):
        return RTResult().succes(
            Number(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end)
        )
    
    def visit_BinOpNode(self, node, context):
        res = RTResult()
        left = res.register(self.visit(node.left_node, context))
        if res.error: return res
        right = res.register(self.visit(node.right_node, context))
        if res.error: return res

        if node.op_tok.type == TT_PLUS:
            result, error = left.added_to(right)
        elif node.op_tok.type == TT_MIN:
            result, error = left.subbed_to(right)
        elif node.op_tok.type == TT_MUL:
            result, error = left.multed_to(right)
        elif node.op_tok.type == TT_DIV:
            result, error = left.dived_to(right)
        elif node.op_tok.type == TT_IDIV:
            result, error = left.idived_to(right)
        elif node.op_tok.type == TT_MOD:
            result, error = left.moded_to(right)
        elif node.op_tok.type == TT_POW:
            result, error = left.powed_to(right)
        elif node.op_tok.type == TT_ROOT:
            result, error = left.rooted_to(right)
        
        if error: return res.faillure(error)
        else: return res.succes(result.set_pos(node.pos_start, node.pos_end))
    
    def visit_UnaryOpNode(self, node, context):
        res = RTResult()
        number = res.register(self.visit(node.node, context))
        if res.error: return res

        error = None

        if node.op_tok.type == TT_MIN: number, error = number.multed_to(Number(-1))
        elif node.op_tok.type == TT_ROOT: number, error = number.rootedto(Number(2))

        if error: return res.faillure(error)

        return res.succes(number.set_pos(node.pos_start, node.pos_end))

##########################################
#   RUN
##########################################

global_symbol_table = SymbolTable()
global_symbol_table.set(TT_INT, 'null', Number(0))

def run(fn, text):
    #LEXER
    lexer = Lexer(fn, text)
    tokens, error = lexer.makeTokens()

    if error: return None, error

    #PARSER
    parser = Parser(tokens)
    ast = parser.parse()

    if ast.error: return None, ast.error

    #INTERPRETER
    interpreter = Interpreter()
    context = Context("<program>")
    context.symbol_table = global_symbol_table
    result = interpreter.visit(ast.node, context)

    return result.value, result.error