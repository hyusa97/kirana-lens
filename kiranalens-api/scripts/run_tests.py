#!/usr/bin/env python3
"""
Test runner script for KiranaLens API

Runs demo data seeding followed by smoke tests.

Usage:
    python scripts/run_tests.py [--skip-seed]
"""
import asyncio
import subprocess
import sys
import time
from pathlib import Path

import httpx
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

BASE_URL = "http://localhost:8000"
TIMEOUT = 5.0


async def check_api_server():
    """Check if API server is running"""
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.get(f"{BASE_URL}/health")
            return response.status_code == 200
    except Exception:
        return False


def run_script(script_name: str, description: str) -> bool:
    """Run a Python script and return success status"""
    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{description}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    
    try:
        result = subprocess.run(
            [sys.executable, f"scripts/{script_name}"],
            cwd=Path(__file__).parent.parent,
            check=True,
            capture_output=False
        )
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}❌ Script failed with exit code {e.returncode}{Style.RESET_ALL}")
        return False
    except Exception as e:
        print(f"{Fore.RED}❌ Error running script: {e}{Style.RESET_ALL}")
        return False


async def main():
    """Main test runner"""
    skip_seed = "--skip-seed" in sys.argv
    
    print(f"{Fore.GREEN}🚀 KiranaLens API Test Runner{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Target: {BASE_URL}{Style.RESET_ALL}")
    
    # Check if API server is running
    print(f"\n{Fore.YELLOW}🔍 Checking API server...{Style.RESET_ALL}")
    if not await check_api_server():
        print(f"{Fore.RED}❌ API server is not running at {BASE_URL}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}💡 Start the server with: python main.py{Style.RESET_ALL}")
        sys.exit(1)
    
    print(f"{Fore.GREEN}✅ API server is running{Style.RESET_ALL}")
    
    success_count = 0
    total_count = 2 if not skip_seed else 1
    
    # Run demo data seeding
    if not skip_seed:
        if run_script("seed_demo_data.py", "🌱 SEEDING DEMO DATA"):
            success_count += 1
            print(f"{Fore.GREEN}✅ Demo data seeding completed{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}❌ Demo data seeding failed{Style.RESET_ALL}")
        
        # Wait a moment for database to settle
        print(f"{Fore.YELLOW}⏳ Waiting 2 seconds for database to settle...{Style.RESET_ALL}")
        time.sleep(2)
    else:
        print(f"{Fore.YELLOW}⏭️  Skipping demo data seeding{Style.RESET_ALL}")
    
    # Run smoke tests
    if run_script("smoke_test.py", "🧪 RUNNING SMOKE TESTS"):
        success_count += 1
        print(f"{Fore.GREEN}✅ Smoke tests completed{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}❌ Smoke tests failed{Style.RESET_ALL}")
    
    # Final summary
    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    if success_count == total_count:
        print(f"{Fore.GREEN}🎉 ALL TESTS COMPLETED SUCCESSFULLY!{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{success_count}/{total_count} scripts passed{Style.RESET_ALL}")
        exit_code = 0
    else:
        print(f"{Fore.RED}❌ SOME TESTS FAILED{Style.RESET_ALL}")
        print(f"{Fore.RED}{success_count}/{total_count} scripts passed{Style.RESET_ALL}")
        exit_code = 1
    
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    
    if exit_code == 0:
        print(f"\n{Fore.GREEN}🚀 Your KiranaLens API is ready for development!{Style.RESET_ALL}")
        print(f"{Fore.CYAN}📖 API Documentation: {BASE_URL}/docs{Style.RESET_ALL}")
        print(f"{Fore.CYAN}👤 Demo Login: demo@kiranalens.com / Demo@1234{Style.RESET_ALL}")
    
    sys.exit(exit_code)


if __name__ == "__main__":
    # Check dependencies
    try:
        import colorama
        import httpx
    except ImportError as e:
        print(f"Missing dependency: {e}")
        print("Installing required packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "colorama", "httpx"])
        import colorama
        import httpx
        colorama.init(autoreset=True)
    
    asyncio.run(main())