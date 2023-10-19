# https://leetcode.com/problems/longest-consecutive-sequence/?envType=study-plan-v2&envId=top-interview-150
# 128. Longest Consecutive Sequence
# Medium
# 18.5K
# 838
# Companies
#
# Given an unsorted array of integers nums, return the length of the longest consecutive elements sequence.
#
# You must write an algorithm that runs in O(n) time.
#
#
#
# Example 1:
#
# Input: nums = [100,4,200,1,3,2]
# Output: 4
# Explanation: The longest consecutive elements sequence is [1, 2, 3, 4]. Therefore its length is 4.

class Solution(object):
    def longestConsecutive_1attemp_fail(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        prev = {}
        nxt= {}
        maxlen = 0

        for n in nums:
            prev[n] = nxt[n] = n

        for n in nums:
            if n-1 in prev:
                prev[n] = prev[n-1]
                nxt[prev[n]] = nxt[n]

            if n+1 in nxt:
                nxt[n] = nxt[n+1]
                prev[nxt[n]] = prev[n]

            nxt[prev[n]] = nxt[n] # note this step
            maxlen = max(maxlen, nxt[n] - prev[n] + 1)

        return maxlen

    def longestConsecutive(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        prev = {}
        nxt= {}
        maxlen = 1 if len(nums) else 0

        for n in nums:
            prev[n] = min(prev.get(n,n), prev.get(n-1,1e10))
            nxt[n] = max(nxt.get(n,n), nxt.get(n+1,-1e10))

            prev[nxt[n]] = min(prev[n], prev.get(nxt[n],1e10))
            nxt[prev[n]] = max(nxt[n], nxt.get(prev[n],-1e10))

            maxlen = max(maxlen, nxt[prev[n]] - prev[nxt[n]] + 1)

        return maxlen

