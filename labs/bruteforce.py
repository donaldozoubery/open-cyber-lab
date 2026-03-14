"""
Brute Force Attack Lab

Learn about brute force attacks and account lockout mechanisms.

This lab demonstrates how attackers use automated tools to
guess passwords and how to protect against such attacks.

DISCLAIMER: This lab is for educational purposes only.
Never attempt brute force attacks without authorization.
"""

DIFFICULTY = "Beginner"

OBJECTIVES = [
    "Understand what brute force attacks are",
    "Learn how password guessing works",
    "Identify protection mechanisms",
    "Practice creating strong passwords"
]

import time
import hashlib
from typing import Optional


# Simulated user database
USERS = {
    "admin": {"password": "admin123", "locked": False},
    "user": {"password": "password123", "locked": False},
    "guest": {"password": "guest", "locked": False},
}


MAX_ATTEMPTS = 5
LOCKOUT_DURATION = 30  # seconds


def hash_password(password: str) -> str:
    """Hash a password using SHA-256.
    
    Args:
        password: Password to hash
        
    Returns:
        str: Hashed password
    """
    return hashlib.sha256(password.encode()).hexdigest()


def attempt_login_vulnerable(username: str, password: str) -> dict:
    """Attempt login without any protection.
    
    Args:
        username: Username
        password: Password
        
    Returns:
        dict: Login result
    """
    user = USERS.get(username)
    
    if user is None:
        return {
            "success": False,
            "message": "Invalid username or password",
            "attempts_remaining": MAX_ATTEMPTS,
            "locked": False,
            "protection": "none"
        }
    
    if user["locked"]:
        return {
            "success": False,
            "message": "Account locked",
            "attempts_remaining": 0,
            "locked": True,
            "protection": "none"
        }
    
    if user["password"] == password:
        return {
            "success": True,
            "message": "Login successful!",
            "attempts_remaining": MAX_ATTEMPTS,
            "locked": False,
            "protection": "none"
        }
    
    return {
        "success": False,
        "message": "Invalid username or password",
        "attempts_remaining": MAX_ATTEMPTS - 1,
        "locked": False,
        "protection": "none"
    }


def attempt_login_protected(username: str, password: str, attempt_count: int) -> dict:
    """Attempt login with brute force protection.
    
    Args:
        username: Username
        password: Password
        attempt_count: Number of failed attempts
        
    Returns:
        dict: Login result
    """
    user = USERS.get(username)
    
    if user is None:
        return {
            "success": False,
            "message": "Invalid username or password",
            "attempts_remaining": MAX_ATTEMPTS - attempt_count,
            "locked": False,
            "protection": "lockout"
        }
    
    if attempt_count >= MAX_ATTEMPTS:
        user["locked"] = True
        return {
            "success": False,
            "message": f"Account locked due to too many failed attempts. Try again in {LOCKOUT_DURATION} seconds.",
            "attempts_remaining": 0,
            "locked": True,
            "protection": "lockout"
        }
    
    if user["password"] == password:
        return {
            "success": True,
            "message": "Login successful!",
            "attempts_remaining": MAX_ATTEMPTS,
            "locked": False,
            "protection": "lockout"
        }
    
    return {
        "success": False,
        "message": "Invalid username or password",
        "attempts_remaining": MAX_ATTEMPTS - attempt_count - 1,
        "locked": False,
        "protection": "lockout"
    }


def brute_force_attack(target_username: str, wordlist: list) -> dict:
    """Simulate a brute force attack.
    
    Args:
        target_username: Target username
        wordlist: List of passwords to try
        
    Returns:
        dict: Attack result
    """
    user = USERS.get(target_username)
    
    if user is None:
        return {
            "success": False,
            "password_found": None,
            "attempts": 0,
            "total_wordlist": len(wordlist),
            "message": "User not found"
        }
    
    for i, password in enumerate(wordlist, 1):
        if user["password"] == password:
            return {
                "success": True,
                "password_found": password,
                "attempts": i,
                "total_wordlist": len(wordlist),
                "message": f"Password cracked in {i} attempts!"
            }
    
    return {
        "success": False,
        "password_found": None,
        "attempts": len(wordlist),
        "total_wordlist": len(wordlist),
        "message": "Password not found in wordlist"
    }


def generate_wordlist(size: str = "small") -> list:
    """Generate a wordlist for brute force.
    
    Args:
        size: Wordlist size (small, medium, large)
        
    Returns:
        list: List of passwords
    """
    base = [
        "123", "1234", "12345", "123456", "1234567", "12345678", "123456789",
        "password", "password1", "password12", "password123",
        "admin", "admin123", "administrator",
        "letmein", "welcome", "qwerty", "abc123",
        "test", "test123", "guest", "root"
    ]
    
    if size == "small":
        return base[:10]
    elif size == "medium":
        return base[:15]
    else:
        # Add variations
        variations = []
        for pwd in base:
            variations.append(pwd)
            variations.append(pwd.upper())
            variations.append(pwd + "!")
            variations.append(pwd + "@")
        return list(set(variations))


def validate_solution(password_found: bool) -> dict:
    """Validate the solution.
    
    Args:
        password_found: Whether password was found
        
    Returns:
        dict: Validation result
    """
    if password_found:
        return {
            "success": True,
            "message": "Brute force attack successful! Weak password cracked."
        }
    
    return {
        "success": False,
        "message": "Password not found. Try with more passwords."
    }


def run(*args):
    """Run the Brute Force Lab."""
    print("=" * 50)
    print("       BRUTE FORCE ATTACK LAB")
    print("=" * 50)
    print()
    print("OBJECTIVES:")
    for i, obj in enumerate(OBJECTIVES, 1):
        print(f"  {i}. {obj}")
    print()
    print("-" * 50)
    print()
    
    print("SCENARIO:")
    print("  An attacker is trying to guess a user's password")
    print("  using automated tools.")
    print()
    
    print("-" * 50)
    print()
    
    print("OPTIONS:")
    print("  1. Test vulnerable login (no protection)")
    print("  2. Test protected login (with lockout)")
    print("  3. Run brute force attack simulation")
    print()
    
    choice = input("Choose (1-3): ")
    
    if choice == "1":
        print("\n--- Vulnerable Login ---")
        username = input("Username: ")
        password = input("Password: ")
        print()
        
        result = attempt_login_vulnerable(username, password)
        
        print(f"Result: {result['message']}")
        print(f"Attempts remaining: {result['attempts_remaining']}")
        print(f"Protection: {result['protection']}")
        
        validation = validate_solution(result["success"])
        
    elif choice == "2":
        print("\n--- Protected Login ---")
        username = input("Username: ")
        password = input("Password: ")
        
        attempt_count = int(input("Failed attempts so far (0-5): "))
        print()
        
        result = attempt_login_protected(username, password, attempt_count)
        
        print(f"Result: {result['message']}")
        print(f"Attempts remaining: {result['attempts_remaining']}")
        print(f"Locked: {result['locked']}")
        print(f"Protection: {result['protection']}")
        
        validation = validate_solution(False)
        
    elif choice == "3":
        print("\n--- Brute Force Attack ---")
        
        target = input("Target username (admin/user/guest): ")
        size = input("Wordlist size (small/medium/large): ")
        
        wordlist = generate_wordlist(size)
        print(f"\nWordlist: {len(wordlist)} passwords")
        print("Running attack...")
        time.sleep(1)
        
        result = brute_force_attack(target, wordlist)
        
        print(f"\nResult: {result['message']}")
        if result["password_found"]:
            print(f"Password: {result['password_found']}")
        print(f"Attempts: {result['attempts']}/{result['total_wordlist']}")
        
        validation = validate_solution(result["success"])
        
    else:
        print("Invalid choice.")
        return False
    
    print()
    print("-" * 50)
    print()
    
    if validation["success"]:
        print("=" * 50)
        print("  CONGRATULATIONS!")
        print("=" * 50)
        print()
        print(validation["message"])
        print()
        print("EXPLANATION:")
        print("  Brute force attacks try all possible combinations.")
        print("  They work best against weak passwords.")
        print()
        print("PROTECTION METHODS:")
        print("  - Account lockout after N failed attempts")
        print("  - Rate limiting")
        print("  - CAPTCHA after failed attempts")
        print("  - Two-factor authentication")
        print("  - IP blocking after suspicious activity")
        print("  - Use strong, unique passwords")
    else:
        print("Keep exploring!")
    
    print()
    print("-" * 50)
    print("Lab completed.")
    return True


if __name__ == "__main__":
    run()
