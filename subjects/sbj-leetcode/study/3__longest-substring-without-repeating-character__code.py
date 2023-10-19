# https://leetcode.com/problems/longest-substring-without-repeating-characters/description/?envType=study-plan-v2&envId=top-interview-150
# 3. Longest Substring Without Repeating Characters
# Medium
# 37.4K
# 1.7K
# Companies
#
# Given a string s, find the length of the longest
# substring
# without repeating characters.

class Solution(object):
    def lengthOfLongestSubstring(self, s):
        """
        :type s: str
        :rtype: int
        """
        if len(s) == 0:
            return 0

        ans = 1
        l = 0
        count = [False] * 256
        count[ord(s[l])] = True

        for r in range(1,len(s)):
            while count[ord(s[r])] and l < r:
                count[ord(s[l])] = False
                l += 1

            count[ord(s[r])] = True
            ans = max(ans, r - l + 1)

        return ans



