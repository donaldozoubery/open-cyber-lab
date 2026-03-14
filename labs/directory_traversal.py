"""
Directory Traversal Lab

Learn about directory traversal vulnerabilities.

This lab demonstrates how attackers use path manipulation
to access files outside the web root.

DISCLAIMER: This lab is for educational purposes only.
Never exploit directory traversal without authorization.
"""

DIFFICULTY = "Intermediate"

OBJECTIVES = [
    "Understand directory traversal vulnerabilities",
    "Learn path manipulation techniques",
    "Identify vulnerable code patterns",
    "Practice secure file handling"
]

from pathlib import Path


# Simulated file system
WEB_ROOT = Path("/var/www/html")
ALLOWED_DIR = Path("/var/www/html/uploads")

# Simulated sensitive files
SENSITIVE_FILES = {
    "/etc/passwd": "root:x:0:0:root:/root:/bin/bash\nadmin:x:1000:1000:admin:/home/admin:/bin/sh",
    "/etc/shadow": "root:$6$xyz:18000:0:99999:7:::\nadmin:$6$abc:18000:0:99999:7:::",
    "/var/www/html/../../etc/passwd": "root:x:0:0:root:/root:/bin/bash",
    "../../../etc/passwd": "root:x:0:0:root:/root:/bin/bash",
    "C:\\Windows\\System32\\config\\sam": "[SAM Database]",
}


def vulnerable_file_read(filename: str) -> dict:
    """Simulate vulnerable file read.
    
    Args:
        filename: User-provided filename
        
    Returns:
        dict: Result with file content or error
    """
    # Vulnerable: No path validation
    try:
        filepath = WEB_ROOT / filename
        
        # Try to read the file
        if str(filepath) in SENSITIVE_FILES:
            return {
                "success": True,
                "content": SENSITIVE_FILES[str(filepath)],
                "path": str(filepath),
                "vulnerable": True
            }
        
        return {
            "success": False,
            "error": "File not found",
            "path": str(filepath),
            "vulnerable": True
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "vulnerable": True
        }


def secure_file_read(filename: str, base_dir: Path = ALLOWED_DIR) -> dict:
    """Simulate secure file read.
    
    Args:
        filename: User-provided filename
        base_dir: Base directory to restrict access
        
    Returns:
        dict: Result with file content or error
    """
    try:
        # Secure: Resolve and validate path
        filepath = (base_dir / filename).resolve()
        
        # Check if resolved path is within allowed directory
        if not str(filepath).startswith(str(base_dir.resolve())):
            return {
                "success": False,
                "error": "Access denied: Path traversal detected!",
                "path": str(filepath),
                "vulnerable": False
            }
        
        # Check if file exists in our simulated system
        if str(filepath) in SENSITIVE_FILES:
            return {
                "success": True,
                "content": SENSITIVE_FILES[str(filepath)],
                "path": str(filepath),
                "vulnerable": False
            }
        
        return {
            "success": False,
            "error": "File not found",
            "path": str(filepath),
            "vulnerable": False
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "vulnerable": False
        }


def detect_traversal(payload: str) -> bool:
    """Detect directory traversal patterns.
    
    Args:
        payload: Input to check
        
    Returns:
        bool: True if traversal detected
    """
    patterns = [
        "../",
        "..\\",
        "..%2F",
        "..%5C",
        "....//",
        "....\\\\",
        "%2e%2e/",
        "%2e%2e\\",
        "..//",
        "..\\\\",
    ]
    
    payload_lower = payload.lower()
    for pattern in patterns:
        if pattern in payload_lower:
            return True
    
    return False


def validate_solution(payload: str, secure: bool = False) -> dict:
    """Validate the solution.
    
    Args:
        payload: Input to validate
        secure: Whether using secure method
        
    Returns:
        dict: Validation result
    """
    is_traversal = detect_traversal(payload)
    
    if secure:
        if is_traversal:
            return {
                "success": True,
                "message": "Attack blocked! Secure code detected the traversal attempt."
            }
        else:
            return {
                "success": False,
                "message": "Normal input processed securely."
            }
    
    if is_traversal:
        return {
            "success": True,
            "message": "Directory traversal successful! You accessed a sensitive file."
        }
    
    return {
        "success": False,
        "message": "No traversal detected. Try using ../ in the filename."
    }


def run(*args):
    """Run the Directory Traversal Lab."""
    print("=" * 50)
    print("      DIRECTORY TRAVERSAL LAB")
    print("=" * 50)
    print()
    print("OBJECTIVES:")
    for i, obj in enumerate(OBJECTIVES, 1):
        print(f"  {i}. {obj}")
    print()
    print("-" * 50)
    print()
    
    print("SCENARIO:")
    print("  A file upload/download feature that doesn't properly")
    print("  validate file paths, allowing attackers to access")
    print("  files outside the web directory.")
    print()
    
    print("-" * 50)
    print()
    
    print("OPTIONS:")
    print("  1. Vulnerable file read (no validation)")
    print("  2. Secure file read (with validation)")
    print("  3. Test payloads")
    print()
    
    choice = input("Choose (1-3): ")
    
    if choice == "1":
        print("\n--- Vulnerable File Read ---")
        print("This simulates code like:")
        print('  filepath = web_root + filename')
        print('  content = open(filepath).read()')
        print()
        
        filename = input("Enter filename: ")
        
        result = vulnerable_file_read(filename)
        
        if result["success"]:
            print(f"\n✓ File accessed: {result['path']}")
            print(f"Content:\n{result['content']}")
        else:
            print(f"\n✗ {result['error']}")
            print(f"Attempted path: {result['path']}")
        
        validation = validate_solution(filename, secure=False)
        
    elif choice == "2":
        print("\n--- Secure File Read ---")
        print("This simulates secure code:")
        print("  filepath = resolve(base_dir + filename)")
        print("  if not filepath.startswith(base_dir):")
        print("      raise AccessDenied")
        print()
        
        filename = input("Enter filename: ")
        
        result = secure_file_read(filename)
        
        if result["success"]:
            print(f"\n✓ File accessed: {result['path']}")
            print(f"Content:\n{result['content']}")
            validation = {"success": False, "message": "Normal access worked."}
        else:
            print(f"\n✗ {result['error']}")
            print(f"Attempted path: {result['path']}")
            validation = validate_solution(filename, secure=True)
        
    elif choice == "3":
        print("\n--- Common Payloads ---")
        
        payloads = [
            "../../../etc/passwd",
            "..\\..\\..\\Windows\\System32\\config\\sam",
            "....//....//....//etc/passwd",
            "..%2F..%2F..%2Fetc%2Fpasswd",
            "uploads/../../../etc/passwd",
        ]
        
        print("\nPayloads to try:")
        for i, payload in enumerate(payloads, 1):
            detection = "✓" if detect_traversal(payload) else "✗"
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
    
    if validation["success"]:
        print("RESULT:")
        print(validation["message"])
    
    print("\nKEY TAKEAWAYS:")
    print("  - Always validate and sanitize file paths")
    print("  - Use allowlist for allowed files")
    print("  - Resolve paths and check they're within allowed directory")
    print("  - Avoid using user input directly in file paths")
    print("  - Use filesystem APIs that prevent traversal")
    print("  - Run web server with minimal privileges")
    
    print()
    print("-" * 50)
    print("Lab completed.")
    return True


if __name__ == "__main__":
    run()
