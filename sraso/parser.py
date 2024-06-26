from sraso.lexer import TokenType
from sraso.ast import *

# <start>		::= <object> | <array> | <list>
# <object>	    ::= "{" <values> "}"
# <array>		::= "[" <values> "]"
# <list>		::= "(" <values> ")"
# <values>	    ::= <value> | <value> "," <values>
# <value>		::= <string> | <number> | <keyvalue> | <object>
# <keyvalue>	::= <key> ":" <value>
# <key>         ::= <string> | <number>

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0
        
    def next(self):
        self.index += 1
        
    def curr(self):
        return self.tokens[self.index]
    
    def ahead(self):
        return self.tokens[self.index + 1]
        
    def parse(self):
        return self.parse_value()
    
    def parse_values(self):
        ast_node = self.parse_value()
            
        if self.curr()['type'] == TokenType.TOKEN_COMMA:
            self.next()
            next_value = self.parse_values()
            ast_node.push(next_value)
            
        return ast_node
        
    def parse_object(self):
        if self.curr()['type'] != TokenType.TOKEN_LBRACE:
            raise Exception('Expected {')
        
        self.next()
        
        ast_node = AstObjectNode()
        ast_node.members = self.parse_values()
        
        if self.curr()['type'] != TokenType.TOKEN_RBRACE:
            raise Exception('Expected }')
        
        self.next()
        
        return ast_node
    
    def parse_array(self):
        if self.curr()['type'] != TokenType.TOKEN_LBRACKET:
            raise Exception('Expected [')
        
        self.next()
        
        ast_node = AstArrayNode()
        ast_node.elements = self.parse_values()
        
        if self.curr()['type'] != TokenType.TOKEN_RBRACKET:
            raise Exception('Expected ]')
        
        self.next()
        
        return ast_node
    
    def parse_list(self):
        if self.curr()['type'] != TokenType.TOKEN_LPAREN:
            raise Exception('Expected (')
        
        self.next()
        
        ast_node = AstArrayNode()
        ast_node.elements = self.parse_values()
        
        if self.curr()['type'] != TokenType.TOKEN_RPAREN:
            raise Exception('Expected )')
        
        self.next()
        
        return ast_node
            
    def parse_keyvalue(self):        
        ast_node = AstKeyValueNode()
        ast_node.key = self.parse_key()
        
        if self.curr()['type'] != TokenType.TOKEN_COLON:
            raise Exception('Expected ":"')
        
        self.next()
        ast_node.value = self.parse_value()
        
        return ast_node
    
    def parse_key(self):
        ast_node = None
        if self.curr()['type'] == TokenType.TOKEN_STRING or self.curr()['type'] == TokenType.TOKEN_WORD:
            ast_node = self.parse_string()
        elif self.curr()['type'] == TokenType.TOKEN_NUMBER:
             ast_node = self.parse_number()
             
        return ast_node
        
    def parse_value(self):
        ast_node = None
        
        if self.index + 1 < len(self.tokens) and self.ahead()['type'] == TokenType.TOKEN_COLON:
            ast_node = self.parse_keyvalue()
        else:
            if self.curr()['type'] == TokenType.TOKEN_STRING or self.curr()['type'] == TokenType.TOKEN_WORD:
                ast_node = self.parse_string()
            elif self.curr()['type'] == TokenType.TOKEN_NUMBER:
                ast_node = self.parse_number()
            elif self.curr()['type'] == TokenType.TOKEN_LBRACKET:
                ast_node = self.parse_array()
            elif self.curr()['type'] == TokenType.TOKEN_LPAREN:
                ast_node = self.parse_list()
            elif self.curr()['type'] == TokenType.TOKEN_LBRACE:
                ast_node = self.parse_object()
            
        return ast_node
                
    def parse_string(self):
        ast_node = AstStringNode(self.curr()['value'])
        self.next()
        return ast_node
        
    def parse_number(self):
        ast_node = AstNumberNode(self.curr()['value'])
        self.next()
        return ast_node