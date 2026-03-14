"""
Command Injection Lab

Learn about OS command injection vulnerabilities.

This lab demonstrates how attackers execute arbitrary
commands through vulnerable input fields.

DISCLAIMER: This lab is for educational purposes only.
Never exploit command injection without authorization.
"""

DIFFICULTY = "Advanced"

OBJECTIVES = [
    "Understand command injection vulnerabilities",
    "Learn command chaining techniques",
    "Identify vulnerable code patterns",
    "Practice secure input handling"
]



# Simulated system commands
AVAILABLE_COMMANDS = {
    "ping": "Pinging 127.0.0.1...",
    "nslookup": "Server: dns.google\nAddress: 8.8.8.8",
    "traceroute": " 1  router.local (192.168.1.1)  1.234 ms",
}


def vulnerable_command_execution(user_input: str) -> dict:
    """Simulate vulnerable command execution.
    
    Args:
        user_input: User-provided input
        
    Returns:
        dict: Execution result
    """
    # Vulnerable: Directly using user input in shell command
    command = f"echo {user_input}"
    
    try:
        # For demo, simulate the output
        output = f"Output: {user_input}"
        
        return {
            "success": True,
            "command": command,
            "output": output,
            "vulnerable": True,
            "injection_possible": True
        }
        
    except Exception as e:
        return {
            "success": False,
            "command": command,
            "error": str(e),
            "vulnerable": True
        }


def simulate_command_injection(user_input: str) -> dict:
    """Simulate successful command injection.
    
    Args:
        user_input: User input with injection
        
    Returns:
        dict: Injection result
    """
    # Detect if input contains command injection
    dangerous_patterns = [
        ";", "&&", "||", "|", "&", "$", "`", "$(", ">", "<", "\n"
    ]
    
    is_injection = any(pattern in user_input for pattern in dangerous_patterns)
    
    if is_injection:
        return {
            "success": True,
            "injection_detected": True,
            "original_command": "echo user_input",
            "injected_commands": user_input,
            "output": "Command injection successful!",
            "can_execute_arbitrary": True
        }
    
    return {
        "success": False,
        "injection_detected": False,
        "original_command": "echo user_input",
        "output": "Normal execution"
    }


def secure_command_execution(user_input: str) -> dict:
    """Simulate secure command execution.
    
    Args:
        user_input: User-provided input
        
    Returns:
        dict: Execution result
    """
    # Secure: Use allowlist and avoid shell=True
    allowed_commands = ["ping", "nslookup", "traceroute"]
    
    # Validate input against allowlist
    if user_input not in allowed_commands:
        return {
            "success": False,
            "error": "Invalid command. Allowed: ping, nslookup, traceroute",
            "vulnerable": False
        }
    
    # Use list form, not string (prevents injection)
    try:
        # Simulated execution
        output = AVAILABLE_COMMANDS.get(user_input, "Command executed")
        
        return {
            "success": True,
            "command": user_input,
            "output": output,
            "vulnerable": False
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "vulnerable": False
        }


def detect_injection(input_text: str) -> bool:
    """Detect potential command injection.
    
    Args:
        input_text: Input to check
        
    Returns:
        bool: True if potential injection detected
    """
    dangerous_chars = [";", "&", "|", "`", "$", ">", "<", "\n", "\r"]
    
    return any(char in input_text for char in dangerous_chars)


def validate_solution(user_input: str, secure: bool = False) -> dict:
    """Validate the solution.
    
    Args:
        user_input: User input
        secure: Whether using secure method
        
    Returns:
        dict: Validation result
    """
    has_injection = detect_injection(user_input)
    
    if secure:
        if has_injection:
            return {
                "success": True,
                "message": "Attack blocked! Input validation caught the injection attempt."
            }
        return {
            "success": True,
            "message": "Normal input processed securely."
        }
    
    if has_injection:
        return {
            "success": True,
            "message": "Command injection successful! You executed arbitrary commands."
        }
    
    return {
        "success": False,
        "message": "No injection detected. Try using ; or && to chain commands."
    }


def run(*args):
    """Run the Command Injection Lab."""
    print("=" * 50)
    print("       COMMAND INJECTION LAB")
    print("=" * 50)
    print()
    print("OBJECTIVES:")
    for i, obj in enumerate(OBJECTIVES, 1):
        print(f"  {i}. {obj}")
    print()
    print("-" * 50)
    print()
    
    print("SCENARIO:")
    print("  A network diagnostic tool that takes user input")
    print("  and passes it to a system shell without proper sanitization.")
    print()
    
    print("-" * 50)
    print()
    
    print("OPTIONS:")
    print("  1. Vulnerable execution (shell=True)")
    print("  2. Secure execution (allowlist)")
    print("  3. Test payloads")
    print()
    
    choice = input("Choose (1-3): ")
    
    if choice == "1":
        print("\n--- Vulnerable Execution ---")
        print("Vulnerable code:")
        print('  command = "ping -c 1 " + user_input')
        print('  os.system(command)  # DANGEROUS!')
        print()
        
        user_input = input("Enter hostname or IP: ")
        
        result = vulnerable_command_execution(user_input)
        
        print(f"\nCommand: {result['command']}")
        print(f"Output: {result['output']}")
        
        injection = simulate_command_injection(user_input)
        if injection["injection_detected"]:
            print("\n⚠️  Command injection detected!")
            print(f"  Injected: {injection['injected_commands']}")
        
        validation = validate_solution(user_input, secure=False)
        
    elif choice == "2":
        print("\n--- Secure Execution ---")
        print("Secure code:")
        print('  allowed = ["ping", "nslookup", "traceroute"]')
        print('  if user_input not in allowed:')
        print('      raise ValueError("Invalid input")')
        print('  subprocess.run([command], shell=False)')
        print()
        
        user_input = input("Enter command (ping/nslookup/traceroute): ")
        
        result = secure_command_execution(user_input)
        
        if result["success"]:
            print(f"\n✓ Command executed: {result['command']}")
            print(f"Output: {result['output']}")
        else:
            print(f"\n✗ {result['error']}")
        
        validation = validate_solution(user_input, secure=True)
        
    elif choice == "3":
        print("\n--- Common Payloads ---")
        
        payloads = [
            "google.com",
            "google.com; whoami",
            "google.com && cat /etc/passwd",
            "google.com | ls -la",
            "google.com`whoami`",
            "$(whoami)",
            "google.com > /tmp/output",
            "127.0.0.1\ncat /etc/passwd",
        ]
        
        print("\nPayloads to try:")
        for i, payload in enumerate(payloads, 1):
            detection = "✓" if detect_injection(payload) else "✗"
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
    print("  - Never pass unsanitized user input to system commands")
    print("  - Use allowlists instead of blocklists")
    print("  - Use subprocess with shell=False and list arguments")
    print("  - Validate and escape all input")
    print("  - Run with minimal privileges")
    print("  - Consider using APIs instead of shell commands")
    
    print()
    print("SECURE ALTERNATIVES:")
    print("  - Use programming language APIs instead of shell")
    print("  - Use libraries for specific tasks")
    print("  - Implement input validation")
    print("  - Use sandboxing if shell is necessary")
    
    print()
    print("-" * 50)
    print("Lab completed.")
    return True


if __name__ == "__main__":
    run()
