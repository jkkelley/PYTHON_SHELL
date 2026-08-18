import math

# Function A: Optimized trial division up to sqrt(n)
def is_prime_a(n):
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

# Function B: Array-based factor filtering
def is_prime_b(n):
    if n < 2:
        return False
    factors = list(range(2, n))
    # Iterate over a copy of the list to safely remove elements
    for i in list(factors):
        if n % i != 0:
            factors.remove(i)
    if len(factors) > 0:  # equivalent to "if factors is not empty"
        return False
    return True

# Function C: Full iteration from 1 to n
def is_prime_c(n):
    if n < 2:
        return False
    for i in range(1, n + 1):
        if i != 1 and i != n and n % i == 0:
            return False
    return True

# List of the first 25 prime numbers
FIRST_25_PRIMES = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
    31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
    73, 79, 83, 89, 97
]

if __name__ == "__main__":
    print("=" * 60)
    print(f"First 25 Prime Numbers:\n{FIRST_25_PRIMES}")
    print("=" * 60)
    print(f"{'Number':<8} | {'Expected':<10} | {'Func A':<8} | {'Func B':<8} | {'Func C':<8}")
    print("-" * 60)
    
    # Test numbers from 1 up to 100
    for num in range(1, 101):
        expected = num in FIRST_25_PRIMES
        res_a = is_prime_a(num)
        res_b = is_prime_b(num)
        res_c = is_prime_c(num)
        
        # Print results for all numbers, highlighting primes or mismatches
        print(f"{num:<8} | {str(expected):<10} | {str(res_a):<8} | {str(res_b):<8} | {str(res_c):<8}")