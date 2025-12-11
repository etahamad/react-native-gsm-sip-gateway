#!/usr/bin/env python3
"""
Patch React Native's build.gradle.kts and libs.versions.toml to remove version and artifact from plugin DSL.
This avoids conflict with classpath version when using both plugin DSL and apply plugin syntax.
"""
import re
import sys
import os

def patch_libs_versions_toml(file_path):
    """Remove version and artifact from android.library plugin in libs.versions.toml."""
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        lines = content.split('\n')
        
        print(f"=== DEBUG: Patching libs.versions.toml ===")
        print(f"Looking for android.library plugin definition...")
        
        # Find the [plugins] section and android.library entry
        # Format in TOML is typically:
        # [plugins]
        # android-library = { id = "com.android.library", version = "8.9.2" }
        # or
        # android-library = { id = "com.android.library", version = "8.9.2", artifact = "com.android.tools.build:gradle:8.9.2" }
        
        modified_lines = []
        in_plugins_section = False
        changed = False
        
        for i, line in enumerate(lines):
            original_line = line
            
            # Check if we're in the [plugins] section
            if line.strip().startswith('[plugins]'):
                in_plugins_section = True
                print(f"Found [plugins] section at line {i+1}")
            elif line.strip().startswith('[') and not line.strip().startswith('[plugins'):
                in_plugins_section = False
            
            # If we're in plugins section and find android-library or android.library
            if in_plugins_section and ('android-library' in line or 'android.library' in line or 'android-library' in line.lower()):
                print(f"Found android library plugin definition at line {i+1}: {line.rstrip()}")
                original_line = line
                
                # Remove version and artifact from the line
                # TOML format examples:
                # android-library = { id = "com.android.library", version = "8.9.2" }
                # android-library = { id = "com.android.library", version = "8.9.2", artifact = "com.android.tools.build:gradle:8.9.2" }
                # android-library = { id = "com.android.library", version.ref = "agp" }
                
                # Remove version = "..." (with quotes)
                line = re.sub(r',\s*version\s*=\s*"[^"]*"', '', line)
                line = re.sub(r'version\s*=\s*"[^"]*"\s*,?\s*', '', line)
                # Remove artifact = "..." (with quotes)
                line = re.sub(r',\s*artifact\s*=\s*"[^"]*"', '', line)
                line = re.sub(r'artifact\s*=\s*"[^"]*"\s*,?\s*', '', line)
                # Remove version.ref = "..." (version references)
                line = re.sub(r',\s*version\.ref\s*=\s*"[^"]*"', '', line)
                line = re.sub(r'version\.ref\s*=\s*"[^"]*"\s*,?\s*', '', line)
                
                # Clean up any double commas or trailing commas before closing brace
                line = re.sub(r',\s*,', ',', line)  # Double commas
                line = re.sub(r',\s*}', '}', line)  # Trailing comma before }
                line = re.sub(r'{\s*,', '{', line)  # Comma right after {
                
                if line != original_line:
                    print(f"  Before: {original_line.rstrip()}")
                    print(f"  After:  {line.rstrip()}")
                    changed = True
            
            modified_lines.append(line)
        
        if changed:
            content = '\n'.join(modified_lines)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"\n=== SUCCESS: Patched {file_path} ===")
            return True
        else:
            print("No changes made to libs.versions.toml")
            # Show the plugins section for debugging
            print("\nShowing [plugins] section:")
            in_plugins = False
            for i, line in enumerate(lines, 1):
                if line.strip().startswith('[plugins]'):
                    in_plugins = True
                elif line.strip().startswith('[') and not line.strip().startswith('[plugins'):
                    if in_plugins:
                        break
                if in_plugins:
                    print(f"{i}: {line.rstrip()}")
            return False
    except Exception as e:
        print(f"Error patching libs.versions.toml: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return False

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
    
    build_gradle_kts = sys.argv[1]
    
    # First patch the build.gradle.kts (though it uses alias, so this might not be needed)
    patch_react_native_build_gradle(build_gradle_kts)
    
    # More importantly, patch the libs.versions.toml file
    # The build.gradle.kts is in node_modules/react-native/ReactAndroid/
    # The libs.versions.toml is in node_modules/react-native/gradle/
    build_dir = os.path.dirname(build_gradle_kts)
    # Navigate from ReactAndroid to react-native root, then to gradle
    react_native_root = os.path.dirname(os.path.dirname(build_dir))
    libs_versions_toml = os.path.join(react_native_root, 'gradle', 'libs.versions.toml')
    
    print(f"\n=== Attempting to patch version catalog ===")
    print(f"Looking for: {libs_versions_toml}")
    
    if os.path.exists(libs_versions_toml):
        patch_libs_versions_toml(libs_versions_toml)
    else:
        print(f"libs.versions.toml not found at {libs_versions_toml}")
        # Try alternative location
        alt_path = os.path.join(os.path.dirname(build_dir), 'gradle', 'libs.versions.toml')
        print(f"Trying alternative: {alt_path}")
        if os.path.exists(alt_path):
            patch_libs_versions_toml(alt_path)
        else:
            print("Could not find libs.versions.toml - version catalog may be defined elsewhere")
    
    # Always return success - no changes needed is also OK
    sys.exit(0)

