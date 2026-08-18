"""
    You are climbing a staircase.
    It takes n steps to reach the top.

    Each time you can either climb 1 or 2 steps.
    In how many distinct ways can you climb to the top?
"""


how_many_stairs = 8
# Expected Output: 2

# Explanation: There are two ways to climb to the top.
# 1. 1 step + 1 step + 1 step
# 2. 1 step + 1 step
# 3. 2 steps + 1 step

# def climbStairs(how_many_stairs):
#     """
#         Time Complexity: O(n)
#         Why: The loop runs from 3 up to n (n - 2 iterations). Each dictionary
#         lookup and addition executes in O(1) constant time.

#         Space Complexity: O(n)
#         Why: The 'combos' dictionary stores n key-value pairs in memory to
#         hold intermediate results.
#     """
#     combos = {1:1, 2:2}

#     for i in range(3, how_many_stairs + 1):
#          combos[i] = combos[i - 1]  + combos[i - 2]

#     return combos[how_many_stairs]
        
def climbStairs(n):
    """
        Time Complexity: O(n)
        Why: The loop executes exactly n times, performing only basic
        arithmetic and variable reassignments in O(1) time per iteration.

        Space Complexity: O(1)
        Why: Only a fixed set of scalar variables (a, b, c) are used,
        requiring constant auxiliary space regardless of the size of n.
    """

    a = 1
    b = 1

    for i in range(n):
        c = a + b
        a = b
        b = c
    
    return a




print(climbStairs(n=how_many_stairs))