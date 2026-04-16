#!/usr/bin/env python
"""Commit STEP 9 changes to git."""
import subprocess
import os

os.chdir(r'C:\PrimeTrade\Primetrade-Backend')

# Add files
print("Adding files...")
result = subprocess.run(['git', 'add', '.'], capture_output=True, text=True)
if result.returncode != 0:
    print(f"Error adding files: {result.stderr}")
    exit(1)

# Commit
print("Committing...")
result = subprocess.run([
    'git', 'commit', 
    '-m', 'step 9: implement role-based access control with admin endpoints'
], capture_output=True, text=True)
print(result.stdout or result.stderr)
if result.returncode != 0 and 'nothing to commit' not in result.stderr:
    print(f"Error committing: {result.stderr}")
    exit(1)

# Push
print("Pushing to GitHub...")
result = subprocess.run(['git', 'push'], capture_output=True, text=True)
print(result.stdout or result.stderr)
if result.returncode != 0:
    print(f"Error pushing: {result.stderr}")
    exit(1)

print("\n✓ STEP 9 committed and pushed successfully")
