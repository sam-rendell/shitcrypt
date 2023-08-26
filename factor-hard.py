import time
import random

def is_prime(n):
    """Check if a number is prime."""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def generate_large_prime(size):
    """Generate a prime number of a given size."""
    while True:
        number = random.getrandbits(size)
        if is_prime(number):
            return number

def naive_factorization(n):
    """Naive factorization approach."""
    for i in range(2, n):
        if n % i == 0:
            return i
    return None

# Generate two large primes
p = generate_large_prime(16)  # 16 bits for demonstration purposes
q = generate_large_prime(16)

# Compute their product
composite = p * q

print(f"Prime p: {p}")
print(f"Prime q: {q}")
print(f"Composite number (p * q): {composite}")

# Attempt to factor the composite number using a naive approach
start_time = time.time()
factor = naive_factorization(composite)
end_time = time.time()

if factor:
    print(f"Found a factor using naive approach: {factor}")
else:
    print("Couldn't factor the composite number using the naive approach.")
print(f"Time taken for naive factorization: {end_time - start_time:.4f} seconds")
