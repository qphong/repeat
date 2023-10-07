# https://leetcode.com/problems/majority-element/?envType=study-plan-v2&envId=top-interview-150
# 169. Majority Element
# Easy
# 17.2K
# 505
# Companies
#
# Given an array nums of size n, return the majority element.
#
# The majority element is the element that appears more than ⌊n / 2⌋ times. You may assume that the majority element always exists in the array.

from collections import defaultdict

class Solution(object):
    def majorityElement(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        count = defaultdict(int)
        for n in nums:
            count[n] += 1
            if count[n] > len(nums) / 2:
                return n

