from typing import List
class Solution:
    def is_integer(self,s):
        try:
            int(s)
            return True
        except ValueError:
            return False
    def evalRPN(self, tokens: List[str]) -> int:
        ops = {'+':lambda x,y:x+y, '-':lambda x,y:x-y, '*':lambda x,y:x*y, '/':lambda x,y:int(x/y)}
        stack=[]
        for i in range(len(tokens)):
            if self.is_integer(tokens[i]):
                stack.append(int(tokens[i]))
            elif tokens[i] in ops:
                a=stack.pop()
                b=stack.pop()
                result = ops[tokens[i]](b,a)
                stack.append(result)
                print(stack)

        return stack.pop()
solution = Solution()
print(solution.evalRPN(["10","6","9","3","+","-11","*","/","*","17","+","5","+"]))