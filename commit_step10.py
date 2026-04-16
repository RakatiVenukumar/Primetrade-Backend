#!/usr/bin/env python
"""Commit STEP 10 changes."""
import subprocess
import os

os.chdir(r'C:\PrimeTrade\Primetrade-Backend')

# Add files
print("[1/3] Staging files...")
subprocess.run(['git', 'add', '.'])
print("[2/3] Committing...")
subprocess.run(['git', 'commit', '-m', 'step 10: create task model with ORM and schema validation'])
print("[3/3] Pushing to GitHub...")
subprocess.run(['git', 'push'])
print("\n✓ STEP 10 committed and pushed")
