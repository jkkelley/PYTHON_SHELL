"""
    Given an integer array nums sorted in non-decreasing order
    return an array of the squares of each number sorted in non-decreasing order.
"""

from collections import deque


nums = [-4,-1,0,3,10]
# Output: [0,1,9,16,100]

# Explanation: After squaring, the array becomes [16,1,0,9,100].
# After sorting, it becomes [0,1,9,16,100].

def sortedSquares(nums: list[int]):
    answer = deque()
    l, r = 0, len(nums) - 1
    while l <= r:
        left, right = abs(nums[l]), abs(nums[r])
        if left > right:
            answer.appendleft(left * left)
            l += 1
            print(answer)
        else:
            answer.appendleft(right * right)
            r -= 1
            print(answer)
    return list(answer)

# def sortedSquares(nums: list[int]):

#     ret_square_list = []

#     left = 0
#     right = len(nums) - 1

#     while left <= right:
#         left_sqaured = nums[left] * nums[left]
#         right_squared = nums[right] * nums[right]

#         if left_sqaured > right_squared:
#             ret_square_list.append(left_sqaured)
#             left += 1
#         else:
#             ret_square_list.append(right_squared)
#             right -= 1
    
#     ret_square_list.reverse()
#     return ret_square_list



# def sortedSquares(nums: list[int]):
#     """
#     :type nums: list[int]
#     :rtype: list[int]
#     """

#     ret_square_list = []

#     left = 0
#     right = len(nums) - 1
    
#     # print(low_val)
#     # print(high_val)

#     while left <= right:
#         left_square = nums[left] ** 2
#         right_square = nums[right] ** 2

#         print(left_square)
#         print(right_square)
#         # break
#         if left_square > right_square:
#             ret_square_list.append(left_square)
#             left += 1
#         else:
#             ret_square_list.append(right_square)
#             right -= 1
    
#     ret_square_list.reverse()
#     print(ret_square_list)
#     return ret_square_list


# def sortedSquares(nums: list[int]):
#     """
#     :type nums: list[int]
#     :rtype: list[int]
#     """

#     ret_square_list = []

#     for num in nums:
#         # print(num ** 2)
#         ret_square_list.append(num ** 2)
#     # print(sorted(ret_square_list))
#     return sorted(ret_square_list)

print(sortedSquares(nums))