# "Starter Code" for EECS 481 HW3 shows how to use a visitor
# pattern to replace nodes in an abstract syntax tree. 
# 
# Note well:
# (1) It does not show you how to read input from a file. 
# (2) It does not show you how to write your resulting source
#       code to a file.
# (3) It does not show you how to "count up" how many of 
#       instances of various node types exist.
# (4) It does not show you how to use random numbers. 
# (5) It does not show you how to only apply a transformation
#       "once" or "some of the time" based on a condition.
# (6) It does not show you how to copy the AST so that each
#       mutant starts from scratch. 
# (7) It does show you how to execute modified code, which is
#       not relevant for this assignment.
#
# ... and so on. It's starter code, not finished code. :-) 
# 
# But it does highlight how to "check" if a node has a particular type, 
# and how to "change" a node to be different. 

import ast
import astor
import random
import sys
random.seed(123)
# randint(1, 100) returns random number 1 to 100 inclusive. Use for mutation
class MyVisitor(ast.NodeTransformer):
    """Notes all Numbers and all Strings. Replaces all numbers with 481 and
    strings with 'SE'."""

    # Note how we never say "if node.type == Number" or anything like that.
    # The Visitor Pattern hides that information from us. Instead, we use
    # these visit_Num() functions and the like, which are called
    # automatically for us by the library. 
    def visit_Num(self, node):
        # print("Visitor sees a number: ", ast.dump(node), " aka ", astor.to_source(node))
        if (random.randint(1,100) < 5):
            return ast.Num(n=(node.n - 1), kind=None)
        # Note how we never say "node.contents = 481" or anything like
        # that. We do not directly assign to nodes. Intead, the Visitor
        # Pattern hides that information from us. We use the return value
        # of this function and the new node we return is put in place by
        # the library. 
        # Note: some students may want: return ast.Num(n=481) 
        return node

    def visit_Str(self, node):
        # print("Visitor sees a string: ", ast.dump(node), " aka ", astor.to_source(node))
        if (random.randint(1,100) < 5):
            return ast.Str(s=(node.s + "1"))
        # Note: some students may want: return ast.Str(s=481)
        return node
    
    def visit_Expr(self, node):
        if (random.randint(1,100) < 1):
            return node
        return node
    
    def visit_BinOp(self, node):
        if random.randint(1, 100) < 1:
            node.op, node.left, node.right = self.swap_binary_operator(
                node.op, node.left, node.right
            )
        return node

    def swap_binary_operator(self, op, left, right):
        if isinstance(op, ast.Add):
            return ast.Sub(), left, right
        elif isinstance(op, ast.Sub):
            return ast.Add(), left, right
        elif isinstance(op, ast.Div):
            return ast.FloorDiv(), left, right
        return op, left, right
    
    def visit_Compare(self, node):
        if random.randint(1, 100) < 1:
            node.ops = self.negate_comparison(node.ops)
        return node

    def negate_comparison(self, op):
        if isinstance(op, ast.Eq):
            return ast.NotEq()
        elif isinstance(op, ast.NotEq):
            return ast.Eq()
        return op
    
    def visit_Assign(self, node):
        if random.randint(1, 100) < 1:
            return None
        return node
        


# code that runs first 
# Instead of reading from a file, the starter code always processes in 
# a small Python expression literally written in this string below: 
# Assuming fuzzywuzzy.py is in the same directory as this script
code = ""
num_files = 0
if len(sys.argv) != 3:
    print("Usage: python script.py <filename> <numerical_value>")
else:
    filename = sys.argv[1]
    numerical_value = int(sys.argv[2])  # Convert numerical value to float
    # Read the contents of the file
    with open(filename, 'r') as file:
        file_content = file.read()
        code = file_content
        num_files = numerical_value

print(code)
print(num_files)




# As a sanity check, we'll make sure we're reading the code
# correctly before we do any processing. 
print("Before any AST transformation")
print("Code is: ", code)
print("Code's output is:") 
#exec(code)      # not needed for HW3
print()
print(num_files)
for i in range(0, num_files):
    # Now we will apply our transformation. 
    print("Applying AST transformation")
    mut_code = code
    tree = ast.parse(mut_code)
    tree = MyVisitor().visit(tree)
    # Add lineno & col_offset to the nodes we created
    ast.fix_missing_locations(tree)
    print("Transformed code is: ", astor.to_source(tree))
    file_to_write = str(i) + ".py"
    with open(file_to_write, "w") as file:
        file.write(astor.to_source(tree))
    print(file_to_write)

    co = compile(tree, "", "exec")
    print("Transformed code's output is:") 
    # exec(co)        # not needed for HW3
    # modded code = mutate(code)
    # write(code) dont mutate code itself!!


