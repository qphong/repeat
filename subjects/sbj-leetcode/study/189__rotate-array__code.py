# https://leetcode.com/problems/rotate-array/?envType=study-plan-v2&envId=top-interview-150
# 189. Rotate Array
# Medium
# 16.4K
# 1.8K
# Companies
#
# Given an integer array nums, rotate the array to the right by k steps, where k is non-negative.

class Solution(object):
    def rotate(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: None Do not return anything, modify nums in-place instead.
        """
        if k == 0:
            return

        i = len(nums) - k
        rotated_nums = [0] * len(nums)

        for j in range(len(nums)):
            idx = i % len(nums)
            rotated_nums[j] = nums[idx]
            i += 1

        for i in range(len(nums)):
            nums[i] = rotated_nums[i]

