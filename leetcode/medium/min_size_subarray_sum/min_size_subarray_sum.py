"""
    Given an array of positive integers nums
    and a positive integer target,
    return the minimal length of a whose sum
    is greater than or equal to target. 

    If there is no such subarray,
    return 0 instead.
"""

from pdb import run
from signal import valid_signals


# target = 7
# nums = [2,4,1,2,4,3]
# Expected Output: 2
# Explanation: The subarray [4,3] has the minimal length under the problem constraint.

target = 4
nums = [1,4,4]

# target = 11
# nums = [1,1,1,1,1,1,1,1]

def minSubArrayLen(target, nums):
    """
    :type target: int
    :type nums: List[int]
    :rtype: int
    """

    if len(nums) < 1:
        return 0

    # Pure Python frequency map
    freq_map = {}


    for num in nums:
        # Check if num in dict
        # If not, default to 0 then add 1
        freq_map[num] = freq_map.get(num, 0) + 1

    sorted_dict = sorted(freq_map.items(), key=lambda x: x[0], reverse=True)

    
    running_total = 0
    min_len = 0

    # print(sorted_dict)
    for num in sorted_dict:
        curr_num_count = num[1]
        curr_num = num[0]

        if curr_num == target:
            return 1

        while curr_num_count > 0 and running_total < target:

            min_len += 1
            running_total += curr_num
            curr_num_count -= 1


    
    if running_total < target:
        return 0

    return min_len


print(minSubArrayLen(target=target, nums=nums))