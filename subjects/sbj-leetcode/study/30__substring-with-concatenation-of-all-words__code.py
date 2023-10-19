# https://leetcode.com/problems/substring-with-concatenation-of-all-words/?envType=study-plan-v2&envId=top-interview-150
# 30. Substring with Concatenation of All Words
# Hard
# 1.4K
# 131
# Companies
#
# You are given a string s and an array of strings words. All the strings of words are of the same length.
#
# A concatenated substring in s is a substring that contains all the strings of any permutation of words concatenated.
#
#     For example, if words = ["ab","cd","ef"], then "abcdef", "abefcd", "cdabef", "cdefab", "efabcd", and "efcdab" are all concatenated strings. "acdbef" is not a concatenated substring because it is not the concatenation of any permutation of words.
#
# Return the starting indices of all the concatenated substrings in s. You can return the answer in any order.

from collections import defaultdict

class Solution(object):
    def findSubstring(self, s, words):
        """
        :type s: str
        :type words: List[str]
        :rtype: List[int]
        """
        wordlen = len(words[0])
        n_word = len(words)
        sublen = n_word * wordlen

        word_count = defaultdict(int)
        for i,word in enumerate(words):
            word_count[word] += 1

        word_in_s = [None] * len(s)
        for i in range(len(s)):
            w = s[i:i+wordlen]
            if w in word_count:
                word_in_s[i] = w

        ans = []

        for start in range(wordlen):
            word_count1 = {}
            for key in word_count:
                word_count1[key] = 0

            count = 0
            prev = start

            for i in range(start, len(s), wordlen):
                wi = word_in_s[i]

                if wi:
                    while word_count1[wi] == word_count[wi] and prev < i: # duplicate word
                        prev_wi = word_in_s[prev]
                        if prev_wi:
                            word_count1[prev_wi] -= 1
                            count -= 1

                        prev += wordlen

                    word_count1[wi] += 1
                    count += 1

                else:
                    prev = i+wordlen
                    count = 0
                    for key in word_count1:
                        word_count1[key] = 0

                if count == n_word:
                    ans.append(prev)
        return ans

if __name__ == "__main__":
    s = "wordgoodgoodgoodbestword"
    words = ["word","good","best","good"]
    ans = Solution().findSubstring(s, words)
    print(ans)
