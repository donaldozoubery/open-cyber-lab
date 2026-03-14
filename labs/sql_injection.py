"""
SQL Injection Lab

Learn about SQL injection vulnerabilities and how to prevent them.

This lab demonstrates a classic SQL injection vulnerability where
user input is directly concatenated into SQL queries.

DISCLAIMER: This lab is for educational purposes only.
Always use parameterized queries in production code.
"""

DIFFICULTY = "Beginner"

OBJECTIVES = [
    "Understand what SQL injection is",
    "Learn how attackers exploit SQL injection",
    "Identify vulnerable code patterns",
    "Practice writing secure queries"
]

# Mock database (in-memory)
MOCK_USERS = {
    "admin": "admin123",
    "user": "password123",
    "guest": "guest"
}


def check_sql_injection(username: str) -> bool:
    """Check if the input contains SQL injection patterns.
    
    Args:
        username: The username input to check
        
    Returns:
        bool: True if SQL injection detected, False otherwise
    """
    injection_patterns = [
        "' OR '1'='1",
        "' OR '1'='1' --",
        "' OR '1'='1' /*",
        "admin' --",
        "admin' #",
        "' UNION SELECT",
        "'; DROP TABLE",
    ]
    
    username_lower = username.lower()
    for pattern in injection_patterns:
        if pattern.lower() in username_lower:
            return True
    
    return False


def validate_solution(username: str, password: str) -> dict:
    """Validate if the user successfully exploited the SQL injection.
    
    Args:
        username: The username provided
        password: The password provided
        
    Returns:
        dict: Result with success status and message
    """
    query = f"SELECT * FROM users WHERE name='{username}' AND password='{password}'"
    
    # Check for SQL injection attempts
    if check_sql_injection(username):
        return {
            "success": True,
            "message": "SQL Injection detected! You've successfully exploited the vulnerability.",
            "query": query
        }
    
    # Check for valid credentials
    if username in MOCK_USERS and MOCK_USERS[username] == password:
        return {
            "success": False,
            "message": "You used valid credentials. Try to bypass authentication using SQL injection!",
            "query": query
        }
    
    return {
        "success": False,
        "message": "Invalid credentials. Try using SQL injection to bypass authentication!",
        "query": query
    }


def run(*args):
    """Run the SQL Injection Lab."""
    print("=" * 50)
    print("         SQL INJECTION LAB")
    print("=" * 50)
    print()
    print("OBJECTIVES:")
    for i, obj in enumerate(OBJECTIVES, 1):
        print(f"  {i}. {obj}")
    print()
    print("-" * 50)
    print()
    print("This lab simulates a login form with a SQL injection vulnerability.")
    print("Your goal is to bypass authentication using SQL injection.")
    print()
    print("Try entering: admin' OR '1'='1")
    print()
    print("-" * 50)
    print()
    
    username = input("Username: ")
    password = input("Password: ")
    
    # Generate the vulnerable query
    query = f"SELECT * FROM users WHERE name='{username}' AND password='{password}'"
    
    print()
    print("Generated SQL query:")
    print(f"  {query}")
    print()
    
    # Validate the solution
    result = validate_solution(username, password)
    
    if result["success"]:
        print("=" * 50)
        print("  CONGRATULATIONS!")
        print("=" * 50)
        print()
        print(result["message"])
        print()
        print("EXPLANATION:")
        print("  The input 'admin' OR '1'='1' always evaluates to true,")
        print("  bypassing the password check entirely.")
        print()
        print("HOW TO PREVENT:")
        print("  - Use parameterized queries (prepared statements)")
        print("  - Use an ORM (Object-Relational Mapper)")
        print("  - Validate and sanitize user input")
        print("  - Apply the principle of least privilege")
    else:
        print("Keep trying! Hint: Try using OR '1'='1 in the username field.")
        print()
        print("TRY THIS:")
        print("  Username: admin' OR '1'='1' --")
        print("  Password: (leave empty)")
    
    print()
    print("-" * 50)
    print("Lab completed.")
    return True


if __name__ == "__main__":
    run()
