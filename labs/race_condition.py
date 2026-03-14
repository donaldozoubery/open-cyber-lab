"""
Race Condition (TOCTOU) Lab

Learn about Time-of-Check-Time-of-Use vulnerabilities.

This lab demonstrates race condition vulnerabilities
where timing affects security decisions.

DISCLAIMER: This lab is for educational purposes only.
Never exploit race conditions without authorization.
"""

DIFFICULTY = "Advanced"

OBJECTIVES = [
    "Understand race conditions and TOCTOU",
    "Learn how attackers exploit timing vulnerabilities",
    "Identify vulnerable code patterns",
    "Practice atomic operations"
]

import time
import threading
from typing import Optional


# Simulated bank account
BANK_ACCOUNTS = {
    "alice": {"balance": 1000, "locked": False},
    "bob": {"balance": 500, "locked": False},
}


def vulnerable_transfer(from_user: str, to_user: str, amount: int) -> dict:
    """Simulate vulnerable transfer with TOCTOU.
    
    Args:
        from_user: Source account
        to_user: Destination account
        amount: Amount to transfer
        
    Returns:
        dict: Transfer result
    """
    # VULNERABLE: Time-of-check-time-of-use
    
    # Step 1: Check balance (TOCTOU window starts)
    if BANK_ACCOUNTS[from_user]["balance"] < amount:
        return {"success": False, "error": "Insufficient funds"}
    
    # WINDOW: Attacker can manipulate between check and use
    # Add artificial delay to simulate the vulnerability
    time.sleep(0.1)  # Simulates network/processing delay
    
    # Step 2: Perform transfer (TOCTOU window ends)
    BANK_ACCOUNTS[from_user]["balance"] -= amount
    BANK_ACCOUNTS[to_user]["balance"] += amount
    
    return {
        "success": True,
        "message": f"Transferred {amount} from {from_user} to {to_user}",
        "from_balance": BANK_ACCOUNTS[from_user]["balance"],
        "to_balance": BANK_ACCOUNTS[to_user]["balance"]
    }


def secure_transfer(from_user: str, to_user: str, amount: int) -> dict:
    """Simulate secure transfer with locking.
    
    Args:
        from_user: Source account
        to_user: Destination account
        amount: Amount to transfer
        
    Returns:
        dict: Transfer result
    """
    # SECURE: Use atomic operations/locking
    
    # Lock both accounts
    if BANK_ACCOUNTS[from_user]["locked"] or BANK_ACCOUNTS[to_user]["locked"]:
        return {"success": False, "error": "Accounts locked"}
    
    BANK_ACCOUNTS[from_user]["locked"] = True
    BANK_ACCOUNTS[to_user]["locked"] = True
    
    try:
        # Check and use in same atomic operation
        if BANK_ACCOUNTS[from_user]["balance"] < amount:
            return {"success": False, "error": "Insufficient funds"}
        
        # Perform transfer atomically
        BANK_ACCOUNTS[from_user]["balance"] -= amount
        BANK_ACCOUNTS[to_user]["balance"] += amount
        
        return {
            "success": True,
            "message": f"Transferred {amount} from {from_user} to {to_user}",
            "from_balance": BANK_ACCOUNTS[from_user]["balance"],
            "to_balance": BANK_ACCOUNTS[to_user]["balance"]
        }
    finally:
        # Always unlock
        BANK_ACCOUNTS[from_user]["locked"] = False
        BANK_ACCOUNTS[to_user]["locked"] = False


def simulate_race_attack(from_user: str, amount: int) -> dict:
    """Simulate race condition attack.
    
    Args:
        from_user: Source account
        amount: Amount for each transfer
        
    Returns:
        dict: Attack result
    """
    results = []
    
    # Create multiple threads to exploit race
    threads = []
    for _ in range(5):
        t = threading.Thread(target=lambda: results.append(vulnerable_transfer(from_user, "bob", amount)))
        threads.append(t)
    
    # Start all threads simultaneously
    for t in threads:
        t.start()
    
    # Wait for all to complete
    for t in threads:
        t.join()
    
    success_count = sum(1 for r in results if r["success"])
    
    return {
        "attack_successful": success_count > 1,
        "successful_transfers": success_count,
        "initial_balance": 1000,
        "final_balance": BANK_ACCOUNTS[from_user]["balance"],
        "message": f"Original: 1000, Final: {BANK_ACCOUNTS[from_user]['balance']}"
    }


def run(*args):
    """Run the Race Condition Lab."""
    print("=" * 50)
    print("      RACE CONDITION (TOCTOU) LAB")
    print("=" * 50)
    print()
    print("OBJECTIVES:")
    for i, obj in enumerate(OBJECTIVES, 1):
        print(f"  {i}. {obj}")
    print()
    print("-" * 50)
    print()
    
    # Reset accounts
    global BANK_ACCOUNTS
    BANK_ACCOUNTS = {
        "alice": {"balance": 1000, "locked": False},
        "bob": {"balance": 500, "locked": False},
    }
    
    print("SCENARIO:")
    print("  A banking system where attackers exploit timing")
    print("  to transfer more money than they have.")
    print()
    
    print(f"Initial: Alice={BANK_ACCOUNTS['alice']['balance']}, Bob={BANK_ACCOUNTS['bob']['balance']}")
    print()
    
    print("-" * 50)
    print()
    
    print("OPTIONS:")
    print("  1. Vulnerable transfer (no locking)")
    print("  2. Secure transfer (with locking)")
    print("  3. Race condition attack simulation")
    print()
    
    choice = input("Choose (1-3): ")
    
    if choice == "1":
        print("\n--- Vulnerable Transfer ---")
        
        amount = int(input("Amount to transfer: "))
        result = vulnerable_transfer("alice", "bob", amount)
        
        if result["success"]:
            print(f"\n✓ {result['message']}")
            print(f"Alice: {result['from_balance']}, Bob: {result['to_balance']}")
        else:
            print(f"\n✗ {result['error']}")
        
    elif choice == "2":
        print("\n--- Secure Transfer ---")
        
        amount = int(input("Amount to transfer: "))
        result = secure_transfer("alice", "bob", amount)
        
        if result["success"]:
            print(f"\n✓ {result['message']}")
            print(f"Alice: {result['from_balance']}, Bob: {result['to_balance']}")
        else:
            print(f"\n✗ {result['error']}")
        
    elif choice == "3":
        print("\n--- Race Condition Attack ---")
        print("Attempting to transfer 300 (5 threads, 300 each)")
        print("But Alice only has 1000!")
        print()
        
        result = simulate_race_attack("alice", 300)
        
        print(f"\nSuccessful transfers: {result['successful_transfers']}")
        print(f"Message: {result['message']}")
        
        if result["attack_successful"]:
            print("\n⚠️  RACE CONDITION EXPLOITED!")
            print("  Multiple transfers succeeded despite insufficient funds!")
        
    else:
        print("Invalid choice.")
        return False
    
    print()
    print("-" * 50)
    print()
    print("KEY TAKEAWAYS:")
    print("  - Use atomic operations")
    print("  - Implement proper locking mechanisms")
    print("  - Minimize TOCTOU windows")
    print("  - Use database transactions")
    print("  - Implement idempotency")
    print("  - Validate at the last possible moment")
    
    print()
    print("-" * 50)
    print("Lab completed.")
    return True


if __name__ == "__main__":
    run()
