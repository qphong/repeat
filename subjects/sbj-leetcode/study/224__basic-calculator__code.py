# https://leetcode.com/problems/basic-calculator/?envType=study-plan-v2&envId=top-interview-150
# 224. Basic Calculator
# Hard
# 5.9K
# 431
# Companies
#
# Given a string s representing a valid expression, implement a basic calculator to evaluate it, and return the result of the evaluation.
#
# Note: You are not allowed to use any built-in function which evaluates strings as mathematical expressions, such as eval().
#
#
#
# Example 1:
#
# Input: s = "1 + 1"
# Output: 2
#
# Example 2:
#
# Input: s = " 2-1 + 2 "
# Output: 3
#
# Example 3:
#
# Input: s = "(1+(4+5+2)-3)+(6+8)"
# Output: 23
class Solution(object):
    def calculate(self, s):
        """
        :type s: str
        :rtype: int
        """

