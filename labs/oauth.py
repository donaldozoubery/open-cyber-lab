"""
OAuth 2.0 Security Lab

Learn about OAuth 2.0 vulnerabilities and secure implementation.

This lab demonstrates common OAuth security issues
and how to implement secure authentication.

DISCLAIMER: This lab is for educational purposes only.
Never exploit OAuth vulnerabilities without authorization.
"""

DIFFICULTY = "Intermediate"

OBJECTIVES = [
    "Understand OAuth 2.0 flow",
    "Learn about OAuth security vulnerabilities",
    "Identify insecure implementations",
    "Practice secure OAuth implementation"
]

import secrets
import time


# Simulated OAuth configuration
CLIENT_ID = "my_app_12345"
CLIENT_SECRET = "super_secret_client_key"
REDIRECT_URI = "http://localhost:8080/callback"

# Authorization codes
AUTH_CODES = {}

# Access tokens
ACCESS_TOKENS = {}


def generate_auth_code() -> str:
    """Generate a secure authorization code."""
    return secrets.token_urlsafe(32)


def generate_access_token() -> str:
    """Generate a secure access token."""
    return secrets.token_urlsafe(32)


def vulnerable_oauth_flow(authorization_code: str, redirect_uri: str) -> dict:
    """Simulate vulnerable OAuth flow.
    
    Args:
        authorization_code: Authorization code
        redirect_uri: Redirect URI
        
    Returns:
        dict: OAuth flow result
    """
    # Vulnerable: No redirect_uri validation
    
    # Check if code is valid
    if authorization_code not in AUTH_CODES:
        return {
            "success": False,
            "error": "Invalid authorization code",
            "vulnerable": True
        }
    
    # Vulnerable: Not validating redirect_uri matches
    # Attacker could use a different redirect_uri
    
    # Generate access token
    access_token = generate_access_token()
    ACCESS_TOKENS[access_token] = {
        "client_id": AUTH_CODES[authorization_code]["client_id"],
        "user": AUTH_CODES[authorization_code]["user"],
        "expires": time.time() + 3600
    }
    
    return {
        "success": True,
        "access_token": access_token,
        "token_type": "Bearer",
        "expires_in": 3600,
        "vulnerable": True
    }


def secure_oauth_flow(authorization_code: str, redirect_uri: str) -> dict:
    """Simulate secure OAuth flow.
    
    Args:
        authorization_code: Authorization code
        redirect_uri: Redirect URI
        
    Returns:
        dict: OAuth flow result
    """
    # Secure: Validate redirect_uri
    
    if authorization_code not in AUTH_CODES:
        return {
            "success": False,
            "error": "Invalid authorization code",
            "vulnerable": False
        }
    
    # Secure: Validate redirect_uri
    stored_redirect = AUTH_CODES[authorization_code].get("redirect_uri")
    if stored_redirect and redirect_uri != stored_redirect:
        return {
            "success": False,
            "error": "redirect_uri mismatch! Possible CSRF attack.",
            "vulnerable": False
        }
    
    # Generate access token
    access_token = generate_access_token()
    ACCESS_TOKENS[access_token] = {
        "client_id": AUTH_CODES[authorization_code]["client_id"],
        "user": AUTH_CODES[authorization_code]["user"],
        "expires": time.time() + 3600
    }
    
    return {
        "success": True,
        "access_token": access_token,
        "token_type": "Bearer",
        "expires_in": 3600,
        "vulnerable": False
    }


def simulate_authorization(redirect_uri: str = REDIRECT_URI) -> dict:
    """Simulate OAuth authorization step.
    
    Args:
        redirect_uri: Redirect URI
        
    Returns:
        dict: Authorization result
    """
    code = generate_auth_code()
    AUTH_CODES[code] = {
        "client_id": CLIENT_ID,
        "user": "john_doe",
        "redirect_uri": redirect_uri,
        "created": time.time()
    }
    
    return {
        "success": True,
        "authorization_code": code,
        "redirect_uri": f"{redirect_uri}?code={code}"
    }


def validate_solution(vulnerable: bool, success: bool) -> dict:
    """Validate the solution.
    
    Args:
        vulnerable: Whether vulnerable method was used
        success: Whether operation succeeded
        
    Returns:
        dict: Validation result
    """
    if vulnerable and success:
        return {
            "success": True,
            "message": "Vulnerable flow exploited! Token was issued without proper validation."
        }
    elif not vulnerable:
        return {
            "success": True,
            "message": "Secure flow! All validations passed."
        }
    
    return {
        "success": False,
        "message": "Operation failed."
    }


def run(*args):
    """Run the OAuth Security Lab."""
    print("=" * 50)
    print("     OAUTH 2.0 SECURITY LAB")
    print("=" * 50)
    print()
    print("OBJECTIVES:")
    for i, obj in enumerate(OBJECTIVES, 1):
        print(f"  {i}. {obj}")
    print()
    print("-" * 50)
    print()
    
    print("OAUTH 2.0 FLOW:")
    print("  1. User authorizes app")
    print("  2. App receives authorization code")
    print("  3. App exchanges code for access token")
    print("  4. App uses token to access resources")
    print()
    
    print("-" * 50)
    print()
    
    # Start authorization
    result = simulate_authorization()
    print(f"Authorization code: {result['authorization_code'][:20]}...")
    print()
    
    print("OPTIONS:")
    print("  1. Vulnerable token exchange (no redirect_uri)")
    print("  2. Secure token exchange (with redirect_uri)")
    print("  3. Attack simulation")
    print()
    
    choice = input("Choose (1-3): ")
    
    if choice == "1":
        print("\n--- Vulnerable Token Exchange ---")
        print("Vulnerable code:")
        print("  token = get_token(code)  # No redirect_uri check!")
        print()
        
        # Use wrong redirect URI
        code = result["authorization_code"]
        wrong_uri = "http://malicious-site.com/callback"
        
        result = vulnerable_oauth_flow(code, wrong_uri)
        
        if result["success"]:
            print(f"\n✓ Access token: {result['access_token'][:20]}...")
            print("\n⚠️  VULNERABILITY: Token issued without redirect_uri validation!")
        else:
            print(f"\n✗ {result['error']}")
        
        validation = validate_solution(vulnerable=True, success=result["success"])
        
    elif choice == "2":
        print("\n--- Secure Token Exchange ---")
        print("Secure code:")
        print("  if redirect_uri != stored_redirect_uri:")
        print("      raise Error('redirect_uri mismatch')")
        print()
        
        code = result["authorization_code"]
        
        result = secure_oauth_flow(code, REDIRECT_URI)
        
        if result["success"]:
            print(f"\n✓ Access token: {result['access_token'][:20]}...")
            print("\n✓ Secure: redirect_uri was validated!")
        else:
            print(f"\n✗ {result['error']}")
        
        validation = validate_solution(vulnerable=False, success=result["success"])
        
    elif choice == "3":
        print("\n--- Attack Simulation ---")
        print("Attacker scenario:")
        print("  1. Attacker creates malicious app")
        print("  2. User authorizes (with legitimate redirect)")
        print("  3. Attacker intercepts authorization code")
        print("  4. Attacker uses code with malicious redirect")
        print()
        
        # Attack simulation
        attack_uri = "http://attacker.com/steal_token"
        code = result["authorization_code"]
        
        result_vuln = vulnerable_oauth_flow(code, attack_uri)
        print(f"Vulnerable flow result: {'Success' if result_vuln['success'] else 'Failed'}")
        
        result_sec = secure_oauth_flow(code, attack_uri)
        print(f"Secure flow result: {'Success' if result_sec['success'] else 'Failed'}")
        
        if result_vuln["success"] and not result_sec["success"]:
            print("\n✓ Attack blocked by secure implementation!")
        
        validation = {"success": True, "message": "See how redirect_uri validation prevents attacks."}
        
    else:
        print("Invalid choice.")
        return False
    
    print()
    print("-" * 50)
    print()
    
    if "validation" in dir():
        print("RESULT:")
        print(validation["message"])
    
    print("\nKEY TAKEAWAYS:")
    print("  - Always validate redirect_uri")
    print("  - Use state parameter to prevent CSRF")
    print("  - Validate authorization codes (one-time, expiry)")
    print("  - Use PKCE for public clients")
    print("  - Implement proper token storage")
    print("  - Use short-lived tokens")
    
    print()
    print("OAUTH ATTACKS:")
    print("  - Authorization code interception")
    print("  - Redirect URI manipulation")
    print("  - CSRF attacks")
    print("  - Token leakage")
    
    print()
    print("-" * 50)
    print("Lab completed.")
    return True


if __name__ == "__main__":
    run()
