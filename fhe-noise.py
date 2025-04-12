import numpy as np
import matplotlib.pyplot as plt

plaintext_modulus = 23  # The modulus for our plaintext space
initial_noise_range = (-3, 3)  # Force non-zero noise values
noise_threshold = 10    # Maximum noise for successful decryption

# Encrypt a message by adding specific noise 
def encrypt(message, noise):
    ciphertext = (message + noise) % plaintext_modulus
    return ciphertext, noise

# Decrypt a ciphertext by removing noise
def decrypt(ciphertext, noise):
    if abs(noise) > noise_threshold:
        return None, False  # Decryption fails due to excessive noise
    message = (ciphertext - noise) % plaintext_modulus
    return message, True

# Homomorphic addition
def add(cipher1, noise1, cipher2, noise2):
    new_cipher = (cipher1 + cipher2) % plaintext_modulus
    new_noise = noise1 + noise2  # Noise adds linearly
    return new_cipher, new_noise

# Homomorphic multiplication
def multiply(cipher1, noise1, cipher2, noise2):
    new_cipher = (cipher1 * cipher2) % plaintext_modulus

    new_noise = noise1 * noise2 * 2  # Ensure non-zero growth
    if new_noise == 0:  # Prevent zero noise after multiplication
        new_noise = max(abs(noise1), abs(noise2)) + 1

    return new_cipher, new_noise

def main():
    m1 = 5
    m2 = 7

    # Encrypt messages with specific noise for demonstration
    n1 = 2  # Force non-zero noise
    n2 = 3  # Force non-zero noise
    c1, n1 = encrypt(m1, n1)
    c2, n2 = encrypt(m2, n2)

    print(f"Message 1: {m1}, Encrypted: {c1}, Noise: {n1}")
    print(f"Message 2: {m2}, Encrypted: {c2}, Noise: {n2}")

    # Track operations and noise
    operations = ["Initial"]
    noise_levels = [max(abs(n1), abs(n2))]

    # Perform addition
    add_cipher, add_noise = add(c1, n1, c2, n2)
    operations.append("Addition")
    noise_levels.append(abs(add_noise))

    # Decrypt addition result
    add_result, add_success = decrypt(add_cipher, add_noise)
    print(f"\nAddition result: {add_cipher}, Noise: {add_noise}")
    print(f"Decryption {'successful' if add_success else 'failed'}: {add_result}")
    print(f"Expected result: {(m1 + m2) % plaintext_modulus}")

    # Perform multiplication
    mult_cipher, mult_noise = multiply(c1, n1, c2, n2)
    operations.append("Multiplication")
    noise_levels.append(abs(mult_noise))

    # Decrypt multiplication result
    mult_result, mult_success = decrypt(mult_cipher, mult_noise)
    print(f"\nMultiplication result: {mult_cipher}, Noise: {mult_noise}")
    print(f"Decryption {'successful' if mult_success else 'failed'}: {mult_result}")
    print(f"Expected result: {(m1 * m2) % plaintext_modulus}")

    # Chain of multiplications to demonstrate noise explosion
    current_cipher, current_noise = c1, n1

    for i in range(1, 5):
        current_cipher, current_noise = multiply(current_cipher, current_noise, c1, n1)
        operations.append(f"Mult Chain {i+1}")
        noise_levels.append(abs(current_noise))

        decrypted, success = decrypt(current_cipher, current_noise)
        print(f"\nAfter {i+1} multiplications: Cipher: {current_cipher}, Noise: {current_noise}")
        print(f"Decryption {'successful' if success else 'failed'}: {decrypted}")
        print(f"Expected result: {(m1 ** (i+1)) % plaintext_modulus}")

    # viz noise growth and save to file instead of showing
    plt.figure(figsize=(10, 6))
    plt.bar(operations, noise_levels, color='skyblue')
    plt.axhline(y=noise_threshold, color='r', linestyle='--', label='Decryption Threshold')
    plt.xlabel('Operations')
    plt.ylabel('Absolute Noise Level')
    plt.title('Noise Growth in FHE Operations')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()

    plt.savefig('fhe_noise_growth.png')
    print("\nNoise growth visualization saved to 'fhe_noise_growth.png'")

    print("\nNoise levels by operation:")
    for op, noise in zip(operations, noise_levels):
        print(f"{op}: {'#' * int(noise)} {noise}")

if __name__ == "__main__":
    main()
