"""
Suppress warning by site-packages/sitecustomize.py
"""
import warnings


warnings.filterwarnings("ignore", category=DeprecationWarning)
