
# contains N distict numbers > range [0, n]
# return num thats missing in range from the list
nums = [9,6,4,2,3,5,7,0,1]

# Time Complexity: O(nlogn)
#  - nums.sort() takes O(nlogn) time
#  - O(nlogn) grows faster than O(n)
# Space Complexity: O(n)
#  - 
# def missingNumber(nums):
#     nums.sort()
#     print(nums)
#     for i, v in enumerate(nums):
#         print(i, v)
#         if i != v:
#             return v-1
#         if i == len(nums) - 1:
#             return v + 1


# Time Complexity: O(n)
#   - sum(nums) iterates through list of size n exactly once, which takes O(n) time
#   - sum(range(len(nums) + 1)) iterates range obj, which takes O(n) time
#   - Adding them together gives O(2n) which == O(n) time complexity
# Space Complexity: O(1)
#   - range() gens nums on the fly
#   - Because we're keeping track of running total and not allocating any new lists, sets
#     dics, it uses constant extra space O(1)
# def missingNumber(nums):
#     return (sum(range(len(nums)+1))) - sum(nums)


# Time Complexity: O(n)
# Space Complexity: o(1)
# We eliminate one full iteration, resulting it being twice as fast
def missingNumber(nums):
    n = len(nums)
    expected_sum = n * (n + 1) // 2
    return expected_sum - sum(nums)

result = missingNumber(nums)
print(result)


