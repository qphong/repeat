Initially, I tried l,r = 0, len(nums) -1, i.e., from the largest subarray, and narrowing down by removing the edge with a smaller value. However, this approach does not work.

E.g.,
target = 20
10,1,1,5,5,9 -> remove the smaller edge -> 10,1,1,5,5 (22) -> stop with len = 5
but the smallest length is 1,5,5,9 (len = 4)

Therefore, the above intuition is incorrect.
The correct gist is that if sum(nums[i:j]) < target, we do not need to scan for subarray of [i:j].
Hence, we need to scan from left to right. Plus, the numbers in nums are positive.
