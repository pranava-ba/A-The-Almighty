"""Sphinx configuration for the Quant Portfolio docs (MyST Markdown, RTD theme).

Build model (a): these pages are pre-rendered/committed; the generators (concepts.json,
scaffold.py, coverage.py, the graph builder) stay local and are NOT needed to build the docs.
"""

project = "Quant Portfolio"
author = "BA Pranava"
copyright = "2026, BA Pranava"
release = "0.1"

extensions = ["myst_parser", "sphinx.ext.mathjax"]

myst_enable_extensions = [
    "dollarmath",   # $…$ / $$…$$ LaTeX math (renders via MathJax)
    "amsmath",      # \begin{align} … environments
    "colon_fence",  # ::: admonitions
    "deflist",
    "attrs_inline",
    "tasklist",
]
myst_heading_anchors = 3

source_suffix = {".md": "markdown"}
# published-manifest.md is an internal (gitignored) planning doc that happens to live here.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "published-manifest.md"]

# Internal cross-links in progress.md point at gitignored files; don't fail on those.
suppress_warnings = ["myst.xref_missing"]

html_theme = "sphinx_rtd_theme"
html_title = "Quant Portfolio"
html_static_path = ["_static"]
html_show_sourcelink = False
