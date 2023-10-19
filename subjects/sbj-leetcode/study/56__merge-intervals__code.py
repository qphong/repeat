# https://leetcode.com/problems/merge-intervals/?envType=study-plan-v2&envId=top-interview-150
# 56. Merge Intervals
# Medium
# 21K
# 710
# Companies
#
# Given an array of intervals where intervals[i] = [starti, endi], merge all overlapping intervals, and return an array of the non-overlapping intervals that cover all the intervals in the input.
#
#
#
# Example 1:
#
# Input: intervals = [[1,3],[2,6],[8,10],[15,18]]
# Output: [[1,6],[8,10],[15,18]]
# Explanation: Since intervals [1,3] and [2,6] overlap, merge them into [1,6].
class Solution(object):
    def merge(self, intervals):
        """
        :type intervals: List[List[int]]
        :rtype: List[List[int]]
        """
        # sort left ends in increasing order
        # if an interval does not overlap, all following intervals does not overlap
        left_sorted_intervals = sorted(intervals)
        max_right = -1
        new_left = -1

        ans = []

        for left, right in left_sorted_intervals:

            if left > max_right:
                max_right = right
                new_left = left
                ans.append([new_left, max_right])

            else:
                max_right = max(max_right, right)
                ans[-1][1] = max_right

        return ans
