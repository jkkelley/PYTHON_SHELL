"""
    You are given an integer array coins representing
    coins of different denominations and an integer
    amount representing a total amount of money.

    Return the fewest number of coins that you
    need to make up that amount. If that amount
    of money cannot be made up by any combination
    of the coins, return -1.

    You may assume that you have an infinite
    number of each kind of coin.
"""

coins = [1,2,5]
amount = 11

# coins = [2]
# amount = 3

# coins = [1]
# amount = 0

# Expected Output: 3
# Explanation: 11 = 5 + 5 + 1

def coinChange(coins, amount):
    """
    :type coins: List[int]
    :type amount: int
    :rtype: int

    Time Complexity: O(amount * number of coins). For every number up
    to the target amount, we run an inner loop to test every single
    coin in our list to see if it fits. 

    Space Complexity: O(amount). We created a single list (the 'dp'
    array) to store a saved answer for every number up to the target 
    amount.
    """

    dp = [float("inf")] * (amount + 1)
    dp[0] = 0

    for i in range(1, amount + 1):
        for coin in coins:
            # print(i, coin)
            if coin <= i:
                dp[i] = min(dp[i], 1 + dp[i - coin])
        
    # print(dp[-1::])
    if dp[-1::] == [float("inf")]:
        # print("yes")
        return -1

        
    return dp[-1]


print(coinChange(coins=coins, amount=amount))