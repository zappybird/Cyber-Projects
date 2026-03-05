import hashlib
from hashing import hash_functions

def dictionary_attack(target_hash: str, algorithm: str, wordlist_path: str, salt: str = ""):

 
    try:
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as file:
            for line in file:
                word = line.strip()
                # Hash the word with the specified algorithm and salt
                hashed_password = hashlib.new(algorithm, (word + salt).encode()).hexdigest()

                #compare the hashed password with the target hash
                if hashed_password == target_hash:
                    return word  # Match found
                    print(f"Match found: {word}")
                    break
            else: 
                print("No match found in the wordlist.")
    except FileNotFoundError:
        print(f"Wordlist file not found: {wordlist_path}")

    # TODO: iterate through each word
    # TODO: hash + compare

    # TODO: return match or None
    pass
