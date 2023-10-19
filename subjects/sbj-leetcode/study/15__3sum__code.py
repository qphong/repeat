# https://leetcode.com/problems/3sum/?envType=study-plan-v2&envId=top-interview-150
# 15. 3Sum
# Medium
# 28.7K
# 2.6K
# Companies
#
# Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]] such that i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0.
#
# Notice that the solution set must not contain duplicate triplets.
class Solution(object):
    def threeSum(self, nums):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        """
        ans = set()
        nums = sorted(nums)
        for i,target in enumerate(nums):
            l,r = i+1, len(nums)-1
            while l < r:
                s = nums[l] + nums[r]
                if s > -target:
                    r -= 1
                elif s < -target:
                    l += 1
                else:
                    ans.add((nums[i], nums[l], nums[r]))
                    l += 1
                    r -= 1
        return list(ans)

if __name__ == "__main__":
    nums = [3,0,-2,-1,1,2]
    ans = Solution().threeSum(nums)
    print(ans)
