"""
    Given an array of distinct integers arr,
    find all pairs of elements with the 
    minimum absolute difference of any two elements.

    Return a list of pairs in ascending 
    order(with respect to pairs),
    each pair [a, b] follows

    a, b are from arr
    a < b
    b - a equals to the minimum absolute difference of any two elements in arr
"""

arr = [4,2,1,3]
# Expected Output: [[1,2],[2,3],[3,4]]
# arr = [1,3,6,10,15]
# Expected Output: [[1,3]]

# 01 = [4, 2]
# 12 = [2, 1]
# 23 = [1, 3]
# 12 = [2, 1]
# 23 = [1, 3]

# 42 = 01
# 41 = 02
# 43 = 03

# 21 = 12
# 23 = 13

# 13 = 23

# Explanation: The minimum absolute difference is 1.
#              List all pairs with difference equal to 1 in ascending order.

def minimumAbsDifference(arr):
    # 1. Sort the array first so adjacent elements are closest
    arr.sort()
    # print(arr)

    min_diff = float("inf")
    res = []

    # 2. Find the minimum difference in a single pass
    for i in range(len(arr) - 1):
        diff = arr[i + 1] - arr[i]
        if diff < min_diff:
            min_diff = diff
            res = [[arr[i], arr[i + 1]]]  # Reset list if we found a smaller diff
        elif diff == min_diff:
            res.append([arr[i], arr[i + 1]])  # Append if it matches the current min

    return res


# def minimumAbsDifference(arr):
#     """
#     :type arr: List[int]
#     :rtype: List[List[int]]
#     """

#     distinct_int_dict = {}
#     ret_list = []
#     min_abs_diff = float("inf")
#     counter = 1

#     # we need to check every combo to find the lowest difference
#     for i in range(len(arr)):
#         j = i + 1
#         for j in range(len(arr)):
#             val = abs(arr[i] - arr[j])

#             # 1. Sort the pair so [3, 4] and [4, 3] create the exact same key string
#             pair = sorted([arr[i], arr[j]])
#             key = f"{pair[0]} - {pair[1]}"

#             # 2. Add your check to the if statement
#             if i != j and val <= min_abs_diff and key not in distinct_int_dict:
#                 counter += 1
#                 min_abs_diff = val
#                 distinct_int_dict[key] = val

#     for val in distinct_int_dict:
#         num1, num2 = map(int, val.split(" - "))
#         if abs(num1 - num2) <= min_abs_diff:
#             ret_list.append(sorted([num1, num2]))   

#     return sorted(ret_list)
                


print(minimumAbsDifference(arr))