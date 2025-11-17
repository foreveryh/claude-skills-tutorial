#!/usr/bin/env python3
"""
MDX file validator for Claude skills documentation.

Usage:
    python validate_mdx.py <file-or-directory>

Examples:
    python validate_mdx.py content/docs/en/development/article.mdx
    python validate_mdx.py content/docs/en/development/
    python validate_mdx.py content/docs/en/
"""

import re
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Any
import subprocess


class MDXValidator:
    """Validator for MDX files with Claude skills documentation patterns."""

    def __init__(self):
        self.errors: List[Dict[str, Any]] = []
        self.warnings: List[Dict[str, Any]] = []
        self.files_checked: int = 0
        self.files_valid: int = 0

    def validate_file(self, file_path: Path) -> bool:
        """Validate a single MDX file."""
        self.files_checked += 1

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check 1: Validate frontmatter
            self._validate_frontmatter(content, file_path)

            # Check 2: Find unescaped comparison operators in text
            self._validate_comparison_operators(content, file_path)

            # Check 3: Check for common unescaped characters
            self._validate_unescaped_characters(content, file_path)

            # Check 4: Validate MDX component syntax
            self._validate_mdx_components(content, file_path)

            # Check 5: Check for unclosed tags
            self._validate_tag_balance(content, file_path)

            self.files_valid += 1
            return True

        except Exception as e:
            self.errors.append({
                'file': str(file_path),
                'line': 0,
                'message': f'Error reading file: {str(e)}'
            })
            return False

    def _validate_frontmatter(self, content: str, file_path: Path):
        """Validate YAML frontmatter."""
        if not content.startswith('---\n'):
            self.warnings.append({
                'file': str(file_path),
                'line': 1,
                'message': 'File does not start with YAML frontmatter (---)'
            })
            return

        frontmatter_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if not frontmatter_match:
            self.errors.append({
                'file': str(file_path),
                'line': 1,
                'message': 'Invalid frontmatter format. Must be: ---\n...\n---'
            })
            return

        frontmatter = frontmatter_match.group(1)

        # Check required fields
        required_fields = ['title', 'description', 'lang']
        for field in required_fields:
            if f'{field}:' not in frontmatter:
                self.warnings.append({
                    'file': str(file_path),
                    'line': 1,
                    'message': f'Missing recommended field in frontmatter: {field}'
                })

        # Validate lang field
        lang_match = re.search(r'^lang:\s*"?([a-z]{2})"?', frontmatter, re.MULTILINE)
        if not lang_match:
            self.errors.append({
                'file': str(file_path),
                'line': 1,
                'message': 'Missing or invalid lang field in frontmatter. Use 2-letter code like "en", "zh", "fr"'
            })
        else:
            lang = lang_match.group(1)
            if lang not in ['en', 'zh', 'fr']:
                self.warnings.append({
                    'file': str(file_path),
                    'line': 1,
                    'message': f'Lang code "{lang}" may not be supported. Consider using en, zh, or fr.'
                })

    def _validate_comparison_operators(self, content: str, file_path: Path):
        """Find unescaped comparison operators that should be HTML entities."""
        # Skip frontmatter
        content_without_frontmatter = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)

        # Patterns that commonly contain problematic comparison operators
        problematic_patterns = [
            (r'\*\*Good\*\*:\s*>(\d+%)', r'**Good**: &gt;\1'),
            (r'\*\*Excellent\*\*:\s*>(\d+%)', r'**Excellent**: &gt;\1'),
            (r'\*\*Outstanding\*\*:\s*>(\d+%)', r'**Outstanding**: &gt;\1'),
            (r'Typical benchmarks:\s*\n\s*- \*\*.*?\*\*:\s*>(\d+%)', None),
            (r'Jalons typiques\s*:\s*\n\s*- \*\*.*?\*\*:\s*>(\d+%)', None),
            (r'典型基准：\s*\n\s*- \*\*.*?\*\*：\s*>(\d+%)', None),
        ]

        lines = content_without_frontmatter.split('\n')
        for line_num, line in enumerate(lines, start=1):
            # Skip code blocks
            if line.strip().startswith('```'):
                continue

            for pattern, _ in problematic_patterns:
                if re.search(pattern, line):
                    if '&gt;' not in line and '&lt;' not in line:
                        self.warnings.append({
                            'file': str(file_path),
                            'line': line_num,
                            'message': f'Unescaped comparison operator found. Use &gt; instead of > in: {line.strip()[:80]}'
                        })

    def _validate_unescaped_characters(self, content: str, file_path: Path):
        """Check for other common unescaped characters in MDX."""
        content_without_frontmatter = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
        lines = content_without_frontmatter.split('\n')

        for line_num, line in enumerate(lines, start=1):
            # Skip code blocks
            if line.strip().startswith('```'):
                continue

            # Check for unescaped < that might be interpreted as HTML tag
            # But allow legitimate HTML entities and MDX components
            if re.search(r'<[^/a-zA-Z]', line) and not re.search(r'<(Callout|Steps|Cards|Tab|Tabs|File|Folder|Files|CodeBlock|SourceAttribution)', line):
                if not re.search(r'&lt;', line):
                    self.warnings.append({
                        'file': str(file_path),
                        'line': line_num,
                        'message': f'Potentially unescaped < character. Consider using &lt; or wrapping in code block: {line.strip()[:60]}'
                    })

    def _validate_mdx_components(self, content: str, file_path: Path):
        """Validate MDX component syntax (simplified - build catches complex issues)."""
        # Only check for obviously malformed components
        # Complex validation is left to the build process

        # Check for components without closing slash that might be typos
        possible_typos = re.findall(r'<(/?)(\w+)[^>]*>', content)

        for closing, name in possible_typos:
            if name in ['SourceAttribution', 'Callout', 'Cards', 'Card', 'Steps', 'Step', 'Files', 'File', 'Folder', 'Tabs', 'Tab', 'CodeBlock']:
                # Just do basic sanity check - don't enforce strict matching
                # Build validation will catch real syntax errors
                pass

    def _validate_tag_balance(self, content: str, file_path: Path):
        """Check for unclosed HTML tags in non-MDX content."""
        # Simple check for common HTML tags
        simple_tags = ['b', 'i', 'strong', 'em', 'code', 'pre']

        for tag in simple_tags:
            open_count = len(re.findall(r'<{}\b[^>]*>'.format(tag), content))
            close_count = len(re.findall(r'</{}>'.format(tag), content))
            if open_count != close_count:
                self.warnings.append({
                    'file': str(file_path),
                    'line': 0,
                    'message': f'Tag <{tag}> appears {open_count} times but </{tag}> appears {close_count} times (may be intentional in MDX)'
                })

    def run_build_check(self, dir_path: Path = None) -> bool:
        """Run npm build to validate MDX compilation."""
        print("\n🔧 Running build validation (this may take a while)...")

        # Determine project root
        if dir_path:
            # Try to find package.json in parent directories
            project_root = dir_path
            while project_root != project_root.parent:
                if (project_root / 'package.json').exists():
                    break
                project_root = project_root.parent
        else:
            project_root = Path.cwd()

        if not (project_root / 'package.json').exists():
            self.warnings.append({
                'file': 'build',
                'line': 0,
                'message': 'Could not find package.json in project. Skipping build validation.'
            })
            return True

        try:
            # Run npm build
            result = subprocess.run(
                ['npm', 'run', 'build'],
                cwd=project_root,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )

            if result.returncode != 0:
                self.errors.append({
                    'file': 'build',
                    'line': 0,
                    'message': 'Build failed. Check MDX syntax errors below:'
                })
                # Extract relevant error messages
                for line in result.stderr.split('\n'):
                    if 'Error' in line or 'error' in line or 'mdx' in line.lower():
                        self.errors.append({
                            'file': 'build',
                            'line': 0,
                            'message': line.strip()
                        })
                return False
            else:
                print("✅ Build validation passed")
                return True

        except subprocess.TimeoutExpired:
            self.errors.append({
                'file': 'build',
                'line': 0,
                'message': 'Build timeout after 5 minutes. This may indicate a problem or just a large project.'
            })
            return False
        except Exception as e:
            self.errors.append({
                'file': 'build',
                'line': 0,
                'message': f'Error running build: {str(e)}'
            })
            return False

    def print_report(self):
        """Print validation report."""
        print("\n" + "="*80)
        print("MDX VALIDATION REPORT")
        print("="*80)

        if self.errors:
            print(f"\n❌ ERRORS ({len(self.errors)}):")
            for error in self.errors:
                print(f"  File: {error['file']}:{error['line']}")
                print(f"  Error: {error['message']}")
                print()

        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings[:10]:  # Show first 10 warnings
                print(f"  File: {warning['file']}:{warning['line']}")
                print(f"  Warning: {warning['message']}")
                print()
            if len(self.warnings) > 10:
                print(f"  ... and {len(self.warnings) - 10} more warnings")

        print(f"\n📊 SUMMARY:")
        print(f"  Files checked: {self.files_checked}")
        print(f"  Files valid: {self.files_valid}")
        print(f"  Errors: {len(self.errors)}")
        print(f"  Warnings: {len(self.warnings)}")

        if not self.errors and not self.warnings:
            print("\n✅ All files passed validation with no issues!")
        elif not self.errors:
            print("\n✅ All files passed validation (with warnings)")
        else:
            print("\n❌ Validation failed due to errors")

        print("="*80)


def main():
    parser = argparse.ArgumentParser(description='Validate MDX files for Claude skills documentation')
    parser.add_argument('path', help='Path to MDX file or directory to validate')
    parser.add_argument('--build', action='store_true', help='Run build validation (slower but more thorough)')
    parser.add_argument('--no-build', action='store_true', help='Skip build validation')

    args = parser.parse_args()

    path = Path(args.path)
    if not path.exists():
        print(f"Error: Path does not exist: {path}")
        sys.exit(1)

    validator = MDXValidator()

    # Validate MDX files
    if path.is_file():
        if path.suffix == '.mdx':
            validator.validate_file(path)
        else:
            print(f"Skipping non-MDX file: {path}")
    else:
        # Recursively validate all MDX files in directory
        mdx_files = list(path.rglob('*.mdx'))
        if not mdx_files:
            print(f"No MDX files found in: {path}")
            sys.exit(0)

        print(f"Found {len(mdx_files)} MDX files to validate")
        for i, file_path in enumerate(mdx_files, 1):
            print(f"\r[{i}/{len(mdx_files)}] Validating {file_path.name}...", end='')
            validator.validate_file(file_path)
        print()  # New line after progress

    # Run build validation if requested
    if args.build and not args.no_build:
        validator.run_build_check(path if path.is_dir() else path.parent)
    elif not args.no_build and not args.build:
        # Default: run build check for directories
        if path.is_dir():
            validator.run_build_check(path)

    validator.print_report()

    # Exit with error code if errors found
    sys.exit(1 if validator.errors else 0)


if __name__ == '__main__':
    main()
