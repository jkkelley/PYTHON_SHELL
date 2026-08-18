"""
    Given an integer array 'nums',
    find the subarray with the largest sum,
    and returns its sum
"""

# nums = [-2,1,-3,4,-1,2,1,-5,4]
# Expected Output: 6
# Explaination: The subarray [4,-1,2,1] has the larget sum 6.

# nums = [1]
# Expected Output: 1
# Explaination: The subarr [1] has the largest sum 1.

nums = [5,4,-1,7,8]
# Expected Output: 23
# Explaination: The subarr [5,4,-1,7,8] has the largest sum 23.


# This is a sliding window probelm
def maxSubArray(nums):
    """
    Time Complexity: O(n)
    - A single linear scan through the array of length n.

    Space Complexity: O(1)
    - Only constant extra space is used for 
      tracking variables (max_so_far, current_sum).
    """

    # 1. Init tracking vars w/ the first ele
    max_so_far = nums[0]
    current_sum = nums[0]

    # 2. Iterate thru the rest of the arr
    for num in range(1, len(nums)):
        # Decide to extend the curr subarr
        # or start fresh from 'num'
        current_sum = max(nums[num], current_sum + nums[num])

        # Update the best overall sum seen so far
        max_so_far = max(max_so_far, current_sum)

    # 3. Ret the max subarr sum found
    return max_so_far

print(maxSubArray(nums=nums))

