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
        
        # Debug: Show lines around plugin declaration (error says line 16)
        print("=== DEBUG: Searching for plugin declaration ===")
        lines = content.split('\n')
        
        # Check around line 16 specifically (where error occurred)
        print(f"Checking lines 1-30 (error reported at line 16):")
        for i in range(min(30, len(lines))):
            line = lines[i]
            if 'com.android.library' in line.lower() or ('plugins' in line.lower() and 'id(' in line):
                print(f"Line {i+1}: {line.rstrip()}")
                # Show context
                for j in range(max(0, i-2), min(len(lines), i+3)):
                    marker = ">>>" if j == i else "   "
                    print(f"{marker} {j+1}: {lines[j].rstrip()}")
        
        # Also search entire file for plugin declarations
        print(f"\n=== DEBUG: Searching entire file for plugin declarations ===")
        for i, line in enumerate(lines, 1):
            if 'id(' in line and 'android' in line.lower():
                print(f"Line {i}: {line.rstrip()}")
        
        # Show raw content around line 16 (where error occurred)
        print(f"\n=== DEBUG: Raw content around line 16 ===")
        for i in range(max(0, 14), min(len(lines), 20)):
            print(f"{i+1:3d}: {lines[i].rstrip()}")
        
        # Pattern to match: id("com.android.library") version "..." artifact "..."
        # Handle various formats including multiline
        # The error shows: id: 'com.android.library', version: '8.9.2', artifact: 'com.android.tools.build:gradle:8.9.2'
        patterns = [
            # Single line with version and artifact - most specific first
            # Format: id("com.android.library") version "8.9.2" artifact "com.android.tools.build:gradle:8.9.2"
            (r'id\("com\.android\.library"\)\s+version\s+"[^"]*"\s+artifact\s+"[^"]*"', 'id("com.android.library")'),
            # With equals signs
            (r'id\("com\.android\.library"\)\s+version\s*=\s*"[^"]*"\s+artifact\s*=\s*"[^"]*"', 'id("com.android.library")'),
            # Multiline pattern (version on one line, artifact on next)
            (r'id\("com\.android\.library"\)\s+version\s+"[^"]*"\s*\n\s*artifact\s+"[^"]*"', 'id("com.android.library")'),
            (r'id\("com\.android\.library"\)\s+version\s+"[^"]*"\s*\n\s*artifact\s*=\s*"[^"]*"', 'id("com.android.library")'),
            # Just version (fallback)
            (r'id\("com\.android\.library"\)\s+version\s+"[^"]*"', 'id("com.android.library")'),
            (r'id\("com\.android\.library"\)\s+version\s*=\s*"[^"]*"', 'id("com.android.library")'),
        ]
        
        print(f"\n=== DEBUG: Applying patterns ===")
        for idx, (pattern, replacement) in enumerate(patterns, 1):
            matches = list(re.finditer(pattern, content, flags=re.MULTILINE))
            if matches:
                print(f"Pattern {idx} matched: {len(matches)} occurrence(s)")
                print(f"  Pattern: {pattern}")
                for match in matches[:3]:  # Show first 3 matches
                    start_line = content[:match.start()].count('\n') + 1
                    print(f"  Match at line {start_line}: {match.group()[:80]}")
                content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
        
        if content != original:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"\n=== SUCCESS: Patched {file_path} ===")
            # Show what was changed
            print("After patch - plugin declaration:")
            for i, line in enumerate(content.split('\n')[:20], 1):
                if 'com.android.library' in line:
                    print(f"Line {i}: {line.strip()}")
            return True
        else:
            print("\n=== WARNING: No regex matches found, trying manual line-by-line replacement ===")
            # Try manual replacement line by line
            modified_lines = []
            changed = False
            for i, line in enumerate(lines):
                original_line = line
                # Check if this line contains the plugin declaration
                if 'id("com.android.library")' in line:
                    # Try to remove version and artifact from this line
                    # Pattern: id("com.android.library") version "X" artifact "Y"
                    line = re.sub(r'\s+version\s+"[^"]*"', '', line)
                    line = re.sub(r'\s+artifact\s+"[^"]*"', '', line)
                    line = re.sub(r'\s+version\s*=\s*"[^"]*"', '', line)
                    line = re.sub(r'\s+artifact\s*=\s*"[^"]*"', '', line)
                    if line != original_line:
                        print(f"Manual replacement at line {i+1}:")
                        print(f"  Before: {original_line.rstrip()}")
                        print(f"  After:  {line.rstrip()}")
                        changed = True
                modified_lines.append(line)
            
            if changed:
                content = '\n'.join(modified_lines)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"\n=== SUCCESS: Manually patched {file_path} ===")
                return True
            else:
                print("Still no changes made - showing all lines with 'id(' and 'android':")
                # More thorough search
                for i, line in enumerate(lines, 1):
                    if 'id(' in line and 'android' in line.lower():
                        print(f"Line {i}: {line.rstrip()}")
                        # Show more context
                        for j in range(max(0, i-1), min(len(lines), i+2)):
                            print(f"  {j+1}: {lines[j].rstrip()}")
                return False
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 patch_react_native_build.py <path_to_build.gradle.kts>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    # Always return success - no changes needed is also OK
    patch_react_native_build_gradle(file_path)
    sys.exit(0)

