# https://leetcode.com/problems/spiral-matrix/?envType=study-plan-v2&envId=top-interview-150
# 54. Spiral Matrix
# Medium
# 13.6K
# 1.2K
# Companies
#
# Given an m x n matrix, return all elements of the matrix in spiral order.
class Solution(object):
    def spiralOrder(self, matrix):
        """
        :type matrix: List[List[int]]
        :rtype: List[int]
        """
        if len(matrix) == 0 or len(matrix[0]) == 0:
            return []

        top, left = 0, 0
        bottom, right = len(matrix) - 1, len(matrix[0]) - 1

        states = ["first_row", "last_col", "last_row", "first_col"]
        state_i = 0
        ans = []

        while top <= bottom and left <= right:

            if states[state_i] == "first_row":
                ans.extend(matrix[top][left:right+1])
                top += 1

            elif states[state_i] == "last_row":
                ans.extend(matrix[bottom][left:right+1][::-1])
                bottom -= 1

            elif states[state_i] == "first_col":
                for i in range(bottom, top-1, -1):
                    ans.append(matrix[i][left])
                left += 1

            elif states[state_i] == "last_col":
                for i in range(top, bottom+1):
                    ans.append(matrix[i][right])
                right -= 1

            state_i = (state_i + 1) % len(states)

        return ans
