"""
JWT (JSON Web Token) Security Lab

Learn about JWT vulnerabilities and secure implementation.

This lab demonstrates common JWT security issues
and how to implement secure token handling.

DISCLAIMER: This lab is for educational purposes only.
Never exploit JWT vulnerabilities without authorization.
"""

DIFFICULTY = "Intermediate"

OBJECTIVES = [
    "Understand JWT structure",
    "Learn about JWT vulnerabilities",
    "Identify insecure implementations",
    "Practice secure JWT handling"
]

import base64
import json
import hashlib
import hmac
from typing import Optional


# Secret key for signing
SECRET_KEY = "super_secret_key_12345"


def base64url_encode(data: str) -> str:
    """Base64URL encode."""
    return base64.urlsafe_b64encode(data.encode()).decode().rstrip("=")


def base64url_decode(data: str) -> str:
    """Base64URL decode."""
    padding = 4 - len(data) % 4
    if padding != 4:
        data += "=" * padding
    return base64.urlsafe_b64decode(data).decode()


def create_jwt(payload: dict, algorithm: str = "HS256", secret: str = SECRET_KEY) -> str:
    """Create a JWT token.
    
    Args:
        payload: Token payload
        algorithm: Signing algorithm
        secret: Secret key
        
    Returns:
        str: JWT token
    """
    header = {"alg": algorithm, "typ": "JWT"}
    
    header_b64 = base64url_encode(json.dumps(header))
    payload_b64 = base64url_encode(json.dumps(payload))
    
    message = f"{header_b64}.{payload_b64}"
    
    if algorithm == "HS256":
        signature = hmac.new(secret.encode(), message.encode(), hashlib.sha256).hexdigest()
    elif algorithm == "HS384":
        signature = hmac.new(secret.encode(), message.encode(), hashlib.sha384).hexdigest()
    elif algorithm == "HS512":
        signature = hmac.new(secret.encode(), message.encode(), hashlib.sha512).hexdigest()
    else:
        signature = "invalid"
    
    return f"{message}.{base64url_encode(signature)}"


def verify_jwt(token: str, secret: str = SECRET_KEY) -> dict:
    """Verify and decode a JWT token.
    
    Args:
        token: JWT token
        secret: Secret key
        
    Returns:
        dict: Verification result
    """
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return {"valid": False, "error": "Invalid token format"}
        
        header_b64, payload_b64, signature_b64 = parts
        
        header = json.loads(base64url_decode(header_b64))
        payload = json.loads(base64url_decode(payload_b64))
        
        algorithm = header.get("alg", "HS256")
        
        # Verify signature
        message = f"{header_b64}.{payload_b64}"
        
        if algorithm == "HS256":
            expected_sig = hmac.new(secret.encode(), message.encode(), hashlib.sha256).hexdigest()
        elif algorithm == "HS384":
            expected_sig = hmac.new(secret.encode(), message.encode(), hashlib.sha384).hexdigest()
        elif algorithm == "HS512":
            expected_sig = hmac.new(secret.encode(), message.encode(), hashlib.sha512).hexdigest()
        else:
            return {"valid": False, "error": "Unsupported algorithm"}
        
        expected_sig_b64 = base64url_encode(expected_sig)
        
        if signature_b64 != expected_sig_b64:
            return {"valid": False, "error": "Invalid signature"}
        
        # Check expiration
        if "exp" in payload:
            import time
            if payload["exp"] < time.time():
                return {"valid": False, "error": "Token expired"}
        
        return {"valid": True, "payload": payload, "header": header}
        
    except Exception as e:
        return {"valid": False, "error": str(e)}


def vulnerable_algorithm_none(token: str) -> dict:
    """Simulate 'alg:none' attack.
    
    Args:
        token: JWT token
        
    Returns:
        dict: Attack result
    """
    try:
        # Attacker modifies algorithm to "none"
        parts = token.split(".")
        if len(parts) != 3:
            return {"success": False, "error": "Invalid token"}
        
        # Remove signature
        token_none = f"{parts[0]}.{parts[1]}."
        
        result = verify_jwt(token_none, secret="")
        
        if result["valid"]:
            return {
                "success": True,
                "message": "alg:none attack successful!",
                "payload": result.get("payload", {})
            }
        
        return {"success": False, "error": "Attack failed"}
        
    except Exception as e:
        return {"success": False, "error": str(e)}


def vulnerable_key_confusion(token: str, new_secret: str) -> dict:
    """Simulate key confusion attack (HS256 -> RS256).
    
    Args:
        token: JWT token
        new_secret: New secret key
        
    Returns:
        dict: Attack result
    """
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return {"success": False, "error": "Invalid token"}
        
        # Change algorithm to RS256 (simulated)
        header = json.loads(base64url_decode(parts[0]))
        header["alg"] = "RS256"
        
        new_header_b64 = base64url_encode(json.dumps(header))
        new_token = f"{new_header_b64}.{parts[1]}.{parts[2]}"
        
        # Try to verify with new secret
        result = verify_jwt(new_token, secret=new_secret)
        
        return {
            "success": result["valid"],
            "message": "Key confusion attack " + ("successful" if result["valid"] else "failed"),
            "note": "This attack exploits weak key handling"
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}


def run(*args):
    """Run the JWT Lab."""
    print("=" * 50)
    print("    JSON WEB TOKEN (JWT) SECURITY LAB")
    print("=" * 50)
    print()
    print("OBJECTIVES:")
    for i, obj in enumerate(OBJECTIVES, 1):
        print(f"  {i}. {obj}")
    print()
    print("-" * 50)
    print()
    
    print("JWT STRUCTURE:")
    print("  header.payload.signature")
    print("  (Base64URL encoded)")
    print()
    
    print("-" * 50)
    print()
    
    # Create a valid token for testing
    import time
    valid_payload = {
        "sub": "user123",
        "name": "John Doe",
        "role": "user",
        "exp": int(time.time()) + 3600
    }
    
    valid_token = create_jwt(valid_payload)
    print(f"Valid token: {valid_token[:50]}...")
    print()
    
    print("OPTIONS:")
    print("  1. Verify valid token")
    print("  2. Test 'alg:none' attack")
    print("  3. Test key confusion attack")
    print("  4. Create tokens")
    print()
    
    choice = input("Choose (1-4): ")
    
    if choice == "1":
        print("\n--- Verify Token ---")
        
        token = input("Enter JWT token: ")
        
        result = verify_jwt(token)
        
        if result["valid"]:
            print(f"\n✓ Token valid!")
            print(f"  Payload: {result['payload']}")
        else:
            print(f"\n✗ {result['error']}")
            
    elif choice == "2":
        print("\n--- 'alg:none' Attack ---")
        print("This attack removes the signature by setting alg=none")
        print()
        
        result = vulnerable_algorithm_none(valid_token)
        
        if result["success"]:
            print(f"\n✓ {result['message']}")
            print(f"  Forged payload: {result['payload']}")
            print("\n⚠️  This vulnerability allows bypassing signature verification!")
        else:
            print(f"\n✗ Attack failed: {result.get('error')}")
            
    elif choice == "3":
        print("\n--- Key Confusion Attack ---")
        print("This attack exploits RS256 -> HS256 algorithm confusion")
        print()
        
        result = vulnerable_key_confusion(valid_token, "attacker_key")
        
        print(f"\nResult: {result['message']}")
        
    elif choice == "4":
        print("\n--- Create JWT Tokens ---")
        
        role = input("Enter role (user/admin): ")
        
        payload = {
            "sub": "user123",
            "name": "Test User",
            "role": role,
            "exp": int(time.time()) + 3600
        }
        
        token = create_jwt(payload)
        print(f"\nCreated token: {token}")
        
        # Verify it
        result = verify_jwt(token)
        print(f"Verified: {result['valid']}")
        
    else:
        print("Invalid choice.")
        return False
    
    print()
    print("-" * 50)
    print()
    print("KEY TAKEAWAYS:")
    print("  - Always specify and verify the algorithm")
    print("  - Use strong secret keys")
    print("  - Implement proper token expiration")
    print("  - Validate all claims (iss, aud, exp)")
    print("  - Use secure libraries (PyJWT)")
    print("  - Don't trust the header for algorithm selection")
    
    print()
    print("JWT ATTACKS:")
    print("  - alg:none attack")
    print("  - Key confusion (RS256 -> HS256)")
    print("  - Weak secret key cracking")
    print("  - Algorithm confusion")
    print("  - JWT header injection")
    
    print()
    print("-" * 50)
    print("Lab completed.")
    return True


if __name__ == "__main__":
    run()
