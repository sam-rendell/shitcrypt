import random

class ShamirSecretSharing:
    def __init__(self, p):
        self.p = p  # A large prime number

    def _polynomial(self, x, coeffs):
        """Evaluate polynomial with coefficients 'coeffs' at point 'x'."""
        return sum([coeff * (x**i) for i, coeff in enumerate(coeffs)]) % self.p

    def share_secret(self, secret_str, k, n):
        """Split the secret string into n shares."""
        secret = int.from_bytes(secret_str.encode(), 'big')
        print(f"Converted secret string '{secret_str}' to integer: {secret}")

        coeffs = [secret] + [random.randint(0, self.p - 1) for _ in range(k - 1)]
        print(f"Generated polynomial coefficients: {coeffs}")

        shares = []
        for i in range(1, n + 1):
            shares.append((i, self._polynomial(i, coeffs)))
            print(f"Share {i}: ({i}, {shares[-1][1]})")

        return shares

    def reconstruct_secret(self, shares):
        """Reconstruct the secret string from k shares."""
        k = len(shares)
        secret = 0

        for i in range(k):
            xi, yi = shares[i]

            li = 1
            for j in range(k):
                if i != j:
                    xj, _ = shares[j]
                    li *= (xj * pow(xj - xi, -1, self.p)) % self.p
                    print(f"Computing Lagrange basis polynomial for share {i + 1}: li *= (x{j + 1} / (x{j + 1} - x{i + 1})) mod p")

            secret += (yi * li) % self.p
            print(f"Adding to secret: y{i + 1} * li")

        secret_str = (secret % self.p).to_bytes((secret.bit_length() + 7) // 8, 'big').decode()
        return secret_str


# Example usage
p = 2**521 - 1  # A large prime for demonstration purposes
sss = ShamirSecretSharing(p)

secret_str = "Hello, Shamir!"  # The secret string we want to share
print(f"Original Secret String: '{secret_str}'\n")

k = 3  # Minimum number of shares needed to reconstruct the secret
n = 5  # Total number of shares

shares = sss.share_secret(secret_str, k, n)
print("\nGenerated Shares:")
for share in shares:
    print(share)

print("\nReconstructing the secret using 3 shares:")
reconstructed_secret_str = sss.reconstruct_secret(shares[:3])
print(f"Reconstructed Secret String: '{reconstructed_secret_str}'")
