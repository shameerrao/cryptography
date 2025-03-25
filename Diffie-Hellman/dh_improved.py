import secrets
import sys
import math

def is_prime(n, k=5):
    """Perform the Miller-Rabin primality test k times."""
    if n < 2 or n % 2 == 0:
        return False
    if n in (2, 3, 5, 7, 11, 13, 17, 19, 23):
        return True
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for _ in range(k):
        a = secrets.randbelow(n - 3) + 2  # Pick a in range [2, n-2]
        x = pow(a, d, n)  # Modular exponentiation
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
    """Find a random prime between min_val and max_val."""
    for _ in range(10000):  # Limit search attempts
        p = secrets.randbelow(max_val - min_val) + min_val
        if p % 2 == 0:
            p += 1  # Make it odd
        if is_prime(p):
            return p
    raise TimeoutError("Failed to find a prime in range")

if __name__ == "__main__":
    verbose = "-v" in sys.argv

    # Step 1: Find a large prime
    if verbose: print("Finding a large prime 'p':")
    p = find_prime(100000, 5000000)
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