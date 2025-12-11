#!/usr/bin/env python3
"""
Patch React Native's build.gradle.kts to remove version and artifact from plugin DSL.
This avoids conflict with classpath version when using both plugin DSL and apply plugin syntax.
"""
import re
import sys
import os

def patch_react_native_build_gradle(file_path):
    """Remove version and artifact specifications from React Native's plugin DSL."""
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        # Pattern to match: id("com.android.library") version "..." artifact "..."
        # Handle various formats including multiline
        patterns = [
            # Single line with version and artifact
            (r'id\("com\.android\.library"\)\s+version\s+"[^"]*"\s+artifact\s+"[^"]*"', 'id("com.android.library")'),
            (r'id\("com\.android\.library"\)\s+version\s*=\s*"[^"]*"\s+artifact\s*=\s*"[^"]*"', 'id("com.android.library")'),
            # Multiline pattern (version on one line, artifact on next)
            (r'id\("com\.android\.library"\)\s+version\s+"[^"]*"\s*\n\s*artifact\s+"[^"]*"', 'id("com.android.library")'),
            # Just version (fallback)
            (r'id\("com\.android\.library"\)\s+version\s+"[^"]*"', 'id("com.android.library")'),
            (r'id\("com\.android\.library"\)\s+version\s*=\s*"[^"]*"', 'id("com.android.library")'),
        ]
        
        for pattern, replacement in patterns:
            content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
        
        if content != original:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Successfully patched {file_path}")
            # Show what was changed
            for line in content.split('\n')[:20]:
                if 'com.android.library' in line:
                    print(f"Found: {line.strip()}")
            return True
        else:
            print("No changes made - checking content...")
            for i, line in enumerate(content.split('\n')[:20], 1):
                if 'com.android' in line.lower():
                    print(f"Line {i}: {line.strip()}")
            return False
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return False

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 patch_react_native_build.py <path_to_build.gradle.kts>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    # Always return success - no changes needed is also OK
    patch_react_native_build_gradle(file_path)
    sys.exit(0)

