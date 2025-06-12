import os
import sys
sys.path.insert(0, os.path.abspath('../..'))  # додає корінь проєкту до PYTHONPATH

project = 'myapplication'
copyright = '2025, Автор'
author = 'Автор'

extensions = ['sphinx.ext.autodoc']

templates_path = ['_templates']
exclude_patterns = []

html_theme = 'alabaster'
html_static_path = ['_static']
