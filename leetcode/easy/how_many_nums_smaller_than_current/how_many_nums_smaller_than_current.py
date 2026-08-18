"""
    Given the array nums,
    for each nums[i] find out how many numbers in the array are smaller than it.

    That is, for each nums[i] you have to count the number of valid j's,
    such that j != i and nums[j] < nums[i].

    Return the answer in an array.
"""

nums = [8,1,2,2,3]


def smallerNumbersThanCurrent(nums):

    sorted_arr = sorted(nums)
    print(sorted_arr)
    d = {}

    for idx, num in enumerate(sorted_arr):
        if num not in d:
            d[num] = idx

    ret_arr = []

    for i in nums:
        # print(f"\n{d[i]}")
        ret_arr.append(d[i])

    return ret_arr

result = smallerNumbersThanCurrent(nums)
print(result)

### Notes
# Time Complexity > Space: First practice interview: Space is cheap




def smallerNumbersThanCurrent_v2(nums):
    """
        Time Complexity:  O(N) - Loops through nums linearly; the n-size + 2 loop is constant O(1).
        Space Complexity: O(1) - Uses a fixed-size count array of n+2 elements regardless of input size.
    """ 
    print(max(nums))

    # Find the biggest number dynamically
    max_val = max(nums) if nums else 0

    # Make just enough boxes (+2 to be safe for indexing)
    count = [0] * (max_val + 2)

    # Count how many time each num appears
    for num in nums:
        # print(f"num + 1: {num + 1}")
        count[num + 1] += 1
        # print(f"incremented num + 1: {count}")
    print(count)

    # Add up the running totals (Cumulative Sum)    
    for i in range(1, len(count)):
        count[i] += count[i - 1]

    # For each num, we check its matching toy box
    # This gathers the final answer
    # Builds new list of answer to give back
    return [count[num] for num in nums]

result = smallerNumbersThanCurrent_v2(nums)
print(result)