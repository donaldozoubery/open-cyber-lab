"""
Ransomware Awareness Lab

Learn about ransomware attacks and how to prevent them.

This lab demonstrates how ransomware encrypts files and
teaches protection and recovery strategies.

DISCLAIMER: This lab is for educational purposes only.
Never create or use ransomware for malicious purposes.
"""

DIFFICULTY = "Advanced"

OBJECTIVES = [
    "Understand what ransomware is",
    "Learn how encryption-based ransomware works",
    "Identify ransomware behavior patterns",
    "Practice protection and recovery strategies"
]

import os
import hashlib
import base64
from typing import Optional
from pathlib import Path


# Simulated encrypted files
ENCRYPTED_FILES: dict = {}


def generate_key() -> bytes:
    """Generate a simulated encryption key.
    
    Returns:
        bytes: Simulated key
    """
    return hashlib.sha256(b"ransomware_key").digest()[:16]


def simple_encrypt(data: str, key: bytes) -> str:
    """Simulate encryption (XOR-based for demo).
    
    Args:
        data: Data to encrypt
        key: Encryption key
        
    Returns:
        str: Encrypted data (base64 encoded)
    """
    encrypted = bytearray()
    key_len = len(key)
    for i, char in enumerate(data.encode()):
        encrypted.append(char ^ key[i % key_len])
    return base64.b64encode(bytes(encrypted)).decode()


def simple_decrypt(data: str, key: bytes) -> str:
    """Simulate decryption.
    
    Args:
        data: Data to decrypt
        key: Encryption key
        
    Returns:
        str: Decrypted data
    """
    decoded = base64.b64decode(data.encode())
    decrypted = bytearray()
    key_len = len(key)
    for i, char in enumerate(decoded):
        decrypted.append(char ^ key[i % key_len])
    return bytes(decrypted).decode()


def simulate_ransomware(target_files: list) -> dict:
    """Simulate a ransomware attack.
    
    Args:
        target_files: List of file paths to encrypt
        
    Returns:
        dict: Attack simulation results
    """
    key = generate_key()
    global ENCRYPTED_FILES
    
    encrypted_list = []
    
    for filepath in target_files:
        # Simulate reading and encrypting file
        original_content = f"Content of {filepath}"
        encrypted_content = simple_encrypt(original_content, key)
        
        ENCRYPTED_FILES[filepath] = {
            "encrypted": encrypted_content,
            "original": original_content,
            "key": key.hex()
        }
        
        encrypted_list.append({
            "file": filepath,
            "status": "encrypted",
            "extension": ".encrypted"
        })
    
    return {
        "success": True,
        "files_encrypted": len(encrypted_list),
        "files": encrypted_list,
        "ransom_note": "Your files have been encrypted! Pay 0.001 BTC to recover them."
    }


def simulate_recovery(file_path: str, key: str) -> dict:
    """Simulate file recovery with key.
    
    Args:
        file_path: File to recover
        key: Decryption key
        
    Returns:
        dict: Recovery result
    """
    global ENCRYPTED_FILES
    
    if file_path not in ENCRYPTED_FILES:
        return {
            "success": False,
            "message": "File not found in encrypted files"
        }
    
    encrypted_data = ENCRYPTED_FILES[file_path]
    
    if key != encrypted_data["key"]:
        return {
            "success": False,
            "message": "Invalid decryption key!"
        }
    
    try:
        key_bytes = bytes.fromhex(key)
        decrypted = simple_decrypt(encrypted_data["encrypted"], key_bytes)
        
        return {
            "success": True,
            "message": "File recovered successfully!",
            "content": decrypted
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Recovery failed: {e}"
        }


def check_protection_measure(measure: str) -> dict:
    """Check if protection measure is effective.
    
    Args:
        measure: Protection measure to check
        
    Returns:
        dict: Result with effectiveness
    """
    effective_measures = {
        "backup": "Most effective! Regular offline backups",
        "offline backup": "Most effective! Regular offline backups",
        "antivirus": "Effective against known ransomware",
        "update": "Keeps security patches up to date",
        "patch": "Keeps security patches up to date",
        "least privilege": "Limits ransomware spread",
        "segmentation": "Limits ransomware spread",
        "education": "Prevents phishing-based ransomware",
        "training": "Prevents phishing-based ransomware",
    }
    
    measure_lower = measure.lower()
    
    for key, value in effective_measures.items():
        if key in measure_lower:
            return {
                "effective": True,
                "measure": value,
                "message": "This is an effective protection measure!"
            }
    
    return {
        "effective": False,
        "measure": measure,
        "message": "This measure alone is not sufficient. Consider additional protections."
    }


def run(*args):
    """Run the Ransomware Lab."""
    print("=" * 50)
    print("        RANSOMWARE AWARENESS LAB")
    print("=" * 50)
    print()
    print("OBJECTIVES:")
    for i, obj in enumerate(OBJECTIVES, 1):
        print(f"  {i}. {obj}")
    print()
    print("-" * 50)
    print()
    
    print("WARNING:")
    print("  This lab is for educational purposes only.")
    print("  Ransomware is illegal and unethical when used maliciously.")
    print()
    
    print("-" * 50)
    print()
    
    print("OPTIONS:")
    print("  1. Simulate ransomware attack")
    print("  2. Try to recover files")
    print("  3. Learn protection measures")
    print()
    
    choice = input("Choose (1-3): ")
    
    if choice == "1":
        print("\n--- Ransomware Attack Simulation ---")
        print("Files to encrypt:")
        target_files = ["document1.txt", "photo.jpg", "backup.zip", "important.pdf"]
        
        for f in target_files:
            print(f"  - {f}")
        
        print("\nEncrypting files...")
        
        result = simulate_ransomware(target_files)
        
        print(f"\nFiles encrypted: {result['files_encrypted']}")
        print(f"\nRansom note: {result['ransom_note']}")
        
        print("\n" + "=" * 50)
        print("  WHAT JUST HAPPENED?")
        print("=" * 50)
        print("  Ransomware encrypted your files using a symmetric key.")
        print("  The attacker now has the only copy of the decryption key.")
        
    elif choice == "2":
        print("\n--- File Recovery ---")
        file_path = input("Enter file to recover: ")
        key = input("Enter decryption key: ")
        
        result = simulate_recovery(file_path, key)
        
        if result["success"]:
            print(f"\n✓ {result['message']}")
            print(f"Content: {result['content']}")
        else:
            print(f"\n✗ {result['message']}")
        
    elif choice == "3":
        print("\n--- Protection Measures ---")
        print("\nCommon protection measures:")
        print("  - Regular backups")
        print("  - Offline backups")
        print("  - Antivirus software")
        print("  - Keep systems updated")
        print("  - Least privilege principle")
        print("  - Network segmentation")
        print("  - Security training")
        print()
        
        measure = input("Enter a protection measure: ")
        
        result = check_protection_measure(measure)
        
        print()
        if result["effective"]:
            print("✓ " + result["message"])
        else:
            print("✗ " + result["message"])
            print("  This alone is not sufficient. You need defense in depth.")
    
    else:
        print("Invalid choice.")
        return False
    
    print()
    print("-" * 50)
    print()
    print("KEY TAKEAWAYS:")
    print("  - Prevention is key: regular backups")
    print("  - Don't click suspicious links/attachments")
    print("  - Keep software updated")
    print("  - Use reputable antivirus")
    print("  - Network segmentation limits spread")
    print("  - Have an incident response plan")
    print()
    print("  If infected:")
    print("  1. Isolate the system immediately")
    print("  2. Don't pay the ransom (encourages attackers)")
    print("  3. Report to authorities")
    print("  4. Restore from clean backups")
    
    print()
    print("-" * 50)
    print("Lab completed.")
    return True


if __name__ == "__main__":
    run()
