"""
Main entry point for the Sales Chatbot application.
"""

from sales_chatbot.tools.df_tools import tools
from sales_chatbot.app import create_app

def main():
    """Main entry point for the application."""
    app = create_app()
    app.run(debug=True)

if __name__ == "__main__":
    main() 