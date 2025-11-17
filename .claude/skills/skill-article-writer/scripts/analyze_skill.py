#!/usr/bin/env python3
"""
Analyze a skill structure and generate metadata for article creation.

Usage:
    python analyze_skill.py <skill-path> [--output <output-file>]

Examples:
    python analyze_skill.py /path/to/skill-creator
    python analyze_skill.py /path/to/skill-creator --output skill-metadata.json
"""

import json
import sys
import argparse
from pathlib import Path
from typing import Dict, Any, List


def analyze_skill(skill_path: Path) -> Dict[str, Any]:
    """Analyze a skill directory and extract comprehensive metadata."""

    metadata = {
        "skill_path": str(skill_path),
        "name": skill_path.name,
        "exists": skill_path.exists(),
        "structure": {},
        "skill_md": {},
        "scripts": [],
        "references": [],
        "assets": [],
        "analysis": {
            "complexity": "unknown",
            "resource_types": [],
            "key_features": [],
            "recommendations": []
        }
    }

    if not skill_path.exists():
        return metadata

    # Analyze directory structure
    structure_analysis = analyze_structure(skill_path)
    metadata["structure"] = structure_analysis

    # Analyze SKILL.md
    skill_md_path = skill_path / "SKILL.md"
    if skill_md_path.exists():
        skill_md_analysis = analyze_skill_md(skill_md_path)
        metadata["skill_md"] = skill_md_analysis

    # Analyze bundled resources
    metadata["scripts"] = list_resource_files(skill_path / "scripts", ["*.py", "*.sh", "*.js"])
    metadata["references"] = list_resource_files(skill_path / "references", ["*.md", "*.txt", "*.json"])
    metadata["assets"] = list_resource_files(skill_path / "assets", ["*"])

    # Generate skill-level analysis
    metadata["analysis"] = generate_skill_analysis(metadata)

    return metadata


def analyze_structure(skill_path: Path) -> Dict[str, Any]:
    """Analyze the directory structure of a skill."""

    return {
        "has_skill_md": (skill_path / "SKILL.md").exists(),
        "has_scripts": (skill_path / "scripts").exists(),
        "has_references": (skill_path / "references").exists(),
        "has_assets": (skill_path / "assets").exists(),
        "total_files": count_files(skill_path),
        "depth": get_directory_depth(skill_path)
    }


def analyze_skill_md(skill_md_path: Path) -> Dict[str, Any]:
    """Analyze the SKILL.md file."""

    try:
        with open(skill_md_path, 'r', encoding='utf-8') as f:
            content = f.read()

        return {
            "exists": True,
            "size": len(content),
            "line_count": len(content.split('\n')),
            "has_yaml_frontmatter": content.startswith('---\n'),
            "sections": extract_sections(content),
            "title": extract_title(content),
            "description": extract_description(content),
            "commands": extract_commands(content)
        }
    except Exception as e:
        return {
            "exists": True,
            "error": str(e),
            "size": 0,
            "line_count": 0
        }


def extract_sections(content: str) -> List[str]:
    """Extract major section headings from SKILL.md."""

    sections = []
    for line in content.split('\n'):
        line = line.strip()
        if line.startswith('## '):
            section = line[3:].strip()
            if section and not section.startswith('---'):
                sections.append(section)
    return sections


def extract_title(content: str) -> str:
    """Extract the skill name from frontmatter or first heading."""

    if content.startswith('---'):
        parts = content.split('\n---', 1)
        if len(parts) == 2:
            frontmatter = parts[0]
            lines = frontmatter.split('\n')
            for line in lines:
                if line.startswith('name: '):
                    return line[6:].strip().strip('"\'')

    # Fallback: find first H1
    for line in content.split('\n'):
        if line.startswith('# '):
            return line[2:].strip()

    return "Unknown Skill"


def extract_description(content: str) -> str:
    """Extract skill description from frontmatter."""

    if content.startswith('---'):
        parts = content.split('\n---', 1)
        if len(parts) == 2:
            frontmatter = parts[0]
            lines = frontmatter.split('\n')
            for line in lines:
                if line.startswith('description: '):
                    desc = line[13:].strip().strip('"\'')
                    return desc if len(desc) < 200 else desc[:200] + "..."

    return "No description available"


def extract_commands(content: str) -> List[str]:
    """Extract command-line examples from the content."""

    commands = []
    in_code_block = False
    current_block = []

    for line in content.split('\n'):
        if line.startswith('```bash'):
            in_code_block = True
            current_block = []
        elif line.startswith('```') and in_code_block:
            in_code_block = False
            block_content = '\n'.join(current_block).strip()
            if block_content:
                commands.append(block_content)
        elif in_code_block:
            current_block.append(line)

    return commands


def list_resource_files(resource_path: Path, patterns: List[str]) -> List[str]:
    """List files in a resource directory."""

    if not resource_path.exists() or not resource_path.is_dir():
        return []

    files = []
    for pattern in patterns:
        files.extend([str(p.relative_to(resource_path)) for p in resource_path.glob(pattern)])

    return sorted(files)


def count_files(directory: Path) -> int:
    """Count total files in directory."""

    try:
        return len(list(directory.rglob('*'))) if directory.exists() else 0
    except:
        return 0


def get_directory_depth(directory: Path) -> int:
    """Get maximum directory depth."""

    if not directory.exists():
        return 0

    max_depth = 0
    for path in directory.rglob('*'):
        if path.is_file():
            depth = len(path.relative_to(directory).parts) - 1
            max_depth = max(max_depth, depth)
    return max_depth


def generate_skill_analysis(metadata: Dict[str, Any]) -> Dict[str, Any]:
    """Generate high-level analysis of the skill."""

    analysis = {
        "complexity": determine_complexity(metadata),
        "resource_types": identify_resource_types(metadata),
        "key_features": extract_key_features(metadata),
        "recommendations": generate_recommendations(metadata)
    }

    return analysis


def determine_complexity(metadata: Dict[str, Any]) -> str:
    """Determine skill complexity level."""

    script_count = len(metadata.get("scripts", []))
    ref_count = len(metadata.get("references", []))
    asset_count = len(metadata.get("assets", []))

    total_resources = script_count + ref_count + asset_count

    if total_resources == 0:
        return "simple"
    elif total_resources <= 3:
        return "moderate"
    else:
        return "complex"


def identify_resource_types(metadata: Dict[str, Any]) -> List[str]:
    """Identify what types of resources the skill uses."""

    types = []
    if metadata.get("scripts"):
        types.append("scripts")
    if metadata.get("references"):
        types.append("references")
    if metadata.get("assets"):
        types.append("assets")
    return types


def extract_key_features(metadata: Dict[str, Any]) -> List[str]:
    """Extract key features based on skill content."""

    features = []

    # Check for common patterns
    skill_md = metadata.get("skill_md", {})
    if skill_md:
        content = skill_md.get("content", "")
        if "workflow" in content.lower():
            features.append("workflow-automation")
        if "script" in content.lower():
            features.append("scripting")
        if "API" in content.lower():
            features.append("api-integration")
        if any(word in content.lower() for word in ["create", "generate", "build"]):
            features.append("content-generation")

    return features


def generate_recommendations(metadata: Dict[str, Any]) -> List[str]:
    """Generate recommendations for article structure."""

    recs = []
    analysis = metadata.get("analysis", {})

    complexity = analysis.get("complexity", "simple")
    if complexity == "complex":
        recs.append("Use detailed sections for each resource type")
        recs.append("Include comprehensive examples")
    else:
        recs.append("Keep sections concise and focused")

    resource_types = analysis.get("resource_types", [])
    if "scripts" in resource_types:
        recs.append("Document each script's purpose and usage")
    if "references" in resource_types:
        recs.append("Explain when and how to load reference files")
    if "assets" in resource_types:
        recs.append("Show examples of asset usage in output")

    return recs


def main():
    parser = argparse.ArgumentParser(description="Analyze a Claude skill structure")
    parser.add_argument("skill_path", help="Path to the skill directory")
    parser.add_argument("--output", help="Output JSON file (default: stdout)")

    args = parser.parse_args()

    skill_path = Path(args.skill_path)

    if not skill_path.exists():
        print(f"Error: Path does not exist: {skill_path}", file=sys.stderr)
        sys.exit(1)

    metadata = analyze_skill(skill_path)

    if args.output:
        output_path = Path(args.output)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        print(f"Metadata saved to: {output_path}")
    else:
        print(json.dumps(metadata, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
