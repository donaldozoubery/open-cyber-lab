"""
Cross-Site Scripting (XSS) Lab

Learn about XSS vulnerabilities and how to prevent them.

This lab demonstrates reflected and stored XSS vulnerabilities
where user input is rendered without proper sanitization.

DISCLAIMER: This lab is for educational purposes only.
Always sanitize and escape user input in production.
"""

DIFFICULTY = "Intermediate"

OBJECTIVES = [
    "Understand what XSS is and its types",
    "Learn how attackers exploit XSS vulnerabilities",
    "Identify vulnerable code patterns",
    "Practice writing secure code"
]


def check_xss_payload(payload: str) -> bool:
    """Check if input contains XSS patterns.
    
    Args:
        payload: The input to check
        
    Returns:
        bool: True if XSS detected, False otherwise
    """
    xss_patterns = [
        "<script>",
        "javascript:",
        "onerror=",
        "onload=",
        "<img src=",
        "<svg",
        "alert(",
        "eval(",
        "document.cookie",
    ]
    
    payload_lower = payload.lower()
    for pattern in xss_patterns:
        if pattern in payload_lower:
            return True
    
    return False


def simulate_reflected_xss(name: str) -> dict:
    """Simulate a reflected XSS attack.
    
    Args:
        name: User input
        
    Returns:
        dict: Result with vulnerability status and details
    """
    # Vulnerable code: directly inserting user input into HTML
    html_response = f"""
    <html>
    <body>
        <h1>Welcome, {name}!</h1>
    </body>
    </html>
    """
    
    is_xss = check_xss_payload(name)
    
    return {
        "vulnerable": is_xss,
        "html": html_response,
        "input": name,
        "type": "reflected"
    }


def simulate_stored_xss(comment: str) -> dict:
    """Simulate a stored XSS attack.
    
    Args:
        comment: User comment
        
    Returns:
        dict: Result with vulnerability status and details
    """
    # Vulnerable code: storing unsanitized comment
    html_response = f"""
    <html>
    <body>
        <div class="comments">
            <p>{comment}</p>
        </div>
    </body>
    </html>
    """
    
    is_xss = check_xss_payload(comment)
    
    return {
        "vulnerable": is_xss,
        "html": html_response,
        "input": comment,
        "type": "stored"
    }


def validate_solution(input_text: str, xss_type: str = "reflected") -> dict:
    """Validate if the XSS exploit was successful.
    
    Args:
        input_text: The payload attempted
        xss_type: Type of XSS (reflected or stored)
        
    Returns:
        dict: Result with success status and explanation
    """
    is_xss = check_xss_payload(input_text)
    
    if is_xss:
        return {
            "success": True,
            "message": "XSS exploit successful! Your payload was executed.",
            "type": xss_type
        }
    
    return {
        "success": False,
        "message": "No XSS detected. Try using script tags or event handlers.",
        "type": xss_type
    }


def run(*args):
    """Run the XSS Lab."""
    print("=" * 50)
    print("    CROSS-SITE SCRIPTING (XSS) LAB")
    print("=" * 50)
    print()
    print("OBJECTIVES:")
    for i, obj in enumerate(OBJECTIVES, 1):
        print(f"  {i}. {obj}")
    print()
    print("-" * 50)
    print()
    
    # Get XSS type from args or default to reflected
    xss_type = args[0] if args else "reflected"
    
    print("XSS TYPES:")
    print("  1. Reflected XSS - Payload in URL parameter")
    print("  2. Stored XSS - Payload saved in database")
    print("  3. DOM-based XSS - Client-side manipulation")
    print()
    
    if xss_type == "stored":
        print("Mode: STORED XSS")
        print("-" * 50)
        print()
        print("A comment section that doesn't sanitize input.")
        print("Try injecting a script tag!")
        print()
        
        user_input = input("Enter your comment: ")
        
        result = simulate_stored_xss(user_input)
        
        print()
        print("Rendered HTML:")
        print(result["html"])
        print()
        
        validation = validate_solution(user_input, "stored")
        
    else:
        print("Mode: REFLECTED XSS")
        print("-" * 50)
        print()
        print("A search box that reflects your input without sanitization.")
        print("Try entering: <script>alert('XSS')</script>")
        print()
        
        user_input = input("Enter your name: ")
        
        result = simulate_reflected_xss(user_input)
        
        print()
        print("Rendered HTML:")
        print(result["html"])
        print()
        
        validation = validate_solution(user_input, "reflected")
    
    if validation["success"]:
        print("=" * 50)
        print("  CONGRATULATIONS!")
        print("=" * 50)
        print()
        print(validation["message"])
        print()
        print("EXPLANATION:")
        print("  XSS allows attackers to inject malicious scripts")
        print("  that run in the victim's browser.")
        print()
        print("  Attackers can:")
        print("  - Steal session cookies")
        print("  - Deface websites")
        print("  - Redirect users to malicious sites")
        print("  - Perform actions as the victim")
        print()
        print("HOW TO PREVENT:")
        print("  - Escape/encode all user input")
        print("  - Use Content Security Policy (CSP)")
        print("  - Use modern frameworks (React, Angular)")
        print("  - Validate input against allowlists")
    else:
        print("Keep trying!")
        print()
        print("TRY THESE PAYLOADS:")
        print("  <script>alert('XSS')</script>")
        print("  <img src=x onerror=alert('XSS')>")
        print("  <svg onload=alert('XSS')>")
        print("  javascript:alert('XSS')")
    
    print()
    print("-" * 50)
    print("Lab completed.")
    return True


if __name__ == "__main__":
    run()
