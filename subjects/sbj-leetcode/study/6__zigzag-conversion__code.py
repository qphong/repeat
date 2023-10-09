# https://leetcode.com/problems/zigzag-conversion/?envType=study-plan-v2&envId=top-interview-150

# 6. Zigzag Conversion
# Medium
# 6.8K
# 13.4K
# Companies
#
# The string "PAYPALISHIRING" is written in a zigzag pattern on a given number of rows like this: (you may want to display this pattern in a fixed font for better legibility)
#
# P   A   H   N
# A P L S I I G
# Y   I   R
#
# And then read line by line: "PAHNAPLSIIGYIR"
#
# Write the code that will take a string and make this conversion given a number of rows:
#
# string convert(string s, int numRows);

class Solution(object):
    def convert(self, s, numRows):
        """
        :type s: str
        :type numRows: int
        :rtype: str
        """
        if numRows == 1:
            return s

        rows = ["" for _ in range(numRows)]
        direction = 1
        i = 0

        for c in s:
            rows[i] += c
            if i == 0 and direction == -1:
                direction = 1
            elif i == numRows - 1 and direction == 1:
                direction = -1

            i += direction

        return ''.join(rows)


