# https://leetcode.com/problems/game-of-life/?envType=study-plan-v2&envId=top-interview-150
# 289. Game of Life
# Medium
# 6K
# 514
# Companies
#
# According to Wikipedia's article: "The Game of Life, also known simply as Life, is a cellular automaton devised by the British mathematician John Horton Conway in 1970."
#
# The board is made up of an m x n grid of cells, where each cell has an initial state: live (represented by a 1) or dead (represented by a 0). Each cell interacts with its eight neighbors (horizontal, vertical, diagonal) using the following four rules (taken from the above Wikipedia article):
#
#     Any live cell with fewer than two live neighbors dies as if caused by under-population.
#     Any live cell with two or three live neighbors lives on to the next generation.
#     Any live cell with more than three live neighbors dies, as if by over-population.
#     Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction.
#
# The next state is created by applying the above rules simultaneously to every cell in the current state, where births and deaths occur simultaneously. Given the current state of the m x n grid board, return the next state.
class Solution(object):
    def gameOfLife(self, board):
        """
        :type board: List[List[int]]
        :rtype: None Do not return anything, modify board in-place instead.
        """
        n = len(board)
        if n == 0:
            return board

        m = len(board[0])

        live = [[0] * m for _ in range(n)]

        for i in range(n):
            for j in range(m):
                for i1, j1 in [
                    [i - 1, j],
                    [i, j - 1],
                    [i - 1, j - 1],
                    [i + 1, j],
                    [i, j + 1],
                    [i + 1, j + 1],
                    [i - 1, j + 1],
                    [i + 1, j - 1],
                ]:
                    if i1 >= 0 and j1 >= 0 and i1 < n and j1 < m:
                        live[i][j] += board[i1][j1]

        for i in range(n):
            for j in range(m):
                if board[i][j] == 0:
                    if live[i][j] == 3:
                        board[i][j] = 1
                else:
                    if live[i][j] < 2:
                        board[i][j] = 0
                    elif live[i][j] > 3:
                        board[i][j] = 0
        return board
