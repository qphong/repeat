# https://leetcode.com/problems/gas-station/?envType=study-plan-v2&envId=top-interview-150
# 134. Gas Station
# Medium
# 11K
# 960
# Companies
#
# There are n gas stations along a circular route, where the amount of gas at the ith station is gas[i].
#
# You have a car with an unlimited gas tank and it costs cost[i] of gas to travel from the ith station to its next (i + 1)th station. You begin the journey with an empty tank at one of the gas stations.
#
# Given two integer arrays gas and cost, return the starting gas station's index if you can travel around the circuit once in the clockwise direction, otherwise return -1. If there exists a solution, it is guaranteed to be unique

class Solution(object):
    def canCompleteCircuit(self, gas, cost):
        """
        :type gas: List[int]
        :type cost: List[int]
        :rtype: int
        """
        start = 0
        remain_gas = gas[start]

        cur = start
        nxt = (cur+1) % len(gas)

        while nxt != start:

            remain_gas -= cost[cur]

            if remain_gas < 0:
                if nxt <= start:
                    return -1

                start = nxt
                remain_gas = gas[start]
                cur = start
                nxt = (cur+1) % len(gas)

            else:
                cur = nxt
                remain_gas += gas[cur]
                nxt = (cur + 1) % len(gas)

        if remain_gas - cost[cur] < 0:
            return -1

        return start

if __name__ == "__main__":
    gas = [2,3,4]
    cost = [3,4,3]

    ans = Solution().canCompleteCircuit(gas, cost)
    print(ans)
