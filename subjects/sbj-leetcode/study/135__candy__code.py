# https://leetcode.com/problems/candy/?envType=study-plan-v2&envId=top-interview-150
# 135. Candy
# Hard
# 7.2K
# 537
# Companies
#
# There are n children standing in a line. Each child is assigned a rating value given in the integer array ratings.
#
# You are giving candies to these children subjected to the following requirements:
#
#     Each child must have at least one candy.
#     Children with a higher rating get more candies than their neighbors.
#
# Return the minimum number of candies you need to have to distribute the candies to the children.

class Solution(object):
    def candy(self, ratings):
        """
        :type ratings: List[int]
        :rtype: int
        """
        candies = [1] * len(ratings)
        for i,r in enumerate(ratings[1:]):
            if r > ratings[i]:
                candies[i+1] = candies[i] + 1

        for i in range(len(ratings) - 2, -1, -1):
            if ratings[i] > ratings[i+1]:
                candies[i] = max(candies[i], candies[i+1] + 1)

        return sum(candies)

