
import ast
import json


#ast.parse() returns root of ast (module)


 
#recursively traversing the ast

class Tree_build(ast.NodeVisitor):
    
    def visit_Module(self, node):  # start of the file
        tree = []
        for child in node.body:
            tree.append(self.visit(child))  
        return {"type": "module", "body": tree}
    

    def visit_Assign(self, node):                   #a=b
        target = self._get_name(node.targets[0])
        value = self.visit(node.value)
        return {"type": "assign", "target": target, "value": value}
    

    def visit_BinOp(self, node):      #z=x+y
        return {
            "type": "binop",
            "left": self.visit(node.left),
            "op": type(node.op).__name__,
            "right": self.visit(node.right)
        }
    

    def _get_name(self, node):
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return self._get_name(node.value) + "." + node.attr
        return str(node)




    def visit_Call(self, node):             #func()
        func = self._get_name(node.func)
        args = [self.visit(a) for a in node.args]
        return {"type": "call", "func": func, "args": args}

    def visit_Constant(self, node):
        return node.value

    def visit_Name(self, node):
        return node.id

    
 
    def visit_Expr(self, node):
        return {
            "type":"Expr",
            "values":self.visit(node.value)

        }
    

    def visit_If(self, node):
        return {
        "type": "if",
        "condition": self.visit(node.test),
        "body": [self.visit(stmt) for stmt in node.body], #visiting eveyr single executable stmnt
        "else": [self.visit(stmt) for stmt in node.orelse]
    }
        
    
    def visit_BoolOp(self, node):
          return {
        "type": "boolop",
        "op": type(node.op).__name__,
        "values": [self.visit(v) for v in node.values]
    }






def parse_code(code):
    tree = Tree_build()

    try:
        parsed = ast.parse(code)
        res = tree.visit(parsed)
        return res

    except SyntaxError as e:
        return f"Syntax Error: {e}"




#testing
code="haha hi"




if __name__=="__main__":
    print(parse_code(code))
    





