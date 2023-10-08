# https://leetcode.com/problems/best-time-to-buy-and-sell-stock/?envType=study-plan-v2&envId=top-interview-150
# 121. Best Time to Buy and Sell Stock
# Easy
# 28.6K
# 973
# Companies
#
# You are given an array prices where prices[i] is the price of a given stock on the ith day.
#
# You want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock.
#
# Return the maximum profit you can achieve from this transaction. If you cannot achieve any profit, return 0.


class Solution(object):
    def maxProfit(self, prices):
        """
        :type prices: List[int]
        :rtype: int
        """
        min_prev = 1e9
        max_profit = 0

        for p in prices:
            max_profit = max(max_profit, p - min_prev)
            min_prev = min(min_prev, p)
        return max_profit

