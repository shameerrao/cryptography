import secrets
import sys
import math

def sieve(limit):
    """Generate a list of primes up to 'limit' using the Sieve of Eratosthenes."""
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False  # 0 and 1 are not prime
    primes = []

    for num in range(2, limit + 1):
        if is_prime[num]:
            primes.append(num)
            for multiple in range(num * num, limit + 1, num):
                is_prime[multiple] = False
    return primes

# Precompute small primes up to 10,000 for fast divisibility testing
SMALL_PRIMES = sieve(10_000)

def is_prime(n, k=5):
    """Perform the Miller-Rabin primality test with quick small-prime filtering."""
    if n < 2 or any(n % p == 0 for p in SMALL_PRIMES if p < n):
        return False
    if n in SMALL_PRIMES:
        return True

    # Miller-Rabin test
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1

    for _ in range(k):
        a = secrets.randbelow(n - 3) + 2  # Pick a in range [2, n-2]
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def find_prime(min_val, max_val):
    """Find a prime number efficiently using small-prime filtering and Miller-Rabin."""
    for _ in range(10_000):  # Limit search attempts
        p = secrets.randbelow(max_val - min_val) + min_val
        if p % 2 == 0:
            p += 1  # Ensure p is odd
        if is_prime(p):
            return p
    raise TimeoutError("Failed to find a prime in range")

if __name__ == "__main__":
    verbose = "-v" in sys.argv

    # Step 1: Find a large prime
    if verbose: print("Finding a large prime 'p':")
    p = find_prime(100_000, 5_000_000)
    print(f"[PUBLIC]             p = {p}")

    # Step 2: Choose a generator x
    x = secrets.randbelow(p - 2) + 2
    print(f"[PUBLIC]             x = {x}")

    # Step 3: Generate private keys for A and B
    a = secrets.randbelow(p - 3) + 1
    b = secrets.randbelow(p - 3) + 1
    print(f"[SECRET A]           a = {a}")
    print(f"[SECRET B]           b = {b}")

    # Step 4: Compute public values
    alpha = pow(x, a, p)
    beta = pow(x, b, p)
    print(f"[PUBLIC] A -> B:     x^a mod p = {alpha}")
    print(f"[PUBLIC] B -> A:     x^b mod p = {beta}")

    # Step 5: Compute shared keys
    kab = pow(beta, a, p)
    kba = pow(alpha, b, p)
    print(f"[SECRET A,B]         Kab = {kab}")
    print(f"[SECRET A,B]         Kba = {kba}")

    assert kab == kba, "Shared keys do not match!"