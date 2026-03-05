
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
    hash_object = hashlib.sha256(encoded_data)

    #return the hexadecimal representation of the hash
    return hash_object.hexdigest()

def verify_hash(guess: str, target_hash: str, algorithm: str, salt: str = "") -> bool: 
    #checks if a guess matches a known hash with salt

    # Combine guess with salt
    salted_guess = guess + salt

    if algorithm.lower() == 'md5':             #Routes to the correct hashing function based on the algorithm name.
        guess_hash = hash_md5(salted_guess)    
    elif algorithm.lower() == 'sha1':          #Routes to the correct hashing function based on the algorithm name.
        guess_hash = hash_sha1(salted_guess)
    elif algorithm.lower() == 'sha256':        #Routes to the correct hashing function based on the algorithm name.
        guess_hash = hash_sha256(salted_guess)
    else:
        raise ValueError("Unsupported hashing algorithm")
    return guess_hash == target_hash


algorithm = ["md5", "sha1", "sha256"]

hash_functions = {
    "md5": hash_md5,
    "sha1": hash_sha1,
    "sha256": hash_sha256
}

for algo in algorithm:
    