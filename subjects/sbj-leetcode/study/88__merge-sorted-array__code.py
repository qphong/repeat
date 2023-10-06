# https://leetcode.com/problems/merge-sorted-array/?envType=study-plan-v2&envId=top-interview-150

# 88. Merge Sorted Array
# Easy
# 12.8K
# 1.4K
# Companies
#
# You are given two integer arrays nums1 and nums2, sorted in non-decreasing order, and two integers m and n, representing the number of elements in nums1 and nums2 respectively.
#
# Merge nums1 and nums2 into a single array sorted in non-decreasing order.
#
# The final sorted array should not be returned by the function, but instead be stored inside the array nums1. To accommodate this, nums1 has a length of m + n, where the first m elements denote the elements that should be merged, and the last n elements are set to 0 and should be ignored. nums2 has a length of n.

class Solution(object):
    def merge(self, nums1, m, nums2, n):
        """
        :type nums1: List[int]
        :type m: int
        :type nums2: List[int]
        :type n: int
        :rtype: None Do not return anything, modify nums1 in-place instead.
        """
        i1 = 0
        i2 = 0
        i = 0
        nums = [0] * (m+n)

        while i1 < m and i2 < n:
            if nums1[i1] <  nums2[i2]:
                nums[i] = nums1[i1]
                i1 += 1
            else:
                nums[i] = nums2[i2]
                i2 += 1
            i += 1

        while i1 < m:
            nums[i] = nums1[i1]
            i1 += 1
            i += 1

        while i2 < n:
            nums[i] = nums2[i2]
            i2 += 1
            i += 1

        for i in range(m+n):
            nums1[i] = nums[i]


