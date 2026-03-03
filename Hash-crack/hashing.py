import hashlib

# hashing.py 
def hash_md5(data_string) -> str:
     # TODO: implement MD5 hashing pass 

     # Encode string to bytes
    encoded_data = data_string.encode('utf-8')

    # Create MD5 hash object
    hash_object = hashlib.md5(encoded_data)

    # Get hexadecimal digest
    return hash_object.hexdigest()

"""sumary_line

Keyword arguments:
argument -- description
Return: return_description


def hash_sha1(text: str) -> str: 
    # TODO: implement SHA1 hashing pass 

    def hash_sha256(text: str) -> str: 
    # TODO: implement SHA256 hashing pass 

def verify_hash(guess: str, target_hash: str, algorithm: str, salt: str = "") -> bool: 
    # TODO: apply salt, hash guess, compare to target pass
"""

input_str = "yo momma" 
hashed_str = hash_md5(input_str)
print(f"MD5 hash of '{input_str}' is: {hashed_str}")