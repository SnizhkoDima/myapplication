import os
import sys
sys.path.insert(0, os.path.abspath('../..'))

project = 'myapplication'
copyright = '2025, Snizhko Dmytro'
author = 'Snizhko Dmytro'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc']


templates_path = ['_templates']
exclude_patterns = []

language = 'uk'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
