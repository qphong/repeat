# https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/?envType=study-plan-v2&envId=top-interview-150
# 122. Best Time to Buy and Sell Stock II
# Medium
# 12.6K
# 2.6K
# Companies
#
# You are given an integer array prices where prices[i] is the price of a given stock on the ith day.
#
# On each day, you may decide to buy and/or sell the stock. You can only hold at most one share of the stock at any time. However, you can buy it then immediately sell it on the same day.
#
# Find and return the maximum profit you can achieve.

class Solution(object):
    def maxProfit(self, prices):
        """
        :type prices: List[int]
        :rtype: int
        """
        profit = 0
        min_prev = 1e9
        for p in prices:
            min_prev = min(min_prev, p)

            if p > min_prev:
                profit += p - min_prev
                min_prev = p
        return profit



