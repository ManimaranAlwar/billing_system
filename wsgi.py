"""
Vercel serverless entry point for ALWAR Store billing system.
"""
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app as application

# Vercel expects a variable named 'app'
app = application