# https://leetcode.com/problems/reverse-words-in-a-string/?envType=study-plan-v2&envId=top-interview-150
# 151. Reverse Words in a String
# Medium
# 7.4K
# 4.9K
# Companies
#
# Given an input string s, reverse the order of the words.
#
# A word is defined as a sequence of non-space characters. The words in s will be separated by at least one space.
#
# Return a string of the words in reverse order concatenated by a single space.
#
# Note that s may contain leading or trailing spaces or multiple spaces between two words. The returned string should only have a single space separating the words. Do not include any extra spaces.

class Solution(object):
    def reverseWords(self, s):
        """
        :type s: str
        :rtype: str
        """
        words = s.split()
        return ' '.join(words[::-1])
