"""
    You are given an array of integers nums and an integer target, 
    return indices of the two numbers such that they add up to target.

    You may assume that each input would have exactly one solution, 
    and you may not use the same element twice.

    You can return the answer in any order.
"""

from typing import Any


nums: [int] = [2,7,11,15,77,66,74,23,4,98,45]
target: int = 78

def twoSum(nums: [int], target: int) -> tuple[int, int]:
    """
        TIME COMPLEXITY: O(n) - We loop through the list of 'n' items just 
        once. Dictionary lookups and insertions happen in O(1) instant time.
        
        SPACE COMPLEXITY: O(n) - In the worst case, we store all 'n' elements 
        of the list inside our dictionary (nums_dict).
    """

    nums_dict: {int, int} = {}

    for key, val in enumerate(nums):
        if target - val not in nums_dict:
            nums_dict[val] = key
        else:
            return [nums_dict[target - val], key]
        print(f"\n{nums_dict}\n")
    return []


result = twoSum(nums, target)
print(result)

"""
{2: 0}


{2: 0, 7: 1}


{2: 0, 7: 1, 11: 2}


{2: 0, 7: 1, 11: 2, 15: 3}


{2: 0, 7: 1, 11: 2, 15: 3, 77: 4}


{2: 0, 7: 1, 11: 2, 15: 3, 77: 4, 66: 5}


{2: 0, 7: 1, 11: 2, 15: 3, 77: 4, 66: 5, 74: 6}


{2: 0, 7: 1, 11: 2, 15: 3, 77: 4, 66: 5, 74: 6, 23: 7}

[6, 8]
"""