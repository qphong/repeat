# https://leetcode.com/problems/remove-element/?envType=study-plan-v2&envId=top-interview-150

# 27. Remove Element
# Easy
# 1.3K
# 1.8K
# Companies
#
# Given an integer array nums and an integer val, remove all occurrences of val in nums in-place. The order of the elements may be changed. Then return the number of elements in nums which are not equal to val.
#
# Consider the number of elements in nums which are not equal to val be k, to get accepted, you need to do the following things:
#
#     Change the array nums such that the first k elements of nums contain the elements which are not equal to val. The remaining elements of nums are not important as well as the size of nums.
#     Return k.

class Solution(object):
    def removeElement(self, nums, val):
        """
        :type nums: List[int]
        :type val: int
        :rtype: int
        """
        k = len(nums) - 1
        i = 0

        while i <= k:
            if nums[i] == val:
                nums[i], nums[k] = nums[k], nums[i]
                k -= 1
            else:
                i += 1

        return k+1

