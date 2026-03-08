import argparse
from utils.charset import get_charset

def parse_arguments():
    # Use argparse to get:
    # --hash
    # --algorithm
    # --wordlist
    # --mode (dictionary/bruteforce)
    # --charset
    # --max-length
    # --salt

    parser = argparse.ArgumentParser(description="Hash cracking tool")
    parser.add_argument("--hash", required=True, help="The hash to crack")
    parser.add_argument("--algorithm", required=True, choices=["md5", "sha1", "sha256"], help="Hashing algorithm")
    parser.add_argument("--mode", required=True, choices=["dictionary", "bruteforce"], help="Attack mode")
    parser.add_argument("--wordlist", help="Path to the wordlist for dictionary attack")
    parser.add_argument("--charset", help="Character set for brute-force attack")
    parser.add_argument("--max-length", type=int, help="Maximum password length for brute-force attack")
    parser.add_argument("--salt", default="", help="Salt value to use in hashing")
    return parser.parse_args()

def main():
    args = parse_arguments()

    # If/Elif/Else Structure
    if args.mode == "dictionary":
        if not args.wordlist:
            print("Wordlist is required for dictionary attack")
            return
        from attacks.dictionary import dictionary_attack
        result = dictionary_attack(args.hash, args.algorithm, args.wordlist, args.salt)

    elif args.mode == "bruteforce":
        from attacks.bruteforce import bruteforce_attack
        charset = get_charset(args.charset)  # converts "lower"/"digits"/etc to actual characters
        result = bruteforce_attack(args.hash, args.algorithm, charset, args.max_length, args.salt)
    
    else:
        print("Invalid mode selected")
        return

    if result:
        print(f"Password found: {result}")
    else:
        print("Password not found")

if __name__ == "__main__":
    main()
