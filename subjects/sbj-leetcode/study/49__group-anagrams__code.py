# https://leetcode.com/problems/group-anagrams/?envType=study-plan-v2&envId=top-interview-150
# 49. Group Anagrams
# Medium
# 17.4K
# 515
# Companies
#
# Given an array of strings strs, group the anagrams together. You can return the answer in any order.
#
# An Anagram is a word or phrase formed by rearranging the letters of a different word or phrase, typically using all the original letters exactly once.
#
#
#
# Example 1:
#
# Input: strs = ["eat","tea","tan","ate","nat","bat"]
# Output: [["bat"],["nat","tan"],["ate","eat","tea"]]
#
# Example 2:
#
# Input: strs = [""]
# Output: [[""]]
class Solution(object):
    def groupAnagrams(self, strs):
        """
        :type strs: List[str]
        :rtype: List[List[str]]
        """
        unique_sorted_strs = {}

        for s in strs:
            ss = ''.join(sorted(s))
            if ss not in unique_sorted_strs:
                unique_sorted_strs[ss] = [s]
            else:
                unique_sorted_strs[ss].append(s)

        return unique_sorted_strs.values()

