import sys
import os
import json
import re
import time


# Dynamically add the project root to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))  # Move up two levels
sys.path.append(project_root)

# Now, you can safely import modules
from modules.utils.path_manager import PATHS

"""
efficiency_tuning.py
Optimizes processing speed, memory usage, and parallel execution.
"""

import concurrent.futures
import functools

def optimize_resume_data(data):
    """Optimize structured resume data for efficiency."""
    if not isinstance(data, dict):
        raise TypeError(f"Expected dictionary for efficiency tuning, got {type(data)}")

    # Example optimization: Trim whitespace and remove empty sections
    optimized_data = {k: v.strip() for k, v in data.items() if isinstance(v, str) and v.strip()}
    
    return optimized_data