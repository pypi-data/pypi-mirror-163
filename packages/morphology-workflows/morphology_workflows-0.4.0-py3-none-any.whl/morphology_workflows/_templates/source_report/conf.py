"""Configuration file for the Sphinx documentation builder."""
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

from pkg_resources import get_distribution

# -- Project information -----------------------------------------------------

project = "Morphology Workflows"

# The short X.Y version
version = get_distribution("morphology_workflows").version

# The full version, including alpha/beta/rc tags
release = version


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.graphviz",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "rst2pdf.pdfbuilder",
]

# Add any paths that contain templates here, relative to this directory.
# templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx-bluebrain-theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ['_static']

html_theme_options = {
    "metadata_distribution": "morphology-workflows",
}

html_title = project

# If true, links to the reST sources are added to the pages.
html_show_sourcelink = False

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "luigi": ("https://luigi.readthedocs.io/en/stable", None),
}

pdf_documents = [
    ("index", "report", html_title, "Neuromathematics team"),
]

latex_documents = [
    ("index", "report.tex", html_title, "Neuromathematics team", "howto"),
]
