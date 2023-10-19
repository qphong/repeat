# https://leetcode.com/problems/minimum-window-substring/?envType=study-plan-v2&envId=top-interview-150
# 76. Minimum Window Substring
# Hard
# 16.3K
# 672
# Companies
#
# Given two strings s and t of lengths m and n respectively, return the minimum window
# substring
# of s such that every character in t (including duplicates) is included in the window. If there is no such substring, return the empty string "".
#
# The testcases will be generated such that the answer is unique.
class Solution(object):
    def minWindow(self, s, t):
        """
        :type s: str
        :type t: str
        :rtype: str
        """
        if len(s) == 0 or len(t) == 0:
            return ""

        c2i = lambda c: ord(c) - ord('A')
        count_t = [0] * (c2i('z')+1)

        ttl_t = 0
        for c in t:
            count_t[c2i(c)] += 1
            ttl_t += 1

        len_substr_s_contain_t = 0
        count_s = [0] * (c2i('z')+1)
        l = 0

        minlen = 1e9
        ans_l, ans_r = 0,0

        for r,c in enumerate(s):
            i_r = c2i(c)
            count_s[i_r] += 1

            if count_s[i_r] <= count_t[i_r]:
                len_substr_s_contain_t += 1

            if len_substr_s_contain_t >= ttl_t:
                while True:
                    i_l = c2i(s[l])
                    if count_s[i_l] == count_t[i_l] and count_t[i_l] > 0:
                        break
                    count_s[i_l] -= 1
                    l += 1

                if minlen > r - l + 1:
                    minlen = r - l + 1
                    ans_l = l
                    ans_r = r + 1

        if len_substr_s_contain_t < ttl_t:
            return ""

        return s[ans_l:ans_r]


if __name__ == "__main__":
    s = "ab"
    t = "a"
    ans = Solution().minWindow(s,t)
    print(ans)

