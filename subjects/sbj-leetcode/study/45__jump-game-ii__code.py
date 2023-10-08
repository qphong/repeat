# https://leetcode.com/problems/jump-game-ii/?envType=study-plan-v2&envId=top-interview-150
# 45. Jump Game II
# Medium
# 13.5K
# 480
# Companies
#
# You are given a 0-indexed array of integers nums of length n. You are initially positioned at nums[0].
#
# Each element nums[i] represents the maximum length of a forward jump from index i. In other words, if you are at nums[i], you can jump to any nums[i + j] where:
#
#     0 <= j <= nums[i] and
#     i + j < n
#
# Return the minimum number of jumps to reach nums[n - 1]. The test cases are generated such that you can reach nums[n - 1].

class Solution(object):
    def jump(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        if len(nums) <= 1:
            return 0

        min_jump = [1e9] * len(nums)
        min_jump[0] = 0

        for i,n in enumerate(nums):
            for j in range(i+1,min(len(nums),i+n+1)):
                min_jump[j] = min(min_jump[j], min_jump[i]+1)

        return min_jump[-1]

    def jump_linear_time(self, nums):
        if len(nums) < 2:
            return 0

        max_reach = [0] * len(nums)
        max_reach[0] = nums[0]

        for i,n in enumerate(nums[1:]):
            max_reach[i+1] = max(max_reach[i], i + 1 + n)

        n_jump = 1
        reach = max_reach[0]
        while reach < len(nums) - 1:
            reach = max_reach[reach]
            n_jump += 1

        return n_jump

