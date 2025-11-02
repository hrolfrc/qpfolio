# Configuration file for the Sphinx documentation builder.

project = 'bib-ami'
# noinspection PyShadowingBuiltins
copyright = '2025, Rolf Carlson'
author = 'Rolf Carlson'
release = '0.16.0'

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# Extensions
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',  # For Google-style docstrings
]

# Theme
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
