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
# random.seed("value")
# randint(1, 100) returns random number 1 to 100 inclusive. Use for mutation
class MyVisitor(ast.NodeTransformer):
    """Notes all Numbers and all Strings. Replaces all numbers with 481 and
    strings with 'SE'."""

    # Note how we never say "if node.type == Number" or anything like that.
    # The Visitor Pattern hides that information from us. Instead, we use
    # these visit_Num() functions and the like, which are called
    # automatically for us by the library. 
    def visit_Num(self, node):
	#edit program you take as input, determines what num to visit.
        print("Visitor sees a number: ", ast.dump(node), " aka ", astor.to_source(node))
        # Note how we never say "node.contents = 481" or anything like
        # that. We do not directly assign to nodes. Intead, the Visitor
        # Pattern hides that information from us. We use the return value
        # of this function and the new node we return is put in place by
        # the library. 
        # Note: some students may want: return ast.Num(n=481) 
        return ast.Num(value=481, kind=None)

    def visit_Str(self, node):
        print("Visitor sees a string: ", ast.dump(node), " aka ", astor.to_source(node))
        # Note: some students may want: return ast.Str(s=481)
        return ast.Str(value="SE", kind=None)
    
    def visit_BinOp(self, node):
        return None

    def visit_IfExp(self, node):
        print("Visitor sees an IfExp:", ast.dump(node), " aka ", astor.to_source(node))
        test = self.visit(node.test)
        body = self.visit(node.body)
        orelse = self.visit(node.orelse)
        return ast.IfExp(test, body, orelse)
    
    def visit_Compare(self, node):
        print("Visitor sees a Compare:", ast.dump(node), " aka ", astor.to_source(node))
        left = self.visit(node.left) if node.left is not None else None
        ops = [self.visit(op) for op in node.ops]
        comparators = [self.visit(comp) for comp in node.comparators]
        
        if None in (left, *ops, *comparators):
            # If any of the nodes is None, return the original node
            return node

        return ast.Compare(left=left, ops=ops, comparators=comparators)
    
    def visit_Assign(self, node):
        print("Visitor sees an Assign:", ast.dump(node), " aka ", astor.to_source(node))

        # Check if the assignment has a value and targets
        if node.value is not None and node.targets:
            # Visit the assigned value
            value = self.visit(node.value)

            # Visit targets
            targets = [self.visit(target) for target in node.targets]

            # Return a new Assign node with the modified values
            return ast.Assign(targets=targets, value=value)
        else:
            # If either value or targets is None, return the original node
            return node
# code that runs first 
# Instead of reading from a file, the starter code always processes in 
# a small Python expression literally written in this string below: 
# Assuming fuzzywuzzy.py is in the same directory as this script
file_path = "fuzzywuzzy.py"

# Read the contents of the file
with open(file_path, "r") as file:
    code = file.read()

# As a sanity check, we'll make sure we're reading the code
# correctly before we do any processing. 
print("Before any AST transformation")
print("Code is: ", code)
print("Code's output is:") 
exec(code)      # not needed for HW3
print()

# Now we will apply our transformation. 
print("Applying AST transformation")
tree = ast.parse(code)
tree = MyVisitor().visit(tree)
# Add lineno & col_offset to the nodes we created
ast.fix_missing_locations(tree)
print("Transformed code is: ", astor.to_source(tree))
co = compile(tree, "", "exec")
print("Transformed code's output is:") 
exec(co)        # not needed for HW3
# modded code = mutate(code)
# write(code) dont mutate code itself!!
