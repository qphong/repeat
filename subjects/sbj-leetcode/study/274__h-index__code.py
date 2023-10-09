# https://leetcode.com/problems/h-index/?envType=study-plan-v2&envId=top-interview-150

# 274. H-Index
# Medium
# 764
# 266
# Companies
#
# Given an array of integers citations where citations[i] is the number of citations a researcher received for their ith paper, return the researcher's h-index.
#
# According to the definition of h-index on Wikipedia: The h-index is defined as the maximum value of h such that the given researcher has published at least h papers that have each been cited at least h times.
#
class Solution(object):
    def hIndex(self, citations):
        """
        :type citations: List[int]
        :rtype: int
        """
        dec_citations = sorted(citations)[::-1] + [0]

        for i,cite in enumerate(dec_citations):
            if cite < i + 1:
                return i

        return 0

