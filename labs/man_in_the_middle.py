"""
Man-in-the-Middle (MITM) Attack Lab

Learn about MITM attacks and secure communication.

This lab demonstrates how attackers intercept communications
between two parties and how encryption prevents this.

DISCLAIMER: This lab is for educational purposes only.
Never perform MITM attacks without authorization.
"""

DIFFICULTY = "Advanced"

OBJECTIVES = [
    "Understand what MITM attacks are",
    "Learn how attackers intercept communications",
    "Understand encryption and certificates",
    "Learn how to detect and prevent MITM"
]

import hashlib
import base64
import time
from typing import Optional


# Simulated network entities
ALICE = {"name": "Alice", "ip": "192.168.1.10", "public_key": None}
BOB = {"name": "Bob", "ip": "192.168.1.20", "public_key": None}
ATTACKER = {"name": "Eve", "ip": "192.168.1.100", "public_key": None}


def generate_key_pair() -> tuple:
    """Generate simulated key pair.
    
    Returns:
        tuple: (public_key, private_key)
    """
    # Simplified for demo - real implementation would use RSA/ECC
    key = hashlib.sha256(str(time.time()).encode()).hexdigest()[:32]
    return key, key  # In reality, these would be different


def simulate_unencrypted_communication(message: str) -> dict:
    """Simulate unencrypted communication.
    
    Args:
        message: Message to send
        
    Returns:
        dict: Communication result
    """
    return {
        "sender": "Alice",
        "receiver": "Bob",
        "message": message,
        "encrypted": False,
        "interceptable": True,
        "visible_to_attacker": True
    }


def simulate_encrypted_communication(message: str) -> dict:
    """Simulate encrypted communication.
    
    Args:
        message: Message to send
        
    Returns:
        dict: Communication result
    """
    return {
        "sender": "Alice",
        "receiver": "Bob",
        "message": "[ENCRYPTED]",
        "encrypted": True,
        "interceptable": True,
        "visible_to_attacker": False,
        "content": message  # Only visible to Alice and Bob
    }


def simulate_mitm_attack(message: str) -> dict:
    """Simulate MITM attack on unencrypted communication.
    
    Args:
        message: Message being sent
        
    Returns:
        dict: Attack simulation results
    """
    return {
        "attacker": "Eve",
        "action": "intercept",
        "original_message": message,
        "modified": False,
        "message_visible": True,
        "can_modify": True,
        "can_eavesdrop": True
    }


def simulate_mitm_on_encrypted(message: str) -> dict:
    """Simulate MITM attack on encrypted communication.
    
    Args:
        message: Message being sent
        
    Returns:
        dict: Attack results
    """
    return {
        "attacker": "Eve",
        "action": "intercept",
        "message_visible": False,
        "can_modify": False,
        "certificate_error": "Certificate mismatch!"
    }


def check_encryption(method: str) -> dict:
    """Check if encryption method is secure.
    
    Args:
        method: Encryption method
        
    Returns:
        dict: Security assessment
    """
    secure_methods = {
        "tls": "Secure - Use TLS 1.3",
        "ssl": "Secure when properly configured",
        "https": "Secure - Uses TLS",
        "ssh": "Secure - Use SSH v2",
        "wireguard": "Very secure",
        "ipsec": "Secure at network layer"
    }
    
    insecure_methods = {
        "http": "INSECURE - No encryption",
        "ftp": "INSECURE - Credentials visible",
        "telnet": "INSECURE - All data visible",
        "smtp": "INSECURE without TLS",
        "pop3": "INSECURE without TLS"
    }
    
    method_lower = method.lower()
    
    for secure, message in secure_methods.items():
        if secure in method_lower:
            return {"secure": True, "message": message, "method": method}
    
    for insecure, message in insecure_methods.items():
        if insecure in method_lower:
            return {"secure": False, "message": message, "method": method}
    
    return {"secure": None, "message": "Unknown method", "method": method}


def run(*args):
    """Run the MITM Lab."""
    print("=" * 50)
    print("   MAN-IN-THE-MIDDLE (MITM) ATTACK LAB")
    print("=" * 50)
    print()
    print("OBJECTIVES:")
    for i, obj in enumerate(OBJECTIVES, 1):
        print(f"  {i}. {obj}")
    print()
    print("-" * 50)
    print()
    
    print("SCENARIO:")
    print("  Alice wants to send a message to Bob.")
    print("  Eve is trying to intercept the communication.")
    print()
    
    print("-" * 50)
    print()
    
    print("OPTIONS:")
    print("  1. Unencrypted communication (HTTP)")
    print("  2. Encrypted communication (HTTPS)")
    print("  3. MITM attack demonstration")
    print("  4. Check encryption methods")
    print()
    
    choice = input("Choose (1-4): ")
    
    if choice == "1":
        print("\n--- Unencrypted Communication ---")
        message = input("Enter message from Alice to Bob: ")
        
        result = simulate_unencrypted_communication(message)
        
        print()
        print(f"Sender: {result['sender']}")
        print(f"Receiver: {result['receiver']}")
        print(f"Message: {result['message']}")
        print(f"Encrypted: {result['encrypted']}")
        print()
        print("⚠️  WARNING: This communication can be intercepted!")
        
    elif choice == "2":
        print("\n--- Encrypted Communication ---")
        message = input("Enter message from Alice to Bob: ")
        
        result = simulate_encrypted_communication(message)
        
        print()
        print(f"Sender: {result['sender']}")
        print(f"Receiver: {result['receiver']}")
        print(f"Message: {result['message']}")
        print(f"Encrypted: {result['encrypted']}")
        print(f"Content (hidden from attacker): {result['content']}")
        print()
        print("✓ This communication is protected by encryption!")
        
    elif choice == "3":
        print("\n--- MITM Attack Demonstration ---")
        print("\nScenario 1: Unencrypted")
        print("  Alice → [Eve intercepts] → Bob")
        
        message = "Hello Bob, send me the password!"
        result = simulate_mitm_attack(message)
        
        print(f"  Original: {result['original_message']}")
        print(f"  Eve can see: {result['message_visible']}")
        print(f"  Eve can modify: {result['can_modify']}")
        
        print("\nScenario 2: Encrypted")
        print("  Alice → [Eve intercepts] → Bob")
        
        result = simulate_mitm_on_encrypted(message)
        
        print(f"  Eve can see: {result['message_visible']}")
        print(f"  Eve can modify: {result['can_modify']}")
        print(f"  Result: {result['certificate_error']}")
        
    elif choice == "4":
        print("\n--- Encryption Method Check ---")
        
        methods = ["https", "http", "ssh", "ftp", "telnet", "smtp", "wireguard"]
        
        for method in methods:
            result = check_encryption(method)
            status = "✓" if result["secure"] else "✗" if result["secure"] is False else "?"
            print(f"  {status} {method.upper()}: {result['message']}")
        
        print()
        method = input("Enter a protocol to check: ")
        result = check_encryption(method)
        
        if result["secure"]:
            print(f"\n✓ {result['message']}")
        elif result["secure"] is False:
            print(f"\n✗ {result['message']}")
        else:
            print(f"\n? {result['message']}")
    
    else:
        print("Invalid choice.")
        return False
    
    print()
    print("-" * 50)
    print()
    print("KEY TAKEAWAYS:")
    print("  - MITM attacks intercept unencrypted communications")
    print("  - Always use HTTPS/TLS for sensitive data")
    print("  - Verify SSL certificates")
    print("  - Use VPN on public networks")
    print("  - Implement certificate pinning")
    print("  - HSTS forces HTTPS connections")
    print()
    print("DETECTION:")
    print("  - Check for valid certificates")
    print("  - Look for HTTPS in URL")
    print("  - Monitor for unexpected redirects")
    print("  - Use network monitoring tools")
    
    print()
    print("-" * 50)
    print("Lab completed.")
    return True


if __name__ == "__main__":
    run()
