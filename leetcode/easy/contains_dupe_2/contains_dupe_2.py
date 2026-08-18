"""
    Given an integer array nums and an integer k,
    return true if there are two distinct indices i and j
    in the array such that nums[i] == nums[j] and abs(i - j) <= k.
"""

nums = [1,2,3,1,2,3]
k = 2
# nums = [1,2,3,1]
# k = 3
# Expected Output: true

def containsNearbyDuplicate(nums, k):
    """
    :type nums: List[int]
    :type k: int
    :rtype: bool
    
    """

    seen = {} # Stores: { number: index }

    for i, num in enumerate(nums):
        # 1. Check if we've seen this number and if it's within distance k
        if num in seen and i - seen[num] <= k:
            return True
        
        # 2. Update the dictionary with the most recent index for this number
        seen[num] = i

    # 3. No nearby duplicate found after checking all elements
    return False

print(containsNearbyDuplicate(nums, k))