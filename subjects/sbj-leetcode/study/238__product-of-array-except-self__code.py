# https://leetcode.com/problems/product-of-array-except-self/?envType=study-plan-v2&envId=top-interview-150
# 238. Product of Array Except Self
# Medium
# 20.2K
# 1.2K
# Companies
#
# Given an integer array nums, return an array answer such that answer[i] is equal to the product of all the elements of nums except nums[i].
#
# The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer.
#
# You must write an algorithm that runs in O(n) time and without using the division operation.

class Solution(object):
    def productExceptSelf(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """
        left = [1] * len(nums)
        right = [1] * len(nums)

        for i in range(len(nums)-1):
            left[i+1] = left[i] * nums[i]

            right_i = len(nums)-2-i
            right[right_i] = right[right_i + 1] * nums[right_i + 1]

        ans = right
        for i in range(len(nums)):
            ans[i] *= left[i]

        return ans
