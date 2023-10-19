# https://leetcode.com/problems/minimum-size-subarray-sum/?envType=study-plan-v2&envId=top-interview-150
# 209. Minimum Size Subarray Sum
# Medium
# 11.8K
# 352
# Companies
#
# Given an array of positive integers nums and a positive integer target, return the minimal length of a
# subarray
# whose sum is greater than or equal to target. If there is no such subarray, return 0 instead.
class Solution(object):
    def minSubArrayLen(self, target, nums):
        """
        :type target: int
        :type nums: List[int]
        :rtype: int
        """
        s = sum(nums)
        if s < target:
            return 0

        l = 0
        minlen = len(nums)
        s = nums[l]

        for r in range(1,len(nums)):
            s += nums[r]
            while s >= target and l <= r:
                minlen = min(minlen, r-l+1)
                s -= nums[l]
                l += 1

        return minlen

if __name__ == "__main__":
    nums = [1,4,4]
    target = 4
    ans = Solution().minSubArrayLen(target, nums)
    print(ans)
