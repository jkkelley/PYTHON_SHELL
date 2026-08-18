"""
Given an integer array nums,
return all the triplets [nums[i], nums[j], nums[k]]
such that i != j, i != k,and j != k, 
and nums[i] + nums[j] + nums[k] == 0.

Notice that the solution set must not contain duplicate triplets.
"""

nums = [-1,0,1,2,-1,-4]
# Output: [[-1,-1,2],[-1,0,1]]

# nums = [0,1,1]

# Explanation: 
# nums[0] + nums[1] + nums[2] = (-1) + 0 + 1 = 0.
# nums[1] + nums[2] + nums[4] = 0 + 1 + (-1) = 0.
# nums[0] + nums[3] + nums[4] = (-1) + 2 + (-1) = 0.
# The distinct triplets are [-1,0,1] and [-1,-1,2].
# Notice that the order of the output and the order of the triplets does not matter.


def threeSum(nums):
    """
    :type nums: List[int]
    :rtype: List[List[int]]
    """

    ret_list = []

    nums_sorted = sorted(nums)
    print(nums_sorted)
    for i in range(len(nums_sorted) - 2):
        # Skip dupes values for i to avoid dupe triplets
        if i > 0 and nums_sorted[i] == nums_sorted[i - 1]:
            continue

        j = i + 1
        k = len(nums_sorted) - 1
        # We check elements at i, j, k here...

        while j < k:
            current_sum = nums_sorted[i] + nums_sorted[j] + nums_sorted[k]

            if current_sum == 0:
                ret_list.append([nums_sorted[i], nums_sorted[j], nums_sorted[k]])
                j += 1
                k -= 1

                # Skip dupes for j/k avoiding dupe triplets
                while j < k and nums_sorted[j] == nums_sorted[j - 1]:
                    j += 1
                while j < k and nums_sorted[k] == nums_sorted[k  + 1]:
                    k -= 1

            elif current_sum < 0:
                # Sum is too small, move the left pointer forward
                j += 1
            else:
                # Sum is too large, move the right pointer backwards
                k -= 1
    
    return ret_list


print(threeSum(nums))