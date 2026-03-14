"""
Cross-Site Request Forgery (CSRF) Lab

Learn about CSRF vulnerabilities and token-based protection.

This lab demonstrates how attackers can trick users into
performing unwanted actions and how CSRF tokens prevent it.

DISCLAIMER: This lab is for educational purposes only.
Always implement CSRF protection in production applications.
"""

DIFFICULTY = "Intermediate"

OBJECTIVES = [
    "Understand what CSRF is",
    "Learn how attackers exploit CSRF vulnerabilities",
    "Understand how CSRF tokens work",
    "Implement token-based protection"
]

import secrets
import hashlib
import time


# Simulated user session
user_session = {
    "user_id": 1,
    "username": "john_doe",
    "logged_in": True
}


def generate_csrf_token() -> str:
    """Generate a secure CSRF token.
    
    Returns:
        str: A random secure token
    """
    return secrets.token_hex(32)


def create_vulnerable_action(action: str) -> dict:
    """Create a vulnerable action without CSRF protection.
    
    Args:
        action: The action to perform
        
    Returns:
        dict: Result showing the vulnerability
    """
    # Vulnerable: No CSRF token validation
    return {
        "success": True,
        "message": f"Action '{action}' performed successfully!",
        "protected": False,
        "token_required": False
    }


def create_protected_action(action: str, token: str, expected_token: str) -> dict:
    """Create a protected action with CSRF validation.
    
    Args:
        action: The action to perform
        token: The token provided by the user
        expected_token: The expected valid token
        
    Returns:
        dict: Result showing protection status
    """
    # Protected: Validate CSRF token
    if token != expected_token:
        return {
            "success": False,
            "message": "CSRF token validation failed!",
            "protected": True,
            "token_required": True
        }
    
    return {
        "success": True,
        "message": f"Action '{action}' performed successfully!",
        "protected": True,
        "token_required": True
    }


def simulate_csrf_attack(attack_url: str) -> dict:
    """Simulate a CSRF attack.
    
    Args:
        attack_url: The malicious URL
        
    Returns:
        dict: Result of the attack
    """
    # Check if attack URL contains a vulnerable action
    vulnerable_actions = ["transfer", "delete", "update", "change_password"]
    
    for action in vulnerable_actions:
        if action in attack_url.lower():
            return {
                "attack_successful": True,
                "message": f"CSRF attack successful! Action '{action}' executed.",
                "impact": "User's account compromised"
            }
    
    return {
        "attack_successful": False,
        "message": "Attack URL doesn't match vulnerable endpoints",
        "impact": "None"
    }


def validate_solution(attack_successful: bool, protected: bool) -> dict:
    """Validate the solution.
    
    Args:
        attack_successful: Whether the attack would work
        protected: Whether protection was used
        
    Returns:
        dict: Result with success status
    """
    if attack_successful and not protected:
        return {
            "success": True,
            "message": "CSRF vulnerability exploited successfully!",
            "explanation": "Without CSRF protection, attackers can trick users into performing actions."
        }
    elif protected:
        return {
            "success": True,
            "message": "CSRF protection working correctly!",
            "explanation": "The token validated successfully, preventing the attack."
        }
    
    return {
        "success": False,
        "message": "Try again to understand the vulnerability."
    }


def run(*args):
    """Run the CSRF Lab."""
    print("=" * 50)
    print("  CROSS-SITE REQUEST FORGERY (CSRF) LAB")
    print("=" * 50)
    print()
    print("OBJECTIVES:")
    for i, obj in enumerate(OBJECTIVES, 1):
        print(f"  {i}. {obj}")
    print()
    print("-" * 50)
    print()
    
    print("SCENARIO:")
    print("  You're logged into your bank account.")
    print("  An attacker sends you a malicious link.")
    print()
    
    # Generate a valid CSRF token
    valid_token = generate_csrf_token()
    
    print(f"Valid CSRF Token: {valid_token[:16]}...")
    print()
    
    print("-" * 50)
    print()
    
    # Menu
    print("OPTIONS:")
    print("  1. Test vulnerable endpoint (no protection)")
    print("  2. Test protected endpoint (with token)")
    print("  3. Simulate CSRF attack")
    print()
    
    choice = input("Choose (1-3): ")
    
    if choice == "1":
        print("\n--- Vulnerable Endpoint ---")
        print("URL: /api/transfer?to=attacker&amount=10000")
        print()
        
        result = create_vulnerable_action("transfer")
        
        print(f"Result: {result['message']}")
        print(f"Protected: {result['protected']}")
        
        validation = validate_solution(attack_successful=True, protected=False)
        
    elif choice == "2":
        print("\n--- Protected Endpoint ---")
        print("URL: /api/transfer?to=attacker&amount=10000")
        
        token_input = input("Enter CSRF token: ")
        print()
        
        result = create_protected_action("transfer", token_input, valid_token)
        
        print(f"Result: {result['message']}")
        print(f"Protected: {result['protected']}")
        
        validation = validate_solution(attack_successful=False, protected=True)
        
    elif choice == "3":
        print("\n--- CSRF Attack Simulation ---")
        
        print("Malicious website contains:")
        print('  <img src="https://bank.com/transfer?to=attacker&amount=10000">')
        print()
        
        attack_url = "https://bank.com/transfer?to=attacker&amount=10000"
        result = simulate_csrf_attack(attack_url)
        
        print(f"Attack Result: {result['message']}")
        print(f"Impact: {result['impact']}")
        
        validation = validate_solution(result['attack_successful'], protected=False)
        
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
        print("  " + validation["explanation"])
        print()
        print("HOW CSRF WORKS:")
        print("  1. User logs into legitimate site")
        print("  2. User visits malicious site")
        print("  3. Malicious site sends requests to legitimate site")
        print("  4. Browser includes user's session cookies")
        print("  5. Legitimate site processes the forged request")
        print()
        print("HOW TO PREVENT:")
        print("  - Use CSRF tokens (synchronizer token pattern)")
        print("  - Implement SameSite cookies")
        print("  - Check Origin/Referer headers")
        print("  - Use double submit cookies")
    else:
        print("Keep trying to understand CSRF!")
    
    print()
    print("-" * 50)
    print("Lab completed.")
    return True


if __name__ == "__main__":
    run()
