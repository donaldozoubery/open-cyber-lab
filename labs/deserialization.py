"""
Insecure Deserialization Lab

Learn about insecure deserialization vulnerabilities.

This lab demonstrates how attackers exploit insecure
deserialization to execute arbitrary code.

DISCLAIMER: This lab is for educational purposes only.
Never exploit deserialization vulnerabilities without authorization.
"""

DIFFICULTY = "Advanced"

OBJECTIVES = [
    "Understand serialization and deserialization",
    "Learn about insecure deserialization risks",
    "Identify vulnerable code patterns",
    "Practice secure data handling"
]

import pickle
import base64
import os


class MaliciousPayload:
    """Simulated malicious payload for demonstration."""
    
    def __reduce__(self):
        """Simulate malicious code execution."""
        return (os.system, ("echo 'Vulnerable! Code executed!'; ls",))


def vulnerable_deserialize(data: str) -> dict:
    """Simulate vulnerable deserialization.
    
    Args:
        data: Base64 encoded serialized data
        
    Returns:
        dict: Deserialization result
    """
    try:
        # Vulnerable: Using pickle without validation
        decoded = base64.b64decode(data)
        obj = pickle.loads(decoded)
        
        return {
            "success": True,
            "deserialized": True,
            "object_type": type(obj).__name__,
            "vulnerable": True,
            "executed": True,
            "message": "Deserialization successful! (This is dangerous)"
        }
    except Exception as e:
        return {
            "success": False,
            "deserialized": False,
            "error": str(e),
            "vulnerable": True
        }


def secure_deserialize(data: str) -> dict:
    """Simulate secure deserialization.
    
    Args:
        data: Base64 encoded data
        
    Returns:
        dict: Deserialization result
    """
    try:
        # Secure: Use JSON instead of pickle
        decoded = base64.b64decode(data)
        import json
        obj = json.loads(decoded)
        
        return {
            "success": True,
            "deserialized": True,
            "data": obj,
            "vulnerable": False,
            "message": "JSON deserialization safe!"
        }
    except Exception as e:
        return {
            "success": False,
            "deserialized": False,
            "error": str(e),
            "vulnerable": False,
            "message": "Safe: Only JSON allowed"
        }


def create_malicious_payload() -> str:
    """Create a malicious pickle payload.
    
    Returns:
        str: Base64 encoded malicious payload
    """
    payload = MaliciousPayload()
    serialized = pickle.dumps(payload)
    return base64.b64encode(serialized).decode()


def create_safe_payload() -> str:
    """Create a safe JSON payload.
    
    Returns:
        str: Base64 encoded safe payload
    """
    import json
    data = {"user": "john", "role": "user"}
    serialized = json.dumps(data)
    return base64.b64encode(serialized.encode()).decode()


def validate_solution(is_vulnerable: bool, success: bool) -> dict:
    """Validate the solution.
    
    Args:
        is_vulnerable: Whether vulnerable method was used
        success: Whether deserialization succeeded
        
    Returns:
        dict: Validation result
    """
    if is_vulnerable and success:
        return {
            "success": True,
            "message": "Insecure deserialization exploited! Arbitrary code could be executed."
        }
    elif not is_vulnerable:
        return {
            "success": True,
            "message": "Secure deserialization! Only safe data types allowed."
        }
    
    return {
        "success": False,
        "message": "Deserialization failed. Try again."
    }


def run(*args):
    """Run the Insecure Deserialization Lab."""
    print("=" * 50)
    print("  INSECURE DESERIALIZATION LAB")
    print("=" * 50)
    print()
    print("OBJECTIVES:")
    for i, obj in enumerate(OBJECTIVES, 1):
        print(f"  {i}. {obj}")
    print()
    print("-" * 50)
    print()
    
    print("SCENARIO:")
    print("  A web application that uses pickle to serialize")
    print("  and deserialize user data without validation.")
    print()
    
    print("-" * 50)
    print()
    
    print("OPTIONS:")
    print("  1. Vulnerable deserialization (pickle)")
    print("  2. Secure deserialization (JSON)")
    print("  3. Test payloads")
    print()
    
    choice = input("Choose (1-3): ")
    
    if choice == "1":
        print("\n--- Vulnerable Deserialization ---")
        print("Vulnerable code:")
        print("  data = base64.b64decode(serialized)")
        print("  obj = pickle.loads(data)  # DANGEROUS!")
        print()
        
        # Generate malicious payload
        malicious = create_malicious_payload()
        print(f"Malicious payload: {malicious[:50]}...")
        print()
        
        use_payload = input("Use malicious payload? (y/n): ")
        
        if use_payload.lower() == "y":
            result = vulnerable_deserialize(malicious)
        else:
            data = input("Enter base64 data: ")
            result = vulnerable_deserialize(data)
        
        if result["success"]:
            print(f"\n✓ {result['message']}")
            print(f"Object type: {result['object_type']}")
        else:
            print(f"\n✗ {result['error']}")
        
        validation = validate_solution(is_vulnerable=True, success=result["success"])
        
    elif choice == "2":
        print("\n--- Secure Deserialization ---")
        print("Secure code:")
        print("  data = json.loads(base64.b64decode(serialized))")
        print()
        
        safe = create_safe_payload()
        print(f"Safe payload: {safe}")
        print()
        
        use_payload = input("Use safe payload? (y/n): ")
        
        if use_payload.lower() == "y":
            result = secure_deserialize(safe)
        else:
            data = input("Enter base64 data: ")
            result = secure_deserialize(data)
        
        if result["success"]:
            print(f"\n✓ {result['message']}")
            print(f"Data: {result['data']}")
        else:
            print(f"\n✗ {result['error']}")
        
        validation = validate_solution(is_vulnerable=False, success=result["success"])
        
    elif choice == "3":
        print("\n--- Test Payloads ---")
        
        # Safe JSON
        safe = create_safe_payload()
        print(f"\n1. Safe JSON: {safe}")
        
        # Malicious pickle
        malicious = create_malicious_payload()
        print(f"2. Malicious pickle: {malicious[:50]}...")
        
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
    print("  - Never unpickle untrusted data")
    print("  - Use JSON for data exchange")
    print("  - Use safer serialization libraries")
    print("  - Implement integrity checks")
    print("  - Run with minimal privileges")
    
    print()
    print("ATTACKS ENABLED:")
    print("  - Remote Code Execution (RCE)")
    print("  - Denial of Service (DoS)")
    print("  - Authentication bypass")
    
    print()
    print("-" * 50)
    print("Lab completed.")
    return True


if __name__ == "__main__":
    run()
