# https://leetcode.com/problems/valid-sudoku/?envType=study-plan-v2&envId=top-interview-150
# 36. Valid Sudoku
# Medium
# 9.8K
# 1K
# Companies
#
# Determine if a 9 x 9 Sudoku board is valid. Only the filled cells need to be validated according to the following rules:
#
#     Each row must contain the digits 1-9 without repetition.
#     Each column must contain the digits 1-9 without repetition.
#     Each of the nine 3 x 3 sub-boxes of the grid must contain the digits 1-9 without repetition.
#
# Note:
#
#     A Sudoku board (partially filled) could be valid but is not necessarily solvable.
#     Only the filled cells need to be validated according to the mentioned rules.
#
class Solution(object):
    def isValidSudoku(self, board):
        """
        :type board: List[List[str]]
        :rtype: bool
        """
        distinct_in_col = [set() for _ in range(9)]
        if j % 3 == 0:
            distinct_in_submatrix = [set() for _ in range(3)]

        # check valid rows and cols
        for j,row in enumerate(board):
            distinct = set()
            for i,n in enumerate(row):
                if n == '.':
                    continue

                if n in distinct:
                    return False
                distinct.add(n)

                if n in distinct_in_col[i]:
                    return False
                distinct_in_col[i].add(n)

                subi = ((j // 3) * 3 + (i // 3)) % 3

                if n in distinct_in_submatrix[subi]:
                    return False
                distinct_in_submatrix[subi].add(n)

        return True
