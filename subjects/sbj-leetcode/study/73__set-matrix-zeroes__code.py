# https://leetcode.com/problems/set-matrix-zeroes/?envType=study-plan-v2&envId=top-interview-150
# 73. Set Matrix Zeroes
# Medium
# 13.3K
# 658
# Companies
#
# Given an m x n integer matrix matrix, if an element is 0, set its entire row and column to 0's.
#
# You must do it in place.
class Solution(object):
    def setZeroes(self, matrix):
        """
        :type matrix: List[List[int]]
        :rtype: None Do not return anything, modify matrix in-place instead.
        """
        if len(matrix) == 0:
            return

        n = len(matrix)
        m = len(matrix[0])
        where_zeros = []

        for i in range(n):
            for j in range(m):
                if matrix[i][j] == 0:
                    where_zeros.append((i,j))

        for i,j in where_zeros:
            for k in range(m):
                matrix[i][k] = 0
            for k in range(n):
                matrix[k][j] = 0


