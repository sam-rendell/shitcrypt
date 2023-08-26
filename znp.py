import random

# Parameters
p = 23  # Prime number
g = 5   # Primitive root modulo p
x = 3   # Secret value
y = pow(g, x, p)  # Public value

def schnorr_protocol():
    print("Schnorr Zero-Knowledge Proof Demonstration\n")
    print(f"Public parameters: p={p}, g={g}, y={y}\n")

    # Prover (Alice) wants to prove she knows x without revealing it.
    # Step 1: Alice selects a random value v and computes t = g^v mod p
    v = random.randint(1, p-2)
    t = pow(g, v, p)
    print(f"Alice selects random v={v} and sends t={t} to Bob.\n")

    # Step 2: Bob (Verifier) selects a random challenge c and sends it to Alice.
    c = random.randint(1, p-2)
    print(f"Bob selects random challenge c={c} and sends it to Alice.\n")

    # Step 3: Alice computes the response r = v - c*x mod (p-1)
    r = (v - c*x) % (p-1)
    print(f"Alice computes response r={r} and sends it to Bob.\n")

    # Step 4: Bob verifies the proof by checking g^r * y^c mod p == t
    if pow(g, r, p) * pow(y, c, p) % p == t:
        print("Bob verifies the proof using the equation g^r * y^c mod p == t.")
        print("The proof is valid!")
    else:
        print("The proof is invalid!")

schnorr_protocol()
