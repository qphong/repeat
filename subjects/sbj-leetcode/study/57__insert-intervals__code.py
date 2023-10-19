# https://leetcode.com/problems/insert-interval/?envType=study-plan-v2&envId=top-interview-150
# 57. Insert Interval
# Medium
# 9.1K
# 667
# Companies
#
# You are given an array of non-overlapping intervals intervals where intervals[i] = [starti, endi] represent the start and the end of the ith interval and intervals is sorted in ascending order by starti. You are also given an interval newInterval = [start, end] that represents the start and end of another interval.
#
# Insert newInterval into intervals such that intervals is still sorted in ascending order by starti and intervals still does not have any overlapping intervals (merge overlapping intervals if necessary).
#
# Return intervals after the insertion.
#
#
#
# Example 1:
#
# Input: intervals = [[1,3],[6,9]], newInterval = [2,5]
# Output: [[1,5],[6,9]]
import bisect

class Solution(object):
    def insert(self, intervals, newInterval):
        """
        :type intervals: List[List[int]]
        :type newInterval: List[int]
        :rtype: List[List[int]]
        """
        idx = bisect.bisect_left(intervals, newInterval)

        new_start = newInterval[0]
        new_end = newInterval[1]

        start = idx - 1
        if start < 0:
            prefix = []

        else:
            while start >= 0 and intervals[start][1] >= newInterval[0]:
                new_start = min(new_start, intervals[start][0])
                new_end = max(new_end, intervals[start][1]) # note: idx is only based on starti
                start -= 1
            start += 1
            prefix = intervals[:start]

        end = idx
        if end == len(intervals):
            postfix = []

        else:
            while end < len(intervals) and intervals[end][0] <= newInterval[1]:
                new_end = max(new_end, intervals[end][1])
                end += 1
            end -= 1
            postfix = intervals[end+1:]

        return prefix + [[new_start, new_end]] + postfix


