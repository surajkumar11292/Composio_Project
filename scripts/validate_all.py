import pytest
import sys

def main():
    print("Running all phase validations...")
    result = pytest.main(["-v", "--tb=short", "tests/"])
    if result != 0:
        print("\n[X] Validation failed. Please fix the errors before committing.")
        sys.exit(1)
    else:
        print("\n[OK] All validations passed.")
        sys.exit(0)

if __name__ == "__main__":
    main()
