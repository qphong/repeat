# https://leetcode.com/problems/rotate-image/?envType=study-plan-v2&envId=top-interview-150
# 48. Rotate Image
# Medium
# 16.3K
# 713
# Companies
#
# You are given an n x n 2D matrix representing an image, rotate the image by 90 degrees (clockwise).
#
# You have to rotate the image in-place, which means you have to modify the input 2D matrix directly. DO NOT allocate another 2D matrix and do the rotation.
class Solution(object):
    def rotate(self, matrix):
        """
        :type matrix: List[List[int]]
        :rtype: None Do not return anything, modify matrix in-place instead.
        """
        n = len(matrix)
        if n <= 1:
            return

        left = 0
        right = n - 1

        while left < right:
            # rotate the boundary of radius
            for i in range(left, right):
                j = n - 1 - i

                (
                    matrix[left][i],
                    matrix[i][right],
                    matrix[right][j],
                    matrix[j][left],
                ) = (
                    matrix[j][left],
                    matrix[left][i],
                    matrix[i][right],
                    matrix[right][j],
                )

            left += 1
            right -= 1


if __name__ == "__main__":
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    matrix = [[5, 1, 9, 11], [2, 4, 8, 10], [13, 3, 6, 7], [15, 14, 12, 16]]
    Solution().rotate(matrix)
    print(matrix)
