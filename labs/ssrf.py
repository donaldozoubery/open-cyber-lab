"""
Server-Side Request Forgery (SSRF) Lab

Learn about SSRF vulnerabilities and secure URL handling.

This lab demonstrates how attackers make the server
perform requests to internal resources.

DISCLAIMER: This lab is for educational purposes only.
Never exploit SSRF without authorization.
"""

DIFFICULTY = "Intermediate"

OBJECTIVES = [
    "Understand what SSRF is",
    "Learn how attackers access internal services",
    "Identify vulnerable code patterns",
    "Practice secure URL validation"
]



# Simulated internal services
INTERNAL_SERVICES = {
    "localhost": "127.0.0.1",
    "127.0.0.1": "127.0.0.1",
    "169.254.169.254": "AWS Metadata Service",
    "metadata.google": "GCP Metadata Service",
    "metadata.google.internal": "GCP Metadata Service",
    "192.168.1.1": "Router Admin Panel",
    "192.168.1.254": "Gateway",
    "10.0.0.1": "Internal Server",
    "172.16.0.1": "Internal Database",
}


def vulnerable_url_fetch(url: str) -> dict:
    """Simulate vulnerable URL fetching.
    
    Args:
        url: User-provided URL
        
    Returns:
        dict: Fetch result
    """
    # Vulnerable: No URL validation
    try:
        # Simulate fetching the URL
        if "localhost" in url.lower() or "127.0.0.1" in url:
            return {
                "success": True,
                "url": url,
                "response": "Internal service accessed!",
                "internal_access": True,
                "vulnerable": True
            }
        
        if "169.254" in url:
            return {
                "success": True,
                "url": url,
                "response": "Cloud metadata service accessed!",
                "internal_access": True,
                "metadata": {"access_key": "AKIAIOSFODNN7EXAMPLE"},
                "vulnerable": True
            }
        
        return {
            "success": True,
            "url": url,
            "response": "External request processed",
            "internal_access": False,
            "vulnerable": True
        }
        
    except Exception as e:
        return {
            "success": False,
            "url": url,
            "error": str(e),
            "vulnerable": True
        }


def secure_url_fetch(url: str) -> dict:
    """Simulate secure URL fetching with validation.
    
    Args:
        url: User-provided URL
        
    Returns:
        dict: Fetch result
    """
    # Secure: Validate URL before fetching
    
    # Block private/internal IP ranges
    blocked_ips = [
        "127.",  # Loopback
        "10.",    # Private Class A
        "172.16.",  # Private Class B
        "192.168.",  # Private Class C
        "169.254.",  # Link-local
        "0.",     # Current network
    ]
    
    # Block dangerous hosts
    blocked_hosts = [
        "localhost",
        "metadata.google",
        "metadata.google.internal",
    ]
    
    # Check for blocked hosts
    url_lower = url.lower()
    for host in blocked_hosts:
        if host in url_lower:
            return {
                "success": False,
                "url": url,
                "error": "Access to this host is blocked!",
                "blocked": True,
                "vulnerable": False
            }
    
    # Check for blocked IP patterns
    for ip_prefix in blocked_ips:
        if ip_prefix in url:
            return {
                "success": False,
                "url": url,
                "error": "Access to internal networks is blocked!",
                "blocked": True,
                "vulnerable": False
            }
    
    return {
        "success": True,
        "url": url,
        "response": "External request processed securely",
        "internal_access": False,
        "vulnerable": False
    }


def check_ssrf_payload(url: str) -> bool:
    """Check if URL is a potential SSRF payload.
    
    Args:
        url: URL to check
        
    Returns:
        bool: True if SSRF detected
    """
    ssrf_indicators = [
        "localhost",
        "127.0.0.1",
        "0.0.0.0",
        "169.254.169.254",
        "metadata.google",
        "192.168.",
        "10.",
        "172.16.",
    ]
    
    url_lower = url.lower()
    return any(indicator in url_lower for indicator in ssrf_indicators)


def validate_solution(url: str, secure: bool = False) -> dict:
    """Validate the solution.
    
    Args:
        url: URL to validate
        secure: Whether using secure method
        
    Returns:
        dict: Validation result
    """
    is_ssrf = check_ssrf_payload(url)
    
    if secure:
        if is_ssrf:
            return {
                "success": True,
                "message": "SSRF attack blocked! Input validation prevented access."
            }
        return {
            "success": True,
            "message": "Normal URL processed securely."
        }
    
    if is_ssrf:
        return {
            "success": True,
            "message": "SSRF successful! You accessed internal resources."
        }
    
    return {
        "success": False,
        "message": "No SSRF detected. Try targeting localhost or internal IPs."
    }


def run(*args):
    """Run the SSRF Lab."""
    print("=" * 50)
    print("  SERVER-SIDE REQUEST FORGERY (SSRF) LAB")
    print("=" * 50)
    print()
    print("OBJECTIVES:")
    for i, obj in enumerate(OBJECTIVES, 1):
        print(f"  {i}. {obj}")
    print()
    print("-" * 50)
    print()
    
    print("SCENARIO:")
    print("  A web application that fetches URLs from user input")
    print("  to generate previews, but doesn't validate them properly.")
    print()
    
    print("-" * 50)
    print()
    
    print("OPTIONS:")
    print("  1. Vulnerable URL fetch (no validation)")
    print("  2. Secure URL fetch (with validation)")
    print("  3. Test payloads")
    print()
    
    choice = input("Choose (1-3): ")
    
    if choice == "1":
        print("\n--- Vulnerable URL Fetch ---")
        print("Vulnerable code:")
        print('  response = requests.get(user_url)')
        print('  # No validation of the URL!')
        print()
        
        url = input("Enter URL to fetch: ")
        
        result = vulnerable_url_fetch(url)
        
        print(f"\nURL: {result['url']}")
        print(f"Response: {result['response']}")
        
        if result.get("internal_access"):
            print("\n⚠️  INTERNAL RESOURCE ACCESSED!")
            if "metadata" in result.get("response", "").lower():
                print(f"  Cloud metadata: {result.get('metadata', {})}")
        
        validation = validate_solution(url, secure=False)
        
    elif choice == "2":
        print("\n--- Secure URL Fetch ---")
        print("Secure code:")
        print("  # Block private IPs and internal services")
        print("  if is_internal_ip(url):")
        print("      raise SecurityError('Blocked')")
        print("  # Use URL allowlist")
        print("  if not is_allowed_domain(url):")
        print("      raise SecurityError('Blocked')")
        print()
        
        url = input("Enter URL to fetch: ")
        
        result = secure_url_fetch(url)
        
        if result["success"]:
            print(f"\n✓ URL processed: {result['url']}")
            print(f"Response: {result['response']}")
        else:
            print(f"\n✗ {result['error']}")
            print(f"URL: {result['url']}")
        
        validation = validate_solution(url, secure=True)
        
    elif choice == "3":
        print("\n--- Common SSRF Payloads ---")
        
        payloads = [
            "http://example.com",
            "http://localhost/admin",
            "http://127.0.0.1:8080",
            "http://169.254.169.254/latest/meta-data/",
            "http://metadata.google.internal/computeMetadata",
            "http://192.168.1.1/router-admin",
            "http://10.0.0.1/database",
            "http://172.16.0.1:3306",
        ]
        
        print("\nPayloads to try:")
        for i, payload in enumerate(payloads, 1):
            detection = "✓" if check_ssrf_payload(payload) else "✗"
            print(f"  {i}. {detection} {payload}")
        
        print()
        print("Try these in option 1 (vulnerable) or 2 (secure)!")
        validation = {"success": True, "message": "Review these payloads."}
        
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
    print("  - SSRF allows attackers to access internal services")
    print("  - Block access to localhost and private IP ranges")
    print("  - Use URL allowlists")
    print("  - Disable unused URL schemas (file://, gopher://)")
    print("  - Timeout requests to prevent DoS")
    print("  - Don't expose services unnecessarily")
    
    print()
    print("ATTACKS ENABLED BY SSRF:")
    print("  - Access internal dashboards")
    print("  - Cloud metadata exposure")
    print("  - Port scanning internal network")
    print("  - Access databases")
    print("  - Read local files (file://)")
    
    print()
    print("-" * 50)
    print("Lab completed.")
    return True


if __name__ == "__main__":
    run()
