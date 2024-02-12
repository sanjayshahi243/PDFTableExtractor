# docs/conf.py

import os
import sys

sys.path.insert(0, os.path.abspath(".."))

# Add extensions
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",  # For parsing Google-style docstrings
]

# Add napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = False

# Set the master doc file
master_doc = "pdfExtractor"

# Additional configuration options...
