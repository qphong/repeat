# https://leetcode.com/problems/container-with-most-water/?envType=study-plan-v2&envId=top-interview-150
# 11. Container With Most Water
# Medium
# 26.9K
# 1.5K
# Companies
#
# You are given an integer array height of length n. There are n vertical lines drawn such that the two endpoints of the ith line are (i, 0) and (i, height[i]).
#
# Find two lines that together with the x-axis form a container, such that the container contains the most water.
#
# Return the maximum amount of water a container can store.
#
# Notice that you may not slant the container.
#

class Solution(object):
    def maxArea(self, height):
        """
        :type height: List[int]
        :rtype: int
        """
        l = 0
        r = len(height) - 1
        max_area = min(height[l], height[r]) * (r - l)

        while l < r:
            if height[l] < height[r]:
                l += 1
            else:
                r -= 1

            max_area = max(max_area, min(height[l], height[r]) * (r-l))
        return max_area
