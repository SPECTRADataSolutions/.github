#!/usr/bin/env python3
"""
Test script for the language style enforcement script.
"""

import sys
import os
import tempfile
import subprocess
from pathlib import Path

# Add the scripts directory to the path so we can import the module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from enforceLanguageStyle import scanRepositoryText, loadRepositoryFiles, reportStyleViolations

def test_language_style_enforcement():
    """Test the language style enforcement functionality."""
    print("🧪 Testing language style enforcement...")
    
    # Create test cases
    test_cases = [
        {
            "content": "The org is important",
            "should_violate": True,
            "description": "standalone org"
        },
        {
            "content": "Visit example.org for details",
            "should_violate": False,
            "description": ".org domain"
        },
        {
            "content": "Check https://github.org/repo",
            "should_violate": False,
            "description": "URL with .org"
        },
        {
            "content": "Use the org.json file",
            "should_violate": False,
            "description": "org followed by dot"
        },
        {
            "content": "Contact the dept for more info",
            "should_violate": True,
            "description": "dept and info violations"
        },
        {
            "content": "The organisation is great",
            "should_violate": False,
            "description": "full word organisation"
        },
        {
            "content": 'do not abbreviate "organisation" to "org"',
            "should_violate": False,
            "description": "org in quotes as example"
        },
        {
            "content": "scopes: repo, admin:org",
            "should_violate": False,
            "description": "org after colon (technical parameter)"
        },
        {
            "content": "The 'org' should not be used",
            "should_violate": False,
            "description": "org in single quotes"
        }
    ]
    
    # Test each case
    for i, case in enumerate(test_cases):
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.md"
            test_file.write_text(case["content"])
            
            files = [test_file]
            violations = scanRepositoryText(files)
            
            has_violations = len(violations) > 0
            
            if has_violations == case["should_violate"]:
                print(f"  ✅ Test case {i+1} ({case['description']}): PASS")
            else:
                print(f"  ❌ Test case {i+1} ({case['description']}): FAIL")
                print(f"    Expected violations: {case['should_violate']}, Got: {has_violations}")
                if violations:
                    for path, line, segment, preferred in violations:
                        print(f"    Violation: {segment} -> {preferred}")
    
    print()

def test_script_execution():
    """Test that the script runs correctly as a command."""
    print("🧪 Testing script execution...")
    
    # Test with no violations (create a clean file)
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = Path(tmpdir) / "clean.md"
        test_file.write_text("# Clean Document\n\nThis is a clean organisation document.")
        
        # Change to the temp directory and run the script
        os.chdir(tmpdir)
        result = subprocess.run([sys.executable, "/home/runner/work/.github/.github/scripts/enforceLanguageStyle.py"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("  ✅ Script execution with clean file: PASS")
        else:
            print("  ❌ Script execution with clean file: FAIL")
            print(f"    Return code: {result.returncode}")
            print(f"    Output: {result.stdout}")
            print(f"    Error: {result.stderr}")
    
    # Test with violations
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = Path(tmpdir) / "dirty.md"
        test_file.write_text("# Dirty Document\n\nThe org needs attention.")
        
        os.chdir(tmpdir)
        result = subprocess.run([sys.executable, "/home/runner/work/.github/.github/scripts/enforceLanguageStyle.py"], 
                              capture_output=True, text=True)
        
        if result.returncode == 1 and "org" in result.stderr:
            print("  ✅ Script execution with violations: PASS")
        else:
            print("  ❌ Script execution with violations: FAIL")
            print(f"    Return code: {result.returncode}")
            print(f"    Output: {result.stdout}")
            print(f"    Error: {result.stderr}")
    
    print()

def main():
    print("🧪 Language Style Guard Test Suite")
    print("=" * 50)
    
    test_language_style_enforcement()
    test_script_execution()
    
    print("✅ Test suite completed!")

if __name__ == "__main__":
    main()