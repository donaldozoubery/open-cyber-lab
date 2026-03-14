"""
Insecure Direct Object Reference (IDOR) Lab

Learn about IDOR vulnerabilities and access control.

This lab demonstrates how attackers access unauthorized resources
by manipulating object references.

DISCLAIMER: This lab is for educational purposes only.
Never exploit IDOR without authorization.
"""

DIFFICULTY = "Intermediate"

OBJECTIVES = [
    "Understand what IDOR is",
    "Learn how attackers manipulate object references",
    "Understand proper authorization checks",
    "Practice secure resource handling"
]

from typing import Optional


# Simulated user database
USERS = {
    "user1": {"id": 1, "name": "Alice", "role": "user", "private_data": "Secret: My SSN is 123-45-6789"},
    "user2": {"id": 2, "name": "Bob", "role": "user", "private_data": "Secret: My credit card ends in 1234"},
    "admin": {"id": 3, "name": "Admin", "role": "admin", "private_data": "Admin panel access key: ADMIN_KEY_12345"},
}

# Current session
CURRENT_USER = {"id": 1, "username": "user1", "role": "user"}


def vulnerable_get_profile(user_id: int) -> dict:
    """Simulate vulnerable profile access.
    
    Args:
        user_id: User ID to access
        
    Returns:
        dict: User profile (or unauthorized)
    """
    # Vulnerable: No authorization check
    if user_id in USERS:
        user = USERS[user_id]
        return {
            "success": True,
            "user_id": user_id,
            "name": user["name"],
            "role": user["role"],
            "private_data": user["private_data"],
            "authorized": True,
            "vulnerable": True
        }
    
    return {
        "success": False,
        "error": "User not found",
        "vulnerable": True
    }


def secure_get_profile(user_id: int, current_user: dict) -> dict:
    """Simulate secure profile access with authorization.
    
    Args:
        user_id: User ID to access
        current_user: Currently authenticated user
        
    Returns:
        dict: User profile (or unauthorized)
    """
    # Secure: Check authorization
    # Users can only access their own profile
    # Admins can access any profile
    
    if current_user["role"] != "admin" and user_id != current_user["id"]:
        return {
            "success": False,
            "error": "Unauthorized: You can only access your own profile",
            "authorized": False,
            "vulnerable": False
        }
    
    # Check if user exists
    user_key = f"user{user_id}" if user_id <= 2 else "admin" if user_id == 3 else None
    
    if user_key and user_key in USERS:
        user = USERS[user_key]
        return {
            "success": True,
            "user_id": user_id,
            "name": user["name"],
            "role": user["role"],
            "private_data": user["private_data"],
            "authorized": True,
            "vulnerable": False
        }
    
    return {
        "success": False,
        "error": "User not found",
        "authorized": False,
        "vulnerable": False
    }


def check_authorization(user_id: int, current_user_id: int, current_role: str) -> bool:
    """Check if access is authorized.
    
    Args:
        user_id: Target user ID
        current_user_id: Current user ID
        current_role: Current user role
        
    Returns:
        bool: True if authorized
    """
    # Admins can access any user
    if current_role == "admin":
        return True
    
    # Users can only access their own profile
    return user_id == current_user_id


def run(*args):
    """Run the IDOR Lab."""
    print("=" * 50)
    print("     INSECURE DIRECT OBJECT REFERENCE LAB")
    print("=" * 50)
    print()
    print("OBJECTIVES:")
    for i, obj in enumerate(OBJECTIVES, 1):
        print(f"  {i}. {obj}")
    print()
    print("-" * 50)
    print()
    
    print("SCENARIO:")
    print("  A user profile API that allows accessing user data")
    print("  without proper authorization checks.")
    print()
    print(f"  Current user: {CURRENT_USER['username']} (ID: {CURRENT_USER['id']})")
    print()
    
    print("-" * 50)
    print()
    
    print("USER DATABASE:")
    for key, user in USERS.items():
        print(f"  ID {user['id']}: {user['name']} ({user['role']})")
    print()
    
    print("OPTIONS:")
    print("  1. Vulnerable profile access (no auth)")
    print("  2. Secure profile access (with auth)")
    print("  3. Test as admin")
    print()
    
    choice = input("Choose (1-3): ")
    
    if choice == "1":
        print("\n--- Vulnerable Profile Access ---")
        print("Vulnerable code:")
        print("  user_id = request.params['user_id']")
        print("  return db.get_user(user_id)  # No check!")
        print()
        
        target_id = input("Enter user ID to access (1-3): ")
        
        try:
            user_id = int(target_id)
            result = vulnerable_get_profile(user_id)
            
            if result["success"]:
                print(f"\n✓ Accessed user: {result['name']}")
                print(f"  Role: {result['role']}")
                print(f"  Private data: {result['private_data']}")
                print(f"\n⚠️  VULNERABLE: You accessed another user's data!")
            else:
                print(f"\n✗ {result['error']}")
                
        except ValueError:
            print("Invalid input")
            
    elif choice == "2":
        print("\n--- Secure Profile Access ---")
        print("Secure code:")
        print("  if current_user.role != 'admin' and user_id != current_user.id:")
        print("      return 'Unauthorized'")
        print()
        
        target_id = input("Enter user ID to access (1-3): ")
        
        try:
            user_id = int(target_id)
            result = secure_get_profile(user_id, CURRENT_USER)
            
            if result["success"]:
                print(f"\n✓ Accessed user: {result['name']}")
                print(f"  Role: {result['role']}")
                print(f"  Private data: {result['private_data']}")
            else:
                print(f"\n✗ {result['error']}")
                
        except ValueError:
            print("Invalid input")
            
    elif choice == "3":
        print("\n--- Test as Admin ---")
        
        global CURRENT_USER
        CURRENT_USER = {"id": 3, "username": "admin", "role": "admin"}
        
        print(f"Current user: {CURRENT_USER['username']} (ID: {CURRENT_USER['id']}, Role: {CURRENT_USER['role']})")
        print()
        
        target_id = input("Enter user ID to access (1-3): ")
        
        try:
            user_id = int(target_id)
            result = secure_get_profile(user_id, CURRENT_USER)
            
            if result["success"]:
                print(f"\n✓ Accessed user: {result['name']}")
                print(f"  Role: {result['role']}")
                print(f"  Private data: {result['private_data']}")
            else:
                print(f"\n✗ {result['error']}")
                
        except ValueError:
            print("Invalid input")
            
    else:
        print("Invalid choice.")
        return False
    
    print()
    print("-" * 50)
    print()
    print("KEY TAKEAWAYS:")
    print("  - Always verify user authorization before access")
    print("  - Don't rely only on user IDs in URLs")
    print("  - Use indirect object references when possible")
    print("  - Implement proper access control checks")
    print("  - Log all access attempts")
    print("  - Use framework-provided auth mechanisms")
    
    print()
    print("-" * 50)
    print("Lab completed.")
    return True


if __name__ == "__main__":
    run()
