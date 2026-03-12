"""
Main entry point for the Banking System backend.
"""

from backend.ui.console_app import ConsoleApp


def main():
    """Run the banking system console application."""
    app = ConsoleApp()
    app.run()


if __name__ == "__main__":
    main()
