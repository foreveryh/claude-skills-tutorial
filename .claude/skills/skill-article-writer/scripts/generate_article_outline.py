#!/usr/bin/env python3
"""
Generate article outline based on skill analysis metadata.

Usage:
    python generate_article_outline.py <skill-metadata.json> [--output <outline.md>]

Examples:
    python generate_article_outline.py skill-metadata.json
    python generate_article_outline.py skill-metadata.json --output article-outline.md
"""

import json
import sys
import argparse
from pathlib import Path
from typing import Dict, Any


def generate_outline(metadata: Dict[str, Any]) -> str:
    """Generate a complete article outline based on skill metadata."""

    skill_name = metadata.get("name", "Unknown Skill")
    description = metadata.get("skill_md", {}).get("description", "No description available")
    sections = metadata.get("skill_md", {}).get("sections", [])
    analysis = metadata.get("analysis", {})

    outline = f"""---
title: "Analyzing {skill_name}: A Complete Guide"  # Will be translated
description: "{description[:150]}..."  # Will be translated
lang: {{{{language}}}}
category: development
difficulty: intermediate
tags:
  - claude-skills
  - skill-analysis
  - tutorial
source_url: "{{{{source_url}}}}"
published_date: "{{{{published_date}}}}"
author: Anthropic
source:
  url: "{{{{source_url}}}}"
  name: "Anthropic Skills Repository"
  author: "Anthropic"
  published_date: "{{{{published_date}}}}"
  accessed_date: "{{{{current_date}}}}"
  license: "See SKILL.md for terms"
import:
  date: "{{{{current_date}}}}"
  slug: "{{{{slug_from_url(source_url)}}}}"
  translator: "Claude AI"
---

import {{ SourceAttribution }} from '@/components/SourceAttribution';
import {{ Callout }} from 'fumadocs-ui/components/callout';
import {{ Cards, Card }} from 'fumadocs-ui/components/card';
import {{ Steps, Step }} from 'fumadocs-ui/components/steps';

<SourceAttribution
  source={{{{...}}}}
  languages={{{{['en', 'zh', 'fr']}}}}
  currentLang={{{{language}}}}
/>

# Analyzing {skill_name}

**{skill_name}** is {{description}} This article provides a comprehensive analysis of its structure, design patterns, and practical applications.

<Callout type="info">
  This is a real-world skill from the Anthropic skills repository, designed to {{description.lower().split()[0]}}.
</Callout>

## Overview

### What is {skill_name}?

<Callout type="question">
  Based on the description: {description}
</Callout>

### Core Purpose

The {skill_name} skill aims to:

{{generate_purpose_bullet_points(description)}}

### Target Audience

This skill is designed for:

- Users who want to...
- Developers working with...
- Anyone interested in...

## Skill Anatomy

### Directory Structure

```
{skill_name}/
├── SKILL.md (required)
└── Bundled Resources (optional)
    ├── scripts/          - Executable code
    ├── references/       - Documentation
    └── assets/           - Templates and files
```

### SKILL.md Structure

Every skill begins with metadata in YAML frontmatter:

```yaml
---
name: {skill_name}
description: "{description}"
license: See SKILL.md for terms
---
```

### Key Components

{{generate_component_sections(metadata)}}

## Technical Deep Dive

### How It Works

<Steps>
  <Step>
    **Trigger Detection**: Claude identifies when this skill should be used based on the description and user query.
  </Step>
  <Step>
    **Context Loading**: SKILL.md content is loaded into Claude's context window.
  </Step>
  <Step>
    **Resource Access**: If needed, Claude loads or references bundled resources.
  </Step>
  <Step>
    **Execution**: Claude follows the procedural instructions to complete the task.
  </Step>
</Steps>

### Detailed Workflow

{{generate_workflow_section(metadata)}}

## Usage Examples

### Basic Usage

```bash
{{generate_basic_usage(metadata)}}
```

### Advanced Scenarios

<Callout type="tip">
  Best practices and advanced usage patterns.
</Callout>

## Best Practices

Based on the design of {skill_name}, here are key principles:

{{generate_best_practices(metadata)}}

## Common Pitfalls

<Callout type="warn">
  Common mistakes users make when working with this skill.
</Callout>

{{generate_common_pitfalls(metadata)}}

## Integration with Other Skills

{skill_name} works well with:

1. **skill-creator** - For creating new skills based on this pattern
2. **skill-builder** - For extending functionality
3. **Other related skills**

## Real-World Applications

### Use Case 1: {{Use Case Description}}

Practical example of how this skill solves a real problem...

### Use Case 2: {{Another Use Case}}

Another practical example with specific details...

## Troubleshooting

<Callout type="error">
  Common errors and their solutions.
</Callout>

{{generate_troubleshooting_section(metadata)}}

## Next Steps

To use {skill_name} effectively:

1. **Clone the repository**: {{repository_url}}
2. **Install dependencies**: {{install_commands}}
3. **Follow the workflow**: {{workflow_instructions}}
4. **Iterate based on feedback**: {{iteration_tips}}

### Related Resources

- **Anthropic Skills Repository**: github.com/anthropics/skills
- **Creating Your First Skill**: /tutorials/creating-first-skill
- **Advanced Skill Development**: /development/advanced-skills

## Conclusion

{skill_name} demonstrates excellent Claude skill design by:

{{generate_conclusion_points(metadata)}}

The key insights from this skill can be applied to your own skill development projects.

---

## Summary

This analysis covered:

- ✅ Skill structure and anatomy
- ✅ Core workflow and execution flow
- ✅ Best practices and design patterns
- ✅ Real-world usage examples
- ✅ Integration strategies
- ✅ Troubleshooting guide

## Next Steps

Ready to apply what you learned?

1. **Study other skills** in the repository
2. **Create your own skill** using these patterns
3. **Share your skills** with the community
4. **Iterate and improve** based on usage

## ℹ️ Source Information

**Original Skill**: [{{skill_name}}]({{source_url}})

- **Source**: Anthropic Skills Repository
- **Author**: Anthropic
- **Accessed**: {{current_date}}
- **License**: See SKILL.md for full terms

*This article was automatically generated based on skill analysis.*

---

## Appendix

### Directory Structure Details

{{generate_directory_details(metadata)}}

### Resource Inventory

<Callout type="info">
  Complete listing of all resources included in this skill.
</Callout>

**Scripts**:
{{generate_resources_list(metadata.get("scripts", []))}}

**References**:
{{generate_resources_list(metadata.get("references", []))}}

**Assets**:
{{generate_resources_list(metadata.get("assets", []))}}
"""

    return outline


def generate_purpose_bullet_points(description: str) -> str:
    """Generate purpose bullet points from description."""

    return """- Automate repetitive tasks
- Provide specialized workflows
- Integrate domain knowledge
- Improve efficiency and consistency"""


def generate_component_sections(metadata: Dict[str, Any]) -> str:
    """Generate component analysis sections."""

    sections = []

    if metadata.get("scripts"):
        sections.append("""### Scripts

<Callout type="info">
  Scripts provide deterministic, reusable code that Claude can execute.
</Callout>

The {skill_name} includes scripts for:

- **init_skill.py**: Initialize a new skill with proper structure
- **package_skill.py**: Package and validate skills for distribution

Each script serves a specific purpose in the skill creation workflow.
""")

    if metadata.get("references"):
        sections.append("""### References

Reference files provide domain knowledge that Claude loads on-demand:

- **schemas.md**: Database schemas and data models
- **policies.md**: Company policies and guidelines
- **API specifications**: API documentation and examples
""")

    if metadata.get("assets"):
        sections.append("""### Assets

Asset files are used in the final output without being loaded into Claude's context:

- **Templates**: HTML/React boilerplate
- **Images**: Logos, icons, and visual assets
- **Sample data**: Example files for demonstration
""")

    return "\n\n".join(sections) if sections else "No bundled resources found."


def generate_workflow_section(metadata: Dict[str, Any]) -> str:
    """Generate workflow analysis section."""

    sections = metadata.get("skill_md", {}).get("sections", [])

    if len(sections) >= 3:
        return f"""### Core Workflow

The skill follows a structured workflow with {len(sections)} major steps:

<Steps>
  <Step>
    **{sections[0]}**: First step in the process...
  </Step>
  <Step>
    **{sections[1]}**: Second step with specific actions...
  </Step>
  <Step>
    **{sections[2]}**: Final step to complete the workflow...
  </Step>
</Steps>

Detailed explanation of each step and how they connect...
"""
    else:
        return """### Core Workflow

The skill provides a clear workflow that Claude follows to accomplish tasks effectively.

<Callout type="question">
  Review the SKILL.md sections to understand the detailed workflow:
</Callout>
"""


def generate_basic_usage(metadata: Dict[str, Any]) -> str:
    """Generate basic usage example."""

    skill_name = metadata.get("name", "unknown")
    return f"# Example usage for {skill_name}\n./scripts/run_{skill_name}.py --help"


def generate_best_practices(metadata: Dict[str, Any]) -> str:
    """Generate best practices section."""

    return """<Cards>
  <Card title="Progressive Disclosure" icon="Layers">
    Load information in three levels: metadata, SKILL.md, and bundled resources.
  </Card>

  <Card title="Avoid Duplication" icon="FileText">
    Keep detailed reference material in references/ files, not in SKILL.md
  </Card>

  <Card title="Test & Iterate" icon="RefreshCw">
    Use the skill on real tasks to identify improvements and update accordingly.
  </Card>
</Cards>
"""


def generate_common_pitfalls(metadata: Dict[str, Any]) -> str:
    """Generate common pitfalls section."""

    return """- **Overloading SKILL.md**: Don't include excessive detail in the main skill file.
- **Missing Context**: Ensure bundled resources are properly referenced.
- **Unclear Triggers**: Make the description specific about when to use the skill.
- **Ignoring Validation**: Always use package_skill.py before distribution.
"""


def generate_troubleshooting_section(metadata: Dict[str, Any]) -> str:
    """Generate troubleshooting section."""

    return """### Validation Errors

**Symptom**: package_skill.py reports validation errors

**Solution**: Run the script and fix all reported issues before packaging.

### Missing Resources

**Symptom**: Claude cannot find referenced files

**Solution**: Verify all paths in SKILL.md and ensure files exist.

### Skill Not Triggering

**Symptom**: Claude doesn't recognize when to use the skill

**Solution**: Make the description more specific and include trigger phrases.
"""


def generate_conclusion_points(metadata: Dict[str, Any]) -> str:
    """Generate conclusion bullet points."""

    return """- ✅ Systematically extending Claude's capabilities
- ✅ Managing context efficiently
- ✅ Providing reusable resources
- ✅ Maintaining high quality through validation
- ✅ Following proven design patterns"""


def generate_resources_list(resources: list) -> str:
    """Generate a markdown list of resources."""

    if not resources:
        return "- None"

    return "\n".join([f"- {res}" for res in resources])


def generate_directory_details(metadata: Dict[str, Any]) -> str:
    """Generate directory structure details."""

    return """### Required Files

- **SKILL.md**: The core skill definition with metadata and instructions

### Optional Directories

- **scripts/**: Executable code for the skill
- **references/**: Documentation and reference material
- **assets/**: Templates, images, and output files

### Best Practices

- Keep SKILL.md under 5k words for optimal loading
- Use descriptive names for all resources
- Follow the six-step skill creation process"""


def main():
    parser = argparse.ArgumentParser(description="Generate article outline from skill metadata")
    parser.add_argument("metadata_file", help="Path to the skill metadata JSON file")
    parser.add_argument("--output", help="Output markdown file (default: stdout)")

    args = parser.parse_args()

    metadata_path = Path(args.metadata_file)

    if not metadata_path.exists():
        print(f"Error: File not found: {metadata_path}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(metadata_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
    except Exception as e:
        print(f"Error reading metadata: {e}", file=sys.stderr)
        sys.exit(1)

    outline = generate_outline(metadata)

    if args.output:
        output_path = Path(args.output)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(outline)
        print(f"Outline saved to: {output_path}")
    else:
        print(outline)


if __name__ == "__main__":
    main()
