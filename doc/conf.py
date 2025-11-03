import os
import sys
from datetime import datetime

# noinspection PyShadowingBuiltins
project = "qpfolio"
author = "Rolf Carlson"
copyright = f"{datetime.now():%Y}, {author}"
release = "0.1.7"

sys.path.insert(0, os.path.abspath(".."))

extensions = [
    "sphinx.ext.autodoc",
    'sphinx.ext.viewcode',
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",
]

html_theme = "furo"
templates_path = ["_templates"]
html_static_path = ['_static']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

autodoc_default_options = {"members": True, "undoc-members": True}
