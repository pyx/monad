# -*- coding: utf-8 -*-
#
# Monad documentation build configuration file.
import os
import sys

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
sys.path.insert(0, PROJECT_DIR)
import monad

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.viewcode',
]

source_suffix = '.rst'

master_doc = 'index'

project = u'Monad'
copyright = u'2012-2014, Philip Xu'

version = '%d.%d' % monad.__version__
release = monad.VERSION

exclude_patterns = ['_build']

pygments_style = 'sphinx'

html_theme = 'agogo'
# use RTD new theme
RTD_NEW_THEME = True

htmlhelp_basename = 'Monaddoc'

latex_documents = [
    ('index', 'Monad.tex', u'Monad Documentation',
     u'Philip Xu', 'manual'),
]

man_pages = [
    ('index', 'monad', u'Monad Documentation',
     [u'Philip Xu'], 1)
]

texinfo_documents = [
    ('index', 'Monad', u'Monad Documentation',
     u'Philip Xu', 'Monad', monad.__doc__,
     'Miscellaneous'),
]
