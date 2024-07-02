class Compose:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        
    def __str__(self):            
        if isinstance(self.value, str):
            return f"['{self.key}','{self.value}']"
        return f"['{self.key}',{self.value}]"