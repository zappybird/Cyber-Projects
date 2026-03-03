import hashlib

# hashing.py 
def hash_md5(data_string: str) -> str:

    # Encode string to bytes
    encoded_data = data_string.encode('utf-8')

    # Create MD5 hash object
    hash_object = hashlib.md5(encoded_data)

    # Get hexadecimal digest
    return hash_object.hexdigest()



def hash_sha1(data_string: str) -> str: 

    #encode string to bytes
    encoded_data = data_string.encode('utf-8')

    #create SHA1 hash object
    hash_object = hashlib.sha1(encoded_data)

    #return the hexadecimal representation of the hash
    return hash_object.hexdigest()

def hash_sha256(data_string: str) -> str: 

    #encode string to bytes
    encoded_data = data_string.encode('utf-8')

    #create SHA256 hash object
    hash_object = hashlib.sha256()

    #return the hexadecimal representation of the hash
    return hash_object.hexdigest()

def verify_hash(guess: str, target_hash: str, algorithm: str, salt: str = "") -> bool: 
    # TODO: apply salt, hash guess, compare to target pass

    # Combine guess with salt
    salted_guess = guess + salt

    # Hash the salted guess using the specified algorithm
    if algorithm.lower() == 'md5':
        guess_hash = hash_md5(salted_guess)
    elif algorithm.lower() == 'sha1':
        guess_hash = hash_sha1(salted_guess)
    elif algorithm.lower() == 'sha256':
        guess_hash = hash_sha256(salted_guess)
    else:
        raise ValueError("Unsupported hashing algorithm")
    return guess_hash == target_hash



input_str = "yo momma" 
hashed_str = hash_md5(input_str)
hash_sha256_str = hash_sha256(input_str)
hash_sha1_str = hash_sha1(input_str)
print(f"MD5 hash of '{input_str}' is: {hashed_str}")
print(f"SHA1 hash of '{input_str}' is: {hash_sha1_str}")
print(f"SHA256 hash of '{input_str}' is: {hash_sha256_str}")