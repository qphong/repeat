# https://leetcode.com/problems/jump-game/?envType=study-plan-v2&envId=top-interview-150
# 55. Jump Game
# Medium
# 17.9K
# 1K
# Companies
#
# You are given an integer array nums. You are initially positioned at the array's first index, and each element in the array represents your maximum jump length at that position.
#
# Return true if you can reach the last index, or false otherwise.

class Solution(object):
    def canJump(self, nums):
        """
        :type nums: List[int]
        :rtype: bool
        """
        max_reach = 0
        for i,n in enumerate(nums):
            if i > max_reach:
                return False
            max_reach = max(i + n, max_reach)
        return max_reach >= len(nums) - 1
