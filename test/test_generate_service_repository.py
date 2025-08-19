#!/usr/bin/env python3
"""
Test script for SPECTRA Service Repository Generator

This script tests the service repository generator functionality without actually
creating repositories or posting comments.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from generate_service_repository import ServiceRepositoryGenerator


def test_command_parsing():
    """Test slash command parsing."""
    print("🧪 Testing command parsing...")
    
    generator = ServiceRepositoryGenerator()
    
    test_cases = [
        {
            "comment": "/create-repo repoName=governancePolicy domain=governance visibility=private templateRepo=SPECTRADataSolutions/blueprint",
            "expected": {
                "repoName": "governancePolicy",
                "domain": "governance", 
                "visibility": "private",
                "templateRepo": "SPECTRADataSolutions/blueprint"
            }
        },
        {
            "comment": "/create-repo repoName=testRepo domain=testing visibility=public",
            "expected": {
                "repoName": "testRepo",
                "domain": "testing",
                "visibility": "public"
            }
        },
        {
            "comment": "This is just a regular comment with no command",
            "expected": None
        },
        {
            "comment": "Maybe /create-repo but malformed repoName=test",
            "expected": {
                "repoName": "test"
            }
        }
    ]
    
    for i, case in enumerate(test_cases):
        result = generator.parse_slash_command(case["comment"])
        
        if result == case["expected"]:
            print(f"  ✅ Test case {i+1}: PASS")
        else:
            print(f"  ❌ Test case {i+1}: FAIL")
            print(f"    Expected: {case['expected']}")
            print(f"    Got: {result}")
    
    print()


def test_parameter_validation():
    """Test parameter validation."""
    print("🧪 Testing parameter validation...")
    
    generator = ServiceRepositoryGenerator()
    
    test_cases = [
        {
            "params": {
                "repoName": "governancePolicy",
                "domain": "governance",
                "visibility": "private",
                "templateRepo": "SPECTRADataSolutions/blueprint"
            },
            "should_be_valid": True
        },
        {
            "params": {
                "repoName": "governance-policy",  # Invalid: has hyphen
                "domain": "governance",
                "visibility": "private"
            },
            "should_be_valid": False
        },
        {
            "params": {
                "repoName": "governancePolicy",
                "domain": "governance"
                # Missing visibility
            },
            "should_be_valid": False
        },
        {
            "params": {
                "repoName": "GovernancePolicy",  # Invalid: starts with uppercase
                "domain": "governance",
                "visibility": "private"
            },
            "should_be_valid": False
        },
        {
            "params": {
                "repoName": "governancePolicy",
                "domain": "governance",
                "visibility": "invalid_visibility"  # Invalid visibility
            },
            "should_be_valid": False
        },
        {
            "params": {
                "repoName": "governancePolicy",
                "domain": "governance",
                "visibility": "private",
                "templateRepo": "InvalidOrg/repo"  # Invalid template org
            },
            "should_be_valid": False
        }
    ]
    
    for i, case in enumerate(test_cases):
        valid, errors = generator.validate_command_params(case["params"])
        
        if valid == case["should_be_valid"]:
            print(f"  ✅ Test case {i+1}: PASS")
        else:
            print(f"  ❌ Test case {i+1}: FAIL")
            print(f"    Expected valid: {case['should_be_valid']}")
            print(f"    Got valid: {valid}")
            if errors:
                print(f"    Errors: {errors}")
    
    print()


def test_camel_case_validation():
    """Test camelCase validation specifically."""
    print("🧪 Testing camelCase validation...")
    
    generator = ServiceRepositoryGenerator()
    
    test_cases = [
        ("governancePolicy", True),
        ("governance", True),
        ("userInterface", True),
        ("a", True),
        ("governance-policy", False),
        ("governance_policy", False),
        ("GovernancePolicy", False),
        ("governance policy", False),
        ("governance.policy", False),
        ("governance/policy", False),
        ("123governance", False),
        ("", False)
    ]
    
    for text, expected in test_cases:
        result = generator._is_valid_camel_case(text)
        
        if result == expected:
            print(f"  ✅ '{text}': {result}")
        else:
            print(f"  ❌ '{text}': expected {expected}, got {result}")
    
    print()


def test_dry_run_repository_creation():
    """Test repository creation in dry-run mode."""
    print("🧪 Testing dry-run repository creation...")
    
    generator = ServiceRepositoryGenerator()
    
    params = {
        "repoName": "testRepo",
        "domain": "testing",
        "visibility": "private"
    }
    
    success, repo_url, warnings = generator.create_repository(params, dry_run=True)
    
    if success and repo_url == "https://github.com/SPECTRADataSolutions/testRepo":
        print("  ✅ Dry-run repository creation: PASS")
    else:
        print("  ❌ Dry-run repository creation: FAIL")
        print(f"    Success: {success}")
        print(f"    URL: {repo_url}")
        print(f"    Warnings: {warnings}")
    
    print()


def test_response_comment_formatting():
    """Test response comment formatting."""
    print("🧪 Testing response comment formatting...")
    
    generator = ServiceRepositoryGenerator()
    
    # Test success comment
    success = generator.post_response_comment(
        "SPECTRADataSolutions", ".github", 123,
        success=True, 
        repo_url="https://github.com/SPECTRADataSolutions/testRepo",
        warnings=["⚠️ Test warning"], 
        dry_run=True
    )
    
    if success:
        print("  ✅ Success comment formatting: PASS")
    else:
        print("  ❌ Success comment formatting: FAIL")
    
    # Test failure comment
    success = generator.post_response_comment(
        "SPECTRADataSolutions", ".github", 123,
        success=False,
        repo_url="",
        warnings=["❌ Test error"], 
        dry_run=True
    )
    
    if success:
        print("  ✅ Failure comment formatting: PASS")
    else:
        print("  ❌ Failure comment formatting: FAIL")
    
    print()


def main():
    """Run all tests."""
    print("🏗️ SPECTRA Service Repository Generator Test Suite")
    print("=" * 60)
    
    test_command_parsing()
    test_parameter_validation()
    test_camel_case_validation()
    test_dry_run_repository_creation()
    test_response_comment_formatting()
    
    print("🎉 Test suite completed!")


if __name__ == "__main__":
    main()