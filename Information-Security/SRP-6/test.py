import hashlib

def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a%b)


def findPrimitiveRoot(modulus):
    required_set = set(num for num in range (1, modulus) if gcd(num, modulus) == 1)
    for g in range(1, modulus):
        actual_set = set(pow(g, powers) % modulus for powers in range (1, modulus))
        if required_set == actual_set:
            return g


print(hashlib.sha256(b"qwerty123"))
print(int(hashlib.sha256(b"qwerty123").hexdigest(), 16))