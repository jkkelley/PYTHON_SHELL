"""
    You may recall that an array `arr` is a mountain array if and only if:

        arr.length >= 3
        There exists some index i (0-indexed) with 0 < i < arr.length - 1 such that:
            arr[0] < arr[1] < ... < arr[i - 1] < arr[i]
            arr[i] > arr[i + 1] > ... > arr[arr.length - 1]

    Given an integer array arr, 
    return the length of the longest subarray, which is a mountain.
    
    Return 0 if there is no mountain subarray.
"""

arr = [2,2,2]
# arr = [2,1,4,7,3,2,5]
# arr = [1,2,3,2,1]
# Output: 5

# Explanation: The largest mountain is [1,4,7,3,2] which has length 5.

def longestMountain(arr):
    if not arr or len(arr) < 3:
        return 0

    len_of_mountain = 0

    for mountain_top in range(1, len(arr) - 1):
        if arr[mountain_top - 1] < arr[mountain_top] and arr[mountain_top] > arr[mountain_top + 1]:
            right = mountain_top
            left = mountain_top

            while left > 0 and arr[left - 1] < arr[left]:
                left -= 1

            while right < len(arr) - 1 and arr[right + 1] < arr[right]:
                right += 1

            # Calculate length and update maximum
            current_len = right - left + 1
            len_of_mountain = max(len_of_mountain, current_len)

    return len_of_mountain


print(longestMountain(arr))