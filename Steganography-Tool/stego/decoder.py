import lsb
import crypto
from exceptions import StegoError, DecryptionError
from image_utils import load_image


def decode_message(image, password=None):
    #Step 1: Extract the first 32 bits to get message length

    img = load_image(image)

    #Step 1 and 2: extract the first 32 bits to get message length
    length_bits = int(length_bits, 2)
    message_length = int.from_bytes(length_bits, byteorder='big')

    #Step 3: extract message_length * 8 bits to get the message
    max_capacity = img.width * img.height * 3
    if message_length <= 0 or message_length * 8 > max_capacity:
        raise StegoError("No hidden message found or message length is invalid.")
    
    #Step 4: convert bits to bytes, then decode to string
    all_bits = lsb.extract_bits(img, 32 + message_length * 8)
    message_bits = all_bits[32:]

    #Step 5: convert bits to bytes
    try:
        bytelist = [int(message_bits[i:i+8], 2) for i in range(0, len(message_bits), 8)]
        extracted_message = bytes(bytelist)

        if password:
            try: 
                decrypted_data = crypto.decrypt_message(extracted_message, password)
                return decrypted_data.decode('utf-8')
            except Exception as e:
                raise DecryptionError(f"Decryption failed: {str(e)}")
            
        return extracted_message.decode('utf-8')
    
    except UnicodeDecodeError:
        raise StegoError("Failed to decode the hidden message. It may be corrupted or not a valid UTF-8 string.")