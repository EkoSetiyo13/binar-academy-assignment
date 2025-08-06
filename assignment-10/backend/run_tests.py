#!/usr/bin/env python3
"""
Test runner script for Assignment 10
Runs comprehensive tests with coverage reporting
"""

import subprocess
import sys
import os

def run_tests():
    """Run tests with coverage"""
    print("🧪 Running Assignment 10 Tests with Coverage...")
    print("=" * 50)
    
    # Install test dependencies if needed
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements-test.txt"], 
                      check=True, capture_output=True)
        print("✅ Test dependencies installed")
    except subprocess.CalledProcessError:
        print("⚠️  Some test dependencies may not be installed")
    
    # Run tests with coverage
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest",
            "--cov=app",
            "--cov-report=html",
            "--cov-report=term-missing",
            "--cov-fail-under=90",
            "-v",
            "tests/"
        ], capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        if result.returncode == 0:
            print("\n🎉 All tests passed with 90%+ coverage!")
            print("📊 Coverage report generated in htmlcov/index.html")
        else:
            print(f"\n❌ Tests failed with return code {result.returncode}")
            return False
            
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False
    
    return True

def show_coverage_summary():
    """Show coverage summary"""
    print("\n📈 Coverage Summary:")
    print("=" * 30)
    
    try:
        # Read coverage report
        with open("htmlcov/index.html", "r") as f:
            content = f.read()
            
        # Extract coverage percentage (simple parsing)
        if "coverage" in content.lower():
            print("✅ Coverage report generated successfully")
            print("📁 Open htmlcov/index.html in your browser to view detailed coverage")
        else:
            print("⚠️  Coverage report may not be complete")
            
    except FileNotFoundError:
        print("❌ Coverage report not found")

if __name__ == "__main__":
    print("🚀 Assignment 10 - AI-Assisted Unit Testing")
    print("=" * 50)
    
    success = run_tests()
    show_coverage_summary()
    
    if success:
        print("\n✅ Assignment 10 completed successfully!")
        print("📝 Ready for submission")
    else:
        print("\n❌ Assignment 10 failed")
        sys.exit(1) 