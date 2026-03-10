import itertools
from hashing import hash_functions

def bruteforce_attack(target_hash: str, algorithm: str, charset: str, max_length: int, salt: str = ""):

    
    for length in range(1, max_length + 1):
        for combination in itertools.product(charset, repeat=length):
            guess = "".join(combination)
            if salt:
                guess = salt + guess
            if hash_functions[algorithm](guess) == target_hash:
                return guess
    return None
