"""
PDFExtractor Application Entry Point.

This module serves as the entry point for the PDFExtractor Flask application.

Usage:
- Run this script to start the development server.
"""

from pdfExtractor import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
