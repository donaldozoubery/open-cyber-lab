"""
Information Disclosure Lab

Learn about information disclosure vulnerabilities.

This lab demonstrates how applications accidentally
leak sensitive information.

DISCLAIMER: This lab is for educational purposes only.
Never exploit information disclosure without authorization.
"""

DIFFICULTY = "Beginner"

OBJECTIVES = [
    "Understand information disclosure",
    "Learn common sources of leaks",
    "Identify sensitive data",
    "Practice secure data handling"
]



# Simulated responses
ERROR_MESSAGES = {
    "user_not_found": "User not found",
    "invalid_password": "Invalid password",
    "account_locked": "Account locked",
    "email_not_found": "Email address not found",
}

# Sensitive data exposure
DEBUG_INFO = {
    "version": "1.2.3",
    "python_version": "3.11.0",
    "os": "Linux 5.10.0",
    "database": "PostgreSQL 14.5",
    "internal_ip": "192.168.1.100",
    "api_key": "sk_live_1234567890",
}


def vulnerable_login(username: str, password: str) -> dict:
    """Simulate vulnerable login with verbose errors.
    
    Args:
        username: Username
        password: Password
        
    Returns:
        dict: Login result
    """
    # VULNERABLE: Different messages for username vs password
    
    if username == "admin":
        if password == "wrong":
            return {
                "success": False,
                "error": "Invalid password",
                "vulnerable": True
            }
        return {"success": True, "message": "Login successful"}
    
    # Different message reveals if username exists
    if username not in ["admin", "user", "guest"]:
        return {
            "success": False,
            "error": "User not found",  # Reveals username validity!
            "vulnerable": True
        }
    
    return {"success": False, "error": "Invalid credentials"}


def secure_login(username: str, password: str) -> dict:
    """Simulate secure login with generic errors.
    
    Args:
        username: Username
        password: Password
        
    Returns:
        dict: Login result
    """
    # SECURE: Generic error message
    
    if username == "admin" and password == "admin123":
        return {"success": True, "message": "Login successful"}
    
    # Always the same message
    return {
        "success": False,
        "error": "Invalid username or password",  # Generic!
        "vulnerable": False
    }


def vulnerable_error_handling(endpoint: str) -> dict:
    """Simulate vulnerable error messages.
    
    Args:
        endpoint: API endpoint
        
    Returns:
        dict: Error response
    """
    errors = {
        "users": "PostgreSQL error: relation 'users' does not exist at character 15",
        "admin": "DEBUG: Stack trace at /app/routes/admin.py:line 42",
        "config": "Config file not found: /etc/app/config.ini (Permission denied)",
        "debug": f"Internal IP: {DEBUG_INFO['internal_ip']}, Python: {DEBUG_INFO['python_version']}",
    }
    
    if endpoint in errors:
        return {
            "success": False,
            "error": errors[endpoint],
            "vulnerable": True,
            "disclosure_type": "verbose_error"
        }
    
    return {"success": True, "message": "OK"}


def secure_error_handling(endpoint: str) -> dict:
    """Simulate secure error messages.
    
    Args:
        endpoint: API endpoint
        
    Returns:
        dict: Error response
    """
    return {
        "success": False,
        "error": "An error occurred. Please contact support.",
        "vulnerable": False,
        "disclosure_type": "generic"
    }


def check_sensitive_exposure(response: dict) -> dict:
    """Check for sensitive data exposure.
    
    Args:
        response: API response
        
    Returns:
        dict: Analysis result
    """
    sensitive_keywords = [
        "password", "secret", "key", "token", "debug", "stack",
        "trace", "internal", "ip", "version", "postgresql"
    ]
    
    error_msg = response.get("error", "").lower()
    
    exposed = []
    for keyword in sensitive_keywords:
        if keyword in error_msg:
            exposed.append(keyword)
    
    return {
        "has_disclosure": len(exposed) > 0,
        "exposed_keywords": exposed,
        "severity": "high" if exposed else "none"
    }


def run(*args):
    """Run the Information Disclosure Lab."""
    print("=" * 50)
    print("    INFORMATION DISCLOSURE LAB")
    print("=" * 50)
    print()
    print("OBJECTIVES:")
    for i, obj in enumerate(OBJECTIVES, 1):
        print(f"  {i}. {obj}")
    print()
    print("-" * 50)
    print()
    
    print("SCENARIO:")
    print("  Applications that accidentally expose sensitive")
    print("  information through error messages or debugging.")
    print()
    
    print("-" * 50)
    print()
    
    print("OPTIONS:")
    print("  1. Vulnerable login (username enumeration)")
    print("  2. Secure login (generic errors)")
    print("  3. Error message analysis")
    print("  4. API endpoint testing")
    print()
    
    choice = input("Choose (1-4): ")
    
    if choice == "1":
        print("\n--- Vulnerable Login ---")
        
        username = input("Username: ")
        password = input("Password: ")
        
        result = vulnerable_login(username, password)
        
        print(f"\nResult: {result['error']}")
        
        if "not found" in result["error"].lower():
            print("\n⚠️  This message reveals if the username exists!")
            print("  Attacker can enumerate valid usernames.")
        
    elif choice == "2":
        print("\n--- Secure Login ---")
        
        username = input("Username: ")
        password = input("Password: ")
        
        result = secure_login(username, password)
        
        if result["success"]:
            print(f"\nResult: {result['message']}")
        else:
            print(f"\nResult: {result['error']}")
            print("\n✓ Generic message doesn't reveal username validity!")
        
    elif choice == "3":
        print("\n--- Error Message Analysis ---")
        
        endpoints = ["users", "admin", "config", "debug", "login"]
        
        for ep in endpoints:
            result = vulnerable_error_handling(ep)
            if not result["success"]:
                analysis = check_sensitive_exposure(result)
                print(f"\n{ep}: {result['error'][:60]}...")
                if analysis["has_disclosure"]:
                    print(f"  ⚠️  Exposed: {analysis['exposed_keywords']}")
        
    elif choice == "4":
        print("\n--- API Endpoint Testing ---")
        
        endpoint = input("Endpoint (users/admin/config/debug): ")
        
        result_vuln = vulnerable_error_handling(endpoint)
        result_secure = secure_error_handling(endpoint)
        
        print(f"\nVulnerable: {result_vuln['error'][:50]}...")
        print(f"Secure: {result_secure['error']}")
        
        analysis = check_sensitive_exposure(result_vuln)
        if analysis["has_disclosure"]:
            print(f"\n⚠️  Information disclosed: {analysis['exposed_keywords']}")
        
    else:
        print("Invalid choice.")
        return False
    
    print()
    print("-" * 50)
    print()
    print("KEY TAKEAWAYS:")
    print("  - Use generic error messages")
    print("  - Disable debug mode in production")
    print("  - Don't expose stack traces")
    print("  - Don't expose version information")
    print("  - Sanitize error responses")
    print("  - Log errors server-side only")
    
    print()
    print("DISCLOSURE TYPES:")
    print("  - Username enumeration")
    print("  - Verbose error messages")
    print("  - Stack traces")
    print("  - Version information")
    print("  - Internal IP addresses")
    print("  - Database information")
    
    print()
    print("-" * 50)
    print("Lab completed.")
    return True


if __name__ == "__main__":
    run()
