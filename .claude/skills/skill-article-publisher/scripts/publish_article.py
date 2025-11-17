#!/usr/bin/env python3
"""
Publish article with semantic commit and automated push.

Usage:
    python publish_article.py <mdx-file-or-directory> [--push] [--type <commit-type>]

Examples:
    python publish_article.py content/docs/en/development/article.mdx
    python publish_article.py content/docs/en/development/article.mdx --push
    python publish_article.py content/docs/en/development/article.mdx --push --type feat
"""

import re
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Any
import subprocess


class ArticlePublisher:
    """Publishes MDX articles with semantic commits and automated push."""

    def __init__(self, push: bool = False, commit_type: str = 'docs'):
        self.push = push
        self.commit_type = commit_type
        self.changes: List[Dict[str, Any]] = []
        self.project_root = None

    def find_project_root(self, start_path: Path) -> Path:
        """Find the project root containing package.json."""
        current = start_path if start_path.is_dir() else start_path.parent
        while current != current.parent:
            if (current / 'package.json').exists():
                return current
            current = current.parent
        return Path.cwd()

    def detect_changes(self, path: Path):
        """Detect changes in git repository."""
        if path.is_file():
            # Single file
            if self._is_mdx_file(path):
                rel_path = path.relative_to(self.project_root)
                self.changes.append({
                    'file': str(rel_path),
                    'type': self._detect_change_type(path),
                    'languages': self._detect_languages(path)
                })
        else:
            # Directory - find all modified/added MDX files
            changed_files = self._get_git_changed_files()
            for file_path in changed_files:
                if self._is_mdx_file(Path(file_path)):
                    self.changes.append({
                        'file': file_path,
                        'type': self._detect_change_type(Path(file_path)),
                        'languages': self._detect_languages(Path(file_path))
                    })

    def _is_mdx_file(self, path: Path) -> bool:
        """Check if file is an MDX file."""
        return path.suffix == '.mdx'

    def _get_git_changed_files(self) -> List[str]:
        """Get list of changed/added files from git."""
        try:
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=True
            )

            files = []
            for line in result.stdout.split('\n'):
                if line.strip():
                    status = line[:2]
                    file_path = line[3:].strip()
                    # Include added (A), modified (M), and renamed (R) files
                    if status[0] in ['A', 'M', 'R'] or status[1] in ['A', 'M']:
                        files.append(file_path)

            return files
        except subprocess.CalledProcessError:
            return []

    def _detect_change_type(self, file_path: Path) -> str:
        """Detect the type of change from file path and content."""
        path_str = str(file_path)

        # Detect based on path patterns
        if 'analyzing-' in path_str:
            return 'skill-analysis'
        elif any(x in path_str for x in ['mcp-', 'playwright', 'webapp-testing']):
            return 'testing'
        elif 'development' in path_str or 'tutorial' in path_str:
            return 'tutorial'
        else:
            return 'article'

    def _detect_languages(self, file_path: Path) -> List[str]:
        """Detect languages from file path."""
        path_str = str(file_path)
        languages = []

        if '/en/' in path_str:
            languages.append('en')
        if '/zh/' in path_str:
            languages.append('zh')
        if '/fr/' in path_str:
            languages.append('fr')

        return languages if languages else ['en']  # Default to English

    def validate_build(self) -> bool:
        """Run build to ensure files compile correctly."""
        print("🔧 Validating build...")
        try:
            result = subprocess.run(
                ['npm', 'run', 'build'],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=300
            )

            if result.returncode != 0:
                print("❌ Build validation failed:")
                print(result.stderr)
                return False

            print("✅ Build validation passed")
            return True
        except subprocess.TimeoutExpired:
            print("⚠️  Build timeout (5 minutes)")
            return False
        except Exception as e:
            print(f"⚠️  Could not run build: {str(e)}")
            return True  # Continue anyway

    def validate_mdx(self, path: Path) -> bool:
        """Run MDX validation."""
        print("🔍 Running MDX validation...")
        try:
            result = subprocess.run(
                ['python', 'scripts/validate_mdx.py', str(path)],
                cwd=self.project_root / '.claude/skills/skill-article-publisher',
                capture_output=True,
                text=True
            )

            # Print validation output
            if result.stdout:
                print(result.stdout)

            if result.returncode != 0:
                print("❌ MDX validation failed")
                if result.stderr:
                    print(result.stderr)
                return False

            return True
        except Exception as e:
            print(f"⚠️  Could not run MDX validation: {str(e)}")
            return True  # Continue anyway

    def generate_commit_message(self) -> str:
        """Generate semantic commit message based on detected changes."""
        if not self.changes:
            return f'{self.commit_type}: publish article'

        # Group by type
        by_type: Dict[str, List[str]] = {}
        by_language: Dict[str, List[str]] = {}

        for change in self.changes:
            change_type = change['type']
            file_name = Path(change['file']).name

            if change_type not in by_type:
                by_type[change_type] = []
            by_type[change_type].append(file_name)

            # Group by language
            for lang in change['languages']:
                if lang not in by_language:
                    by_language[lang] = []
                by_language[lang].append(file_name)

        # Determine primary change type
        primary_type = self.commit_type
        if 'skill-analysis' in by_type:
            primary_type = 'feat'
        elif len(self.changes) > 3:
            primary_type = 'feat'

        # Build message
        message_lines = []

        # Main commit line
        if len(self.changes) == 1:
            # Single file
            change = self.changes[0]
            file_name = Path(change['file']).name.replace('.mdx', '')
            message_lines.append(f"{primary_type}: publish {file_name}")
        else:
            # Multiple files
            type_summary = ', '.join(f"{len(files)} {t}" for t, files in by_type.items())
            message_lines.append(f"{primary_type}: publish multiple articles ({type_summary})")

        # Body with details
        message_lines.append('')

        # Group by type
        for change_type, files in sorted(by_type.items()):
            message_lines.append(f"{change_type.replace('-', ' ').title()}: {', '.join(files[:3])}{'...' if len(files) > 3 else ''}")

        # Add language info if multiple languages
        if len(by_language) > 1:
            message_lines.append('')
            message_lines.append('Languages: ' + ', '.join(sorted(by_language.keys())))

        return '\n'.join(message_lines)

    def stage_and_commit(self, message: str) -> bool:
        """Stage changes and create commit."""
        print(f"\n📝 Preparing commit...")

        try:
            # Stage all changes
            subprocess.run(
                ['git', 'add', '-A'],
                cwd=self.project_root,
                check=True,
                capture_output=True
            )

            # Check if there are staged changes
            result = subprocess.run(
                ['git', 'diff', '--staged', '--name-only'],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=True
            )

            if not result.stdout.strip():
                print("⚠️  No changes to commit")
                return False

            # Create commit
            subprocess.run(
                ['git', 'commit', '-m', message],
                cwd=self.project_root,
                check=True,
                capture_output=True
            )

            print("✅ Commit created successfully")
            return True

        except subprocess.CalledProcessError as e:
            print(f"❌ Git operation failed: {str(e)}")
            if e.stderr:
                print(f"Error: {e.stderr.decode() if isinstance(e.stderr, bytes) else e.stderr}")
            return False

    def push_changes(self) -> bool:
        """Push changes to remote repository."""
        print(f"\n🚀 Pushing to remote...")

        try:
            # Get current branch
            result = subprocess.run(
                ['git', 'branch', '--show-current'],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=True
            )
            branch = result.stdout.strip()

            # Push
            subprocess.run(
                ['git', 'push', 'origin', branch],
                cwd=self.project_root,
                check=True
            )

            print(f"✅ Changes pushed to origin/{branch}")
            return True

        except subprocess.CalledProcessError as e:
            print(f"❌ Push failed: {str(e)}")
            return False

    def print_summary(self):
        """Print summary of changes."""
        print("\n" + "="*80)
        print("ARTICLE PUBLISH SUMMARY")
        print("="*80)

        if self.changes:
            print(f"\n📄 Changes detected ({len(self.changes)} files):")
            for change in self.changes:
                languages = ', '.join(change['languages'])
                print(f"  - {change['file']} [{languages}]")

        commit_msg = self.generate_commit_message()
        print(f"\n📝 Generated commit message:\n")
        for line in commit_msg.split('\n'):
            print(f"    {line}")

        print(f"\n📦 Actions:")
        if self.changes:
            if self.push:
                print("  ✅ Validate MDX")
                print("  ✅ Run build check")
                print("  ✅ Create semantic commit")
                print("  ✅ Push to remote")
            else:
                print("  ✅ Validate MDX")
                print("  ✅ Run build check")
                print("  ✅ Create semantic commit (dry run)")
                print("  ⏭️  Push (use --push to enable)")
        else:
            print("  ⚠️  No changes detected")

        print("="*80)


def main():
    parser = argparse.ArgumentParser(description='Publish article with semantic commit and automated push')
    parser.add_argument('path', help='Path to MDX file or directory to publish')
    parser.add_argument('--push', action='store_true', help='Push changes to remote after commit')
    parser.add_argument('--type', choices=['docs', 'feat', 'fix', 'chore'], default='docs',
                       help='Commit type for semantic commits (default: docs)')
    parser.add_argument('--skip-build', action='store_true', help='Skip build validation')
    parser.add_argument('--skip-mdx', action='store_true', help='Skip MDX validation')

    args = parser.parse_args()

    path = Path(args.path)
    if not path.exists():
        print(f"❌ Path does not exist: {path}")
        sys.exit(1)

    # Initialize publisher
    publisher = ArticlePublisher(push=args.push, commit_type=args.type)
    publisher.project_root = publisher.find_project_root(path)

    print(f"📁 Project root: {publisher.project_root}")

    # Detect changes
    publisher.detect_changes(path)

    if not publisher.changes:
        print("⚠️  No MDX changes detected")
        publisher.print_summary()
        sys.exit(0)

    # Validate build
    if not args.skip_build:
        if not publisher.validate_build():
            print("\n❌ Build validation failed. Fix errors before publishing.")
            sys.exit(1)
    else:
        print("\n⏭️  Skipping build validation")

    # Validate MDX
    if not args.skip_mdx:
        if not publisher.validate_mdx(path):
            print("\n❌ MDX validation failed. Fix errors before publishing.")
            sys.exit(1)
    else:
        print("\n⏭️  Skipping MDX validation")

    # Generate and show commit message
    commit_msg = publisher.generate_commit_message()
    publisher.print_summary()

    # Confirm before commit
    if args.push:
        print("\n" + "="*80)
        response = input("Proceed with commit and push? [y/N]: ").strip().lower()
        if response not in ['y', 'yes']:
            print("❌ Aborted")
            sys.exit(0)

    # Stage and commit
    if publisher.stage_and_commit(commit_msg):
        # Push if requested
        if args.push:
            if publisher.push_changes():
                print("\n✅ Publish complete!")
            else:
                print("\n❌ Commit succeeded but push failed")
                sys.exit(1)
        else:
            print("\n✅ Commit created (dry run - use --push to actually push)")
    else:
        print("\n❌ Commit failed")
        sys.exit(1)


if __name__ == '__main__':
    main()
