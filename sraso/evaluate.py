from sraso.ast import *
    
def evaluate(ast):
    if ast.node_type == NodeType.NODE_OBJECT:
        current = ast.members
        obj = {}
        while current is not None:
            obj[evaluate(current.key)] = evaluate(current.value)
            current = current.next
        return obj

    elif ast.node_type == NodeType.NODE_ARRAY:
        current = ast.elements
        array = []
        while current is not None:
            array.append(evaluate(current))
            current = current.next
        return array
    
    elif ast.node_type == NodeType.NODE_KEY_VALUE:
        return {evaluate(ast.key): evaluate(ast.value)}

    elif ast.node_type == NodeType.NODE_NUMBER:
        return ast.value

    elif ast.node_type == NodeType.NODE_STRING:
        return ast.value

    elif ast.node_type == NodeType.NODE_PAIR:
        return evaluate(ast.value)