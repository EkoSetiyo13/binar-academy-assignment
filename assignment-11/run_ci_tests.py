#!/usr/bin/env python3
"""
CI Test Runner for Assignment 11
Runs all tests locally to simulate CI/CD pipeline
"""

import subprocess
import sys
import os
import time
from pathlib import Path

def run_command(command, cwd=None, description=""):
    """Run a command and return success status"""
    print(f"\n🔧 {description}")
    print(f"Running: {command}")
    print("=" * 50)
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True
        )
        
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
            
        if result.returncode == 0:
            print(f"✅ {description} - SUCCESS")
            return True
        else:
            print(f"❌ {description} - FAILED (exit code: {result.returncode})")
            return False
            
    except Exception as e:
        print(f"❌ {description} - ERROR: {e}")
        return False

def check_coverage():
    """Check if coverage meets requirements"""
    print("\n📊 Coverage Analysis")
    print("=" * 50)
    
    # Backend coverage check
    backend_success = run_command(
        "pytest --cov=app --cov-report=term-missing --cov-fail-under=90 -v tests/",
        cwd="backend",
        description="Backend Coverage Test (90%+)"
    )
    
    # Frontend coverage check (if npm test is available)
    frontend_success = True
    if os.path.exists("frontend/package.json"):
        frontend_success = run_command(
            "npm test -- --coverage --watchAll=false --passWithNoTests",
            cwd="frontend",
            description="Frontend Coverage Test (80%+)"
        )
    
    return backend_success and frontend_success

def run_security_scan():
    """Run security scanning"""
    print("\n🔒 Security Scanning")
    print("=" * 50)
    
    # Install bandit if not available
    run_command("pip install bandit", description="Installing Bandit")
    
    # Run security scan
    security_success = run_command(
        "bandit -r app/ -f json -o bandit-report.json",
        cwd="backend",
        description="Security Scan (Bandit)"
    )
    
    return security_success

def run_code_quality():
    """Run code quality checks"""
    print("\n📝 Code Quality Checks")
    print("=" * 50)
    
    # Install quality tools
    run_command("pip install black isort flake8", description="Installing Quality Tools")
    
    # Run formatting check
    formatting_success = run_command(
        "black --check app/ tests/",
        cwd="backend",
        description="Code Formatting Check (Black)"
    )
    
    # Run import sorting check
    import_success = run_command(
        "isort --check-only app/ tests/",
        cwd="backend",
        description="Import Sorting Check (isort)"
    )
    
    # Run linting
    linting_success = run_command(
        "flake8 app/ tests/ --max-line-length=88 --extend-ignore=E203,W503",
        cwd="backend",
        description="Code Linting (flake8)"
    )
    
    return formatting_success and import_success and linting_success

def run_integration_tests():
    """Run integration tests"""
    print("\n🔗 Integration Tests")
    print("=" * 50)
    
    integration_success = run_command(
        "pytest tests/test_integration.py -v",
        cwd="backend",
        description="Integration Tests"
    )
    
    return integration_success

def generate_report():
    """Generate test report"""
    print("\n📈 Test Report")
    print("=" * 50)
    
    report = {
        "coverage": check_coverage(),
        "security": run_security_scan(),
        "quality": run_code_quality(),
        "integration": run_integration_tests()
    }
    
    print("\n🎯 Final Results")
    print("=" * 50)
    
    for test_name, success in report.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name.upper()}: {status}")
    
    all_passed = all(report.values())
    
    if all_passed:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Coverage requirements met")
        print("✅ Security scan clean")
        print("✅ Code quality standards met")
        print("✅ Integration tests passed")
        print("\n🚀 Ready for CI/CD deployment!")
    else:
        print("\n⚠️  SOME TESTS FAILED")
        print("Please fix the issues before proceeding")
        sys.exit(1)
    
    return all_passed

def main():
    """Main function"""
    print("🚀 Assignment 11 - CI/CD Test Runner")
    print("=" * 50)
    print("This script simulates the CI/CD pipeline locally")
    print("Running all tests and quality checks...")
    
    # Check if we're in the right directory
    if not os.path.exists("backend") or not os.path.exists("frontend"):
        print("❌ Error: Please run this script from the assignment-11 directory")
        sys.exit(1)
    
    # Install dependencies
    print("\n📦 Installing Dependencies")
    print("=" * 50)
    
    # Backend dependencies
    run_command(
        "pip install -r requirements.txt -r requirements-test.txt",
        cwd="backend",
        description="Installing Backend Dependencies"
    )
    
    # Frontend dependencies (if available)
    if os.path.exists("frontend/package.json"):
        run_command(
            "npm install",
            cwd="frontend",
            description="Installing Frontend Dependencies"
        )
    
    # Run all tests
    success = generate_report()
    
    if success:
        print("\n📋 Next Steps:")
        print("1. Push to GitHub to trigger CI/CD pipeline")
        print("2. Set up CodeCov integration")
        print("3. Configure GitHub Secrets for notifications")
        print("4. Monitor pipeline status in GitHub Actions")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main()) 