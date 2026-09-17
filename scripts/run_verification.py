import os
from verification.sampler import sample_apps
from verification.manual_checker import run_verification

def main():
    print("Running Verification Loop...")
    sample_apps()
    run_verification()
    
if __name__ == "__main__":
    main()
