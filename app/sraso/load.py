from sraso import lexer, parser, evaluate

def load(sraso):
    lexemes = lexer.Lexer(sraso).lex()
    ast = parser.Parser(lexemes).parse()
    objects = evaluate.evaluate(ast)
    return objects