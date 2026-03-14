"""
Password Cracking Lab

Learn about password security and cracking techniques.

This lab demonstrates dictionary attacks against weak passwords
and teaches the importance of using strong, unique passwords.

DISCLAIMER: This lab is for educational purposes only.
Never attempt to crack passwords without authorization.
"""

DIFFICULTY = "Beginner"

OBJECTIVES = [
    "Understand how dictionary attacks work",
    "Learn about password hashing",
    "Identify weak password patterns",
    "Practice creating strong passwords"
]

# For educational purposes, we use a simple hash
# In production, use proper password hashing libraries like bcrypt
import hashlib


def hash_password(password: str) -> str:
    """Hash a password using SHA-256.
    
    Note: SHA-256 is not recommended for password hashing.
    Use bcrypt or argon2 in production.
    
    Args:
        password: The password to hash
        
    Returns:
        str: The hexadecimal hash
    """
    return hashlib.sha256(password.encode()).hexdigest()


def generate_wordlist(size: str = "small") -> list:
    """Generate a wordlist for the dictionary attack.
    
    Args:
        size: Size of wordlist ('small', 'medium', 'large')
        
    Returns:
        list: List of words to try
    """
    base_words = [
        "admin", "root", "test", "guest", "user",
        "123456", "password", "12345678", "qwerty", "abc123",
        "monkey", "1234567", "letmein", "trustno1", "dragon",
        "baseball", "iloveyou", "master", "sunshine", "ashley",
        "football", "password1", "shadow", "123123", "654321",
        "superman", "qazwsx", "michael", "password123", "welcome"
    ]
    
    if size == "small":
        return base_words[:10]
    elif size == "medium":
        return base_words[:20]
    else:  # large
        # Add common variations
        variations = []
        for word in base_words:
            variations.append(word)
            variations.append(word.upper())
            variations.append(word.capitalize())
            variations.append(word + "123")
            variations.append(word + "!")
        return list(set(variations))


def crack_password(target_hash: str, wordlist: list) -> tuple:
    """Attempt to crack a password using dictionary attack.
    
    Args:
        target_hash: The hash to crack
        wordlist: List of words to try
        
    Returns:
        tuple: (success: bool, password: str or None, attempts: int)
    """
    for i, word in enumerate(wordlist, 1):
        word_hash = hash_password(word)
        if word_hash == target_hash:
            return True, word, i
    
    return False, None, len(wordlist)


def validate_solution(password_found: bool) -> dict:
    """Validate the solution and provide feedback.
    
    Args:
        password_found: Whether the password was successfully cracked
        
    Returns:
        dict: Result with success status and message
    """
    if password_found:
        return {
            "success": True,
            "message": "Password cracked successfully!"
        }
    else:
        return {
            "success": False,
            "message": "Password not found in wordlist. Try a larger wordlist!"
        }


def run(*args):
    """Run the Password Cracking Lab."""
    print("=" * 50)
    print("       PASSWORD CRACKING LAB")
    print("=" * 50)
    print()
    print("OBJECTIVES:")
    for i, obj in enumerate(OBJECTIVES, 1):
        print(f"  {i}. {obj}")
    print()
    print("-" * 50)
    print()
    print("This lab demonstrates a dictionary attack on a hashed password.")
    print("You'll use a wordlist to try to crack the target password.")
    print()
    print("Note: This lab uses SHA-256 for demonstration.")
    print("In production, use bcrypt, argon2, or scrypt for password hashing.")
    print()
    print("-" * 50)
    print()
    
    # Get wordlist size from args or use default
    wordlist_size = args[0] if args else "small"
    wordlist = generate_wordlist(wordlist_size)
    
    # Generate a target password (for demonstration)
    target_password = "password123"
    target_hash = hash_password(target_password)
    
    print(f"Wordlist size: {len(wordlist)} words ({wordlist_size})")
    print(f"Target hash: {target_hash}")
    print()
    print("Starting dictionary attack...")
    print("-" * 50)
    print()
    
    # Attempt to crack the password
    success, found_password, attempts = crack_password(target_hash, wordlist)
    
    print(f"Attempts: {attempts}")
    print()
    
    result = validate_solution(success)
    
    if success:
        print("=" * 50)
        print("  CONGRATULATIONS!")
        print("=" * 50)
        print()
        print(result["message"])
        print(f"  Password found: {found_password}")
        print()
        print("EXPLANATION:")
        print("  Dictionary attacks work by trying common words and patterns.")
        print("  This is why strong, unique passwords are essential.")
        print()
        print("KEY TAKEAWAYS:")
        print("  - Use long passwords (12+ characters)")
        print("  - Mix uppercase, lowercase, numbers, and symbols")
        print("  - Avoid dictionary words and common patterns")
        print("  - Use a password manager")
        print("  - Enable two-factor authentication")
    else:
        print("Keep trying! You can specify a larger wordlist:")
        print("  python cyberlab.py run password_cracking medium")
        print("  python cyberlab.py run password_cracking large")
    
    print()
    print("-" * 50)
    print("Lab completed.")
    return True


if __name__ == "__main__":
    run()
