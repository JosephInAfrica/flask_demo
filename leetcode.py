class Solution:

    nums = [11, 7, 2, 15]
    target = 9

    def twoSum(self, nums, target):
        length = len(nums)
        for i in range(length):
            for j in range(i + 1, length):
                if nums[i] + nums[j] == target:
                    return [i, j]


s = Solution()
print(s.twoSum(s.nums, s.targe)