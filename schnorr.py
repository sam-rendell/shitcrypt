import random

# Parameters
p = 23  # Prime number
g = 5   # Primitive root modulo p

# Two parties: Alice and Bob
x_alice = 3   # Alice's secret value
y_alice = pow(g, x_alice, p)  # Alice's public value

x_bob = 6   # Bob's secret value
y_bob = pow(g, x_bob, p)  # Bob's public value

def multi_party_schnorr():
    print("Multi-Party Schnorr Identification\n")
    print(f"Public parameters: p={p}, g={g}, y_alice={y_alice}, y_bob={y_bob}\n")

    # Both parties select random values and compute commitments
    v_alice = random.randint(1, p-2)
    t_alice = pow(g, v_alice, p)

    v_bob = random.randint(1, p-2)
    t_bob = pow(g, v_bob, p)

    print(f"Alice's commitment t_alice={t_alice}")
    print(f"Bob's commitment t_bob={t_bob}\n")

    # Both parties exchange commitments and compute combined commitment
    t_combined = (t_alice * t_bob) % p
    print(f"Combined commitment t_combined={t_combined}\n")

    # Both parties select challenges
    c_alice = random.randint(1, p-2)
    c_bob = random.randint(1, p-2)

    # Both parties compute responses
    r_alice = (v_alice - c_alice * x_alice) % (p-1)
    r_bob = (v_bob - c_bob * x_bob) % (p-1)

    print(f"Alice's response r_alice={r_alice}")
    print(f"Bob's response r_bob={r_bob}\n")

    # Verification
    if pow(g, r_alice, p) * pow(y_alice, c_alice, p) % p == t_alice and pow(g, r_bob, p) * pow(y_bob, c_bob, p) % p == t_bob:
        print("Both proofs are valid!")
    else:
        print("One or both proofs are invalid!")

multi_party_schnorr()
