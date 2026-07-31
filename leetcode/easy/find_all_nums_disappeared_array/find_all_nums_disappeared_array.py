"""
    Given an array nums of n integers where nums[i] is in the range [1, n],
    return an array of all the integers in the range [1, n] that do not appear in nums.
"""

nums = [4,3,2,7,8,2,3,1]

# Time Complexity: O(N) iterate thru range, append to new list in not in given list
# Space Complexity: O(N)
# def findDisappearedNumbers(nums):
#     ret = []
#     set_nums = set(nums)
#     for i in range(1, len(nums)+1):
#         if i not in set_nums:
#             ret.append(i)
#     return ret

def findDisappearedNumbers(nums):
    for i in range(len(nums)):
        temp = abs(nums[i]) - 1
        if nums[temp] > 0:
            nums[temp] *= -1
    
    res = []

    for i,n in enumerate(nums):
        if n > 0:
            res.append(i + 1)
    
    return res

result = findDisappearedNumbers(nums)
print(result)

