"""
Simple test script to run the banking system console application.
This script adds the parent directory to the Python path to allow imports.
"""

import sys
import os

# Add the parent directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.ui.console_app import ConsoleApp


def main():
    """Run the banking system console application."""
    app = ConsoleApp()
    app.run()


if __name__ == "__main__":
    main()
