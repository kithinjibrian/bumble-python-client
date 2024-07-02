from enum import Enum

class NodeType(Enum):
    NODE_PAIR = 'NODE_PAIR'
    NODE_LIST = 'NODE_LIST'
    NODE_ARRAY = 'NODE_ARRAY'
    NODE_OBJECT = 'NODE_OBJECT'
    NODE_STRING = 'NODE_STRING'
    NODE_NUMBER = 'NODE_NUMBER'
    NODE_KEY_VALUE = 'NODE_KEY_VALUE'

class AstNode:
    def __init__(self, node_type):
        self.node_type = node_type
        self.next = None
        
    def push(self, node):
        current = self
        while current.next is not None:
            current = current.next
        current.next = node
        
class AstObjectNode(AstNode):
	def __init__(self):
		super().__init__(NodeType.NODE_OBJECT)
		self.members = None
  
	def __str__(self):
		member_str = ",".join(str(member) for member in self.iter_members())
		return "{" + member_str + "}"

	def iter_members(self):
		current = self.members
		while current is not None:
			yield current
			current = current.next
   
class AstArrayNode(AstNode):
	def __init__(self):
		super().__init__(NodeType.NODE_ARRAY)
		self.elements = None
  
	def __str__(self):
		element_str = ", ".join(str(element) for element in self.iter_elements())
		return "[" + element_str + "]"

	def iter_elements(self):
		current = self.elements
		while current is not None:
			yield current
			current = current.next
  

class AstKeyValueNode(AstNode):
	def __init__(self):
		super().__init__(NodeType.NODE_KEY_VALUE)
		self.key = None
		self.value = None
  
	def __str__(self):
		return str(self.key) + " : " + str(self.value)
  
class AstStringNode(AstNode):
	def __init__(self, string_value):
		super().__init__(NodeType.NODE_STRING)
		self.value = string_value
	
	def __str__(self):
		return "\"" + self.value + "\""

class AstNumberNode(AstNode):
	def __init__(self, number_value):
		super().__init__(NodeType.NODE_NUMBER)
		self.value = number_value
  
	def __str__(self):
		return str(self.value)