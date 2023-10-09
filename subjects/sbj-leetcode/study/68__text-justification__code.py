# https://leetcode.com/problems/text-justification/?envType=study-plan-v2&envId=top-interview-150
# 68. Text Justification
# Hard
# 3.3K
# 4.3K
# Companies
#
# Given an array of strings words and a width maxWidth, format the text such that each line has exactly maxWidth characters and is fully (left and right) justified.
#
# You should pack your words in a greedy approach; that is, pack as many words as you can in each line. Pad extra spaces ' ' when necessary so that each line has exactly maxWidth characters.
#
# Extra spaces between words should be distributed as evenly as possible. If the number of spaces on a line does not divide evenly between words, the empty slots on the left will be assigned more spaces than the slots on the right.
#
# For the last line of text, it should be left-justified, and no extra space is inserted between words.
#
# Note:
#
#     A word is defined as a character sequence consisting of non-space characters only.
#     Each word's length is guaranteed to be greater than 0 and not exceed maxWidth.
#     The input array words contains at least one word.
#
class Solution(object):
    def fullJustify(self, words, maxWidth):
        """
        :type words: List[str]
        :type maxWidth: int
        :rtype: List[str]
        """
        curlen = 0
        prev = 0
        justified = []

        for i, word in enumerate(words):
            curlen += len(word)
            n_spaces = i - prev

            if curlen + n_spaces > maxWidth:
                # justify this line of words[prev:i]
                n_gap = i - prev - 1
                ttl_spaces = maxWidth - curlen + len(word)

                if n_gap > 0:
                    equal_spaces = ttl_spaces // n_gap
                    remain_spaces = ttl_spaces % n_gap

                    spaces = [equal_spaces + 1] * remain_spaces + [equal_spaces] * (
                        n_gap - remain_spaces
                    )

                    line = [words[prev]]
                    for j, w in enumerate(words[prev + 1 : i]):
                        line.extend([" " * spaces[j], w])

                    justified.append("".join(line))

                else:  # n_gap == 0
                    justified.append(words[prev] + " " * ttl_spaces)

                curlen = len(word)
                prev = i

        line = " ".join(words[prev:])
        justified.append(line + " " * (maxWidth - len(line)))

        return justified


if __name__ == "__main__":
    words = ["This", "is", "an", "example", "of", "text", "justification."]
    maxWidth = 16
    ans = Solution().fullJustify(words, maxWidth)
    print(ans)
