# contains_duplicate.py

# Given an integer array nums,
# return true if any value appears more than once in the array,
# otherwise return false.

# Constraints:
# 
#  0 <= nums.length <= 10^5
#  -10^9 <= nums[i] <= 10^9


input_nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]


### Brute force

def has_duplicate(value):
    for i in range(len(value)):
        for j in range(i + 1, len(value)):
            if value[i] == value[j]:
                return True

    return False

print("Any duplicates? ", has_duplicate(input_nums))

### Time Complexity:    O(n2)
### Space Complexity:   O(1)

"""
    1. Create an empty list (it can also be a dictionary or a set).
    2. Create a hash function.
    3. Inserting an element using a hash function.
    4. Looking up an element using a hash function.
    5. Handling collisions.
"""

# 1. Create an empty list (it can also be a dictionary or a set).
# data structure designed to be fast to work with
array_hash_table = {}

# 2. Create a hash function
def hash_function(input_nums):
    if len(set(input_nums)) == len(input_nums):
        return False
    else:
        return True

print("Any duplicates hash function? ", hash_function(input_nums))
