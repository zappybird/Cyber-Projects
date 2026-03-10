from hashing import hash_functions

def dictionary_attack(target_hash: str, algorithm: str, wordlist_path: str, salt: str = ""):
    import os
    base_dir = os.path.dirname(os.path.abspath(__file__))
    wordlist_path = os.path.join(base_dir, wordlist_path)
    
    try:
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as file:
            for line in file:
                word = line.strip()
                # Hash the word with the specified algorithm and salt
                hashed_password = hash_functions[algorithm](word + salt)

                #compare the hashed password with the target hash
                if hashed_password == target_hash:
                    print(f"Match found: {word}")
                    return word  # Return the matching password
                
            print("No match found in the wordlist.")
            return None 
    except FileNotFoundError:
        print(f"Wordlist file not found: {wordlist_path}")

    except Exception as e:
        print(f"An error occurred: {e}")