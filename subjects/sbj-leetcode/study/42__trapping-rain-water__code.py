# https://leetcode.com/problems/trapping-rain-water/?envType=study-plan-v2&envId=top-interview-150
# 42. Trapping Rain Water
# Hard
# 29.4K
# 420
# Companies
#
# Given n non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.
class Solution(object):
    def trap(self, height):
        """
        :type height: List[int]
        :rtype: int
        """
        height = [0] + height + [0]

        left_i = 0
        left = height[left_i]

        water = 0
        middle_height = 0

        for i in range(1,len(height)):
            if height[i] >= left:
                water += (i - left_i - 1) * min(height[i], left) - middle_height
                left_i = i
                left = height[left_i]
                middle_height = 0
            else:
                middle_height += height[i]

        right_i = len(height) - 1
        right = height[right_i]
        middle_height = 0
        for i in range(len(height)-2, -1, -1):
            if height[i] > right:
                water += (right_i - i - 1) * min(height[i], right) - middle_height
                right_i = i
                right = height[right_i]
                middle_height = 0
            else:
                middle_height += height[i]

        return water
