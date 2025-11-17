# Article Templates for Different Skill Types

This reference guide provides templates for different categories of Claude skills to ensure consistent article structure and coverage.

## Template Categories

### 1. Simple Metadata Skills

**Characteristics**: Only SKILL.md, no bundled resources
**Complexity**: Simple
**Focus**: Design patterns, trigger optimization, use cases

**Article Structure**:
```mdx
1. Introduction
2. Why This Skill Works (design principles)
3. SKILL.md Deep Dive (structure analysis)
4. Trigger Optimization (when to use)
5. Real Usage Examples
6. Integration Patterns
7. Conclusion
```

**Example Skills**: `todo-tracker`, `greeting-generator`

---

### 2. Script-Based Skills

**Characteristics**: Contains scripts/, process automation
**Complexity**: Moderate
**Focus**: Workflow automation, script functionality, error handling

**Article Structure**:
```mdx
1. Introduction
2. Problem This Skill Solves
3. Directory Structure (scripts/ emphasis)
4. Script Analysis (each script's purpose)
5. Workflow Deep Dive (execution flow)
6. Usage Examples (command-line demonstrations)
7. Error Handling & Edge Cases
8. Integration Patterns
9. Conclusion
```

**Example Skills**: `skill-creator`, `skill-packager`

---

### 3. Reference-Heavy Skills

**Characteristics**: Large references/ with domain knowledge
**Complexity**: Complex
**Focus**: Progressive disclosure, resource management, domain expertise

**Article Structure**:
```mdx
1. Introduction
2. Domain Overview
3. Progressive Disclosure Design
4. SKILL.md Structure
5. Reference Files Analysis
6. Loading Strategies (when to load references)
7. Usage Patterns
8. Performance Considerations
9. Real-World Applications
10. Conclusion
```

**Example Skills**: `api-contract-manager`, `database-schemas`

---

### 4. Agent-Based Skills

**Characteristics**: Uses subagents, complex workflows
**Complexity**: Complex
**Focus**: Agent patterns, task delegation, concurrent execution

**Article Structure**:
```mdx
1. Introduction
2. Why Use Subagents?
3. Agent Architecture Overview
4. SKILL.md Structure
5. Agent Configuration
6. Execution Flow
7. Error Recovery
8. Usage Examples
9. Scaling Considerations
10. Conclusion
```

**Example Skills**: `code-reviewer`, `multi-step-workflow`

---

### 5. MCP-Builder Skills

**Characteristics**: Integrates with MCP servers, tool definitions
**Complexity**: Complex
**Focus**: MCP integration, tool definitions, external services

**Article Structure**:
```mdx
1. Introduction
2. MCP Architecture Overview
3. Directory Structure
4. Tool Definition Analysis
5. Server Integration
6. Security Considerations
7. Usage Examples
8. Error Handling
9. Deployment Patterns
10. Conclusion
```

**Example Skills**: `mcp-builder`, `mcp-integrator`

---

## Template Selection Guide

### Select template based on:

1. **Resource Type**:
   - SKILL.md only → Template 1
   - Has scripts/ → Template 2
   - Has references/ → Template 3
   - Uses agents → Template 4
   - Uses MCP → Template 5

2. **Complexity**:
   - Simple skill (< 3 resources) → Use concise template
   - Complex skill (≥ 3 resources) → Use detailed template with more sections

3. **Target Audience**:
   - Beginners → Add more context and examples
   - Advanced users → Focus on architecture and patterns

---

## Section Depth Guidelines

### Article Length by Complexity:

| Complexity | Word Count | Sections | Examples |
|------------|-----------|----------|----------|
| Simple | 1500-2000 | 6-8 | 2-3 basic |
| Moderate | 2500-3500 | 8-10 | 3-4 practical |
| Complex | 3500-5000 | 10-12 | 4-5 comprehensive |

### Key Section Depth:

**Introduction** (always):
- What is this skill?
- What problem does it solve?
- Who is it for?

**Technical Deep Dive** (vary by complexity):
- Simple: Brief overview
- Moderate: Workflow analysis
- Complex: Architecture breakdown

**Examples** (vary by complexity):
- Simple: 1-2 command examples
- Moderate: Full workflow example
- Complex: Multiple scenarios with troubleshooting

---

## Writing Patterns

### Effective Skill Article Patterns

**Pattern 1: Problem-First Structure**
```mdx
<Callout type="question">
  "How do I consistently create high-quality Claude skills?"
</Callout>

This skill solves that by...
```

**Pattern 2: Before-After Demonstration**
```mdx
**Without this skill**:
- Manual, error-prone process
- Inconsistent results
- No validation

**With this skill**:
- Automated workflow
- Consistent quality
- Built-in validation
```

**Pattern 3: Progressive Disclosure**
```mdx
1. Start with overview (always visible)
2. Add details for those who want to know more
3. Provide complete implementation for advanced users
```

---

## Component Usage by Template

### Callout Placement:
- **Info**: After each major section heading
- **Warning**: Before common pitfalls
- **Tip**: After examples, for best practices
- **Question**: In introduction and transitions

### Cards Usage:
- Template 1: Design principles (2-3 cards)
- Template 2: Script purposes (3-4 cards)
- Template 3: Loading strategies (3-4 cards)
- Template 4: Agent patterns (4-5 cards)
- Template 5: Integration patterns (3-4 cards)

### Steps Usage:
- Template 1: 3-4 steps for basic workflow
- Template 2: 5-6 steps for execution flow
- Template 3: 4-5 steps for progressive loading
- Template 4: 6-8 steps for agent delegation
- Template 5: 5-7 steps for MCP integration

---

## Quality Checklist by Template

### All Templates:
- ✅ SourceAttribution component present
- ✅ All imports included
- ✅ Generic placeholders marked with {{}}
- ✅ Commands in code blocks with proper syntax highlighting
- ✅ Real skill URL in source attribution

### Template-Specific:
**Simple Skills**:
- ✅ Trigger examples included
- ✅ Multiple use cases shown
- ✅ Integration with at least 1 related skill

**Script-Based**:
- ✅ Each script documented
- ✅ Command-line examples work
- ✅ Error handling discussed

**Reference-Heavy**:
- ✅ Reference loading strategy explained
- ✅ Context size considerations noted
- ✅ When to load each reference documented

**Agent-Based**:
- ✅ Agent delegation pattern explained
- ✅ Concurrent vs sequential execution clarified
- ✅ Task splitting logic shown

**MCP-Builder**:
- ✅ Tool definitions examined
- ✅ Security implications discussed
- ✅ Deployment considerations included

---

## Related Resources

- **skill-article-writer/scripts/generate_article_outline.py**: Automated template selection
- **skill-article-writer/examples/**: Completed examples for each template type
- **Anthropic Skills Repository**: github.com/anthropics/skills

---

## ℹ️ Version Information

- **Created**: 2025-01-17
- **Template Version**: 1.0
- **Last Updated**: 2025-01-17
