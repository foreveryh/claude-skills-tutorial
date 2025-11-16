# Translator MCP Server Integration Guide

> **⚠️ DEPRECATED - This guide is kept for reference only**
>
> **The Fumadocs Article Importer now uses the built-in `translator` skill instead of Translator MCP Server.**
>
> **Benefits of the new approach:**
> - ✅ No external dependencies or configuration required
> - ✅ Uses Claude's native translation capabilities
> - ✅ Simpler setup and maintenance
> - ✅ Automatic activation when translation is needed
> - ✅ Better integration with Claude Code's skill system
>
> **Migration:** Simply remove `translator-mcp` from your MCP configuration. The translator skill is already available at `.claude/skills/translator/` and will be automatically used by the fumadocs-article-importer skill.
>
> ---

This document provides detailed instructions for integrating the Translator MCP Server with the Fumadocs Article Importer Skill. **Note: This is now deprecated in favor of the translator skill.**

## Overview

The Translator MCP Server (https://github.com/foreveryh/translator-mcp-server) provides professional-grade translation services with a three-stage workflow:

1. **Stage 1: Analysis & Planning**
   - Domain recognition (technical, legal, medical, etc.)
   - Terminology extraction
   - Translation strategy planning

2. **Stage 2: Segmented Translation**
   - Paragraph-by-paragraph translation
   - Context preservation across segments
   - Consistent terminology application

3. **Stage 3: Full-Text Review**
   - Consistency check across entire document
   - Style alignment with source
   - Final quality assurance

**Benefits over Direct Claude Translation:**
- ⚡ **3-5x faster**: ~5-10 seconds per language vs ~20-40 seconds
- 🎯 **Better quality**: Professional translation workflow
- 📚 **Terminology consistency**: Domain-aware translation
- 💰 **Cost-effective**: Optimized API usage
- 🔄 **Quality evaluation**: Built-in quality assessment

---

## Supported Languages

The MCP server supports all languages needed for this skill:

- ✅ **Chinese (zh)**: Simplified Chinese
- ✅ **English (en)**: Source and target
- ✅ **French (fr)**: Professional French
- ✅ **Korean (ko)**: Formal Korean
- ✅ **Japanese (ja)**: Additional support
- ✅ **German (de)**: Additional support

---

## Setup Options

### Option 1: Public MCP Server (Recommended for Quick Start) 🚀

**Easiest option** - No installation required!

#### For Claude Desktop

Add to your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
**Linux**: `~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "translator": {
      "url": "https://airylark-mcp.vcorp.ai/sse"
    }
  }
}
```

#### For Claude Code CLI

Add to your Claude Code configuration:

```bash
# Create or edit config file
vim ~/.claude/config.json
```

```json
{
  "mcpServers": {
    "translator": {
      "url": "https://airylark-mcp.vcorp.ai/sse"
    }
  }
}
```

#### For Cursor

Add to Cursor settings:

```json
{
  "mcp": {
    "servers": {
      "translator": {
        "url": "https://airylark-mcp.vcorp.ai/sse"
      }
    }
  }
}
```

**Verify Connection:**
After restarting Claude, the MCP server should be automatically available. You'll see `translate_text` and `evaluate_translation` tools available.

---

### Option 2: Self-Hosted MCP Server (For Privacy/Control) 🔒

**Best for**: Production use, privacy-sensitive content, custom configurations

#### Step 1: Clone and Install

```bash
# Clone the repository
git clone https://github.com/foreveryh/translator-mcp-server
cd translator-mcp-server/mcp-server

# Install dependencies
npm install
```

#### Step 2: Configure Environment

Create a `.env` file in the `mcp-server` directory:

```bash
# Required configuration
TRANSLATION_API_KEY=your_api_key_here
TRANSLATION_MODEL=your_model_name
TRANSLATION_BASE_URL=your_api_base_url

# Optional configuration
PORT=3031  # Default port, change if needed
```

**Configuration Examples:**

**Using OpenAI API:**
```bash
TRANSLATION_API_KEY=sk-proj-xxxxxxxxxxxxx
TRANSLATION_MODEL=gpt-4-turbo
TRANSLATION_BASE_URL=https://api.openai.com/v1
```

**Using Anthropic API:**
```bash
TRANSLATION_API_KEY=sk-ant-xxxxxxxxxxxxx
TRANSLATION_MODEL=claude-3-5-sonnet-20241022
TRANSLATION_BASE_URL=https://api.anthropic.com
```

**Using Azure OpenAI:**
```bash
TRANSLATION_API_KEY=your_azure_key
TRANSLATION_MODEL=gpt-4
TRANSLATION_BASE_URL=https://your-resource.openai.azure.com
```

**Using Custom API Endpoint:**
```bash
TRANSLATION_API_KEY=your_custom_key
TRANSLATION_MODEL=custom-model
TRANSLATION_BASE_URL=https://your-api.example.com/v1
```

#### Step 3: Start the Server

**Development mode:**
```bash
npm run dev
```

**Production mode:**
```bash
npm start
```

**Using Docker:**
```bash
# Build and run
docker build -t translator-mcp .
docker run -p 3031:3031 --env-file .env translator-mcp

# Or use pre-built image
docker run -p 3031:3031 \
  -e TRANSLATION_API_KEY=your_key \
  -e TRANSLATION_MODEL=your_model \
  -e TRANSLATION_BASE_URL=your_url \
  wizdy/airylark-mcp-server
```

**Using Docker Compose:**
```yaml
# docker-compose.yml
version: '3.8'
services:
  translator:
    image: wizdy/airylark-mcp-server
    ports:
      - "3031:3031"
    environment:
      - TRANSLATION_API_KEY=${TRANSLATION_API_KEY}
      - TRANSLATION_MODEL=${TRANSLATION_MODEL}
      - TRANSLATION_BASE_URL=${TRANSLATION_BASE_URL}
    restart: unless-stopped
```

```bash
# Start with docker-compose
docker-compose up -d
```

#### Step 4: Configure Claude to Use Self-Hosted Server

Update your Claude configuration to point to your local server:

```json
{
  "mcpServers": {
    "translator": {
      "url": "http://localhost:3031/sse"
    }
  }
}
```

Or if running on a different machine:
```json
{
  "mcpServers": {
    "translator": {
      "url": "http://your-server-ip:3031/sse"
    }
  }
}
```

#### Step 5: Verify Installation

Test the server is running:

```bash
# Check server health
curl http://localhost:3031/health

# Expected response: {"status":"ok"}
```

In Claude, verify MCP tools are available:
```
List available MCP tools
```

You should see:
- ✅ `translate_text`
- ✅ `evaluate_translation`

---

## Using the MCP Server

### Tool 1: translate_text

**Purpose**: Translate text with professional quality

**Parameters:**
- `text` (required): The text to translate
- `target_language` (required): Target language code (`'zh'`, `'en'`, `'fr'`, `'ko'`, `'ja'`, `'de'`)
- `source_language` (optional): Source language code (auto-detected if not provided)
- `high_quality` (optional): Enable three-stage workflow (default: `true`)

**Example Usage in Skill:**

```markdown
# Translating article content to Chinese
translate_text(
  text: "# Building React Apps\n\nReact is a powerful library for building user interfaces...",
  target_language: "zh",
  source_language: "en",
  high_quality: true
)
```

**Output:**
```markdown
# 构建 React 应用

React 是一个用于构建用户界面的强大库...
```

**Performance:**
- Short articles (<1000 words): 3-5 seconds
- Medium articles (1000-3000 words): 5-10 seconds
- Long articles (3000+ words): 10-20 seconds

### Tool 2: evaluate_translation

**Purpose**: Assess translation quality

**Parameters:**
- `original_text` (required): Source text
- `translated_text` (required): Translated text
- `detailed_feedback` (optional): Get detailed analysis (default: `false`)

**Example Usage:**

```markdown
evaluate_translation(
  original_text: "React is a JavaScript library for building user interfaces.",
  translated_text: "React 是一个用于构建用户界面的 JavaScript 库。",
  detailed_feedback: true
)
```

**Output:**
```json
{
  "overall_score": 95,
  "accuracy": {
    "score": 98,
    "feedback": "Perfect semantic equivalence"
  },
  "fluency": {
    "score": 95,
    "feedback": "Natural Chinese expression, proper technical term usage"
  },
  "terminology": {
    "score": 100,
    "feedback": "Correct technical terms: 'JavaScript 库', '用户界面'"
  },
  "style": {
    "score": 90,
    "feedback": "Maintains professional tone suitable for technical documentation"
  }
}
```

---

## Integration with Fumadocs Article Importer

### How the Skill Uses MCP

When you run the skill, it automatically:

1. **Detects MCP availability**:
   ```
   Checking for translator MCP server...
   ✅ Translator MCP found and ready
   ```

2. **Translates each language**:
   ```
   Translating to Chinese (zh)...
   ├─ Stage 1: Analyzing content and extracting terminology
   ├─ Stage 2: Translating segments with context
   └─ Stage 3: Reviewing full text for consistency
   ✅ Chinese translation complete (6.2 seconds)

   Translating to French (fr)...
   ✅ French translation complete (5.8 seconds)

   Translating to Korean (ko)...
   ✅ Korean translation complete (7.1 seconds)
   ```

3. **Optional quality check**:
   ```
   Evaluating Chinese translation quality...
   ✅ Score: 94/100 (Accuracy: 96, Fluency: 93, Terminology: 95, Style: 92)
   ```

### Workflow Comparison

**With MCP Server:**
```
Total time for 3 languages: ~19 seconds
Quality: Professional-grade with terminology consistency
Cost: Optimized API usage
```

**Without MCP (Claude fallback):**
```
Total time for 3 languages: ~90 seconds
Quality: Good, but may lack terminology consistency
Cost: Higher token usage
```

---

## Troubleshooting

### Issue 1: MCP Server Not Detected

**Symptoms:**
```
⚠️  Translator MCP not found, using Claude fallback
```

**Solutions:**

1. **Verify configuration file exists**:
   ```bash
   # Check Claude Desktop config
   cat ~/Library/Application\ Support/Claude/claude_desktop_config.json

   # Check Claude Code config
   cat ~/.claude/config.json
   ```

2. **Verify JSON syntax**:
   ```bash
   # Validate JSON
   python3 -m json.tool your_config.json
   ```

3. **Restart Claude**:
   - Close and reopen Claude Desktop
   - Or restart Claude Code CLI

4. **Check server is running** (if self-hosted):
   ```bash
   curl http://localhost:3031/health
   ```

### Issue 2: Translation Quality Issues

**Symptoms:**
- Incorrect technical terms
- Broken Markdown syntax
- Inconsistent terminology

**Solutions:**

1. **Enable high_quality mode** (should be default):
   ```
   high_quality: true
   ```

2. **Use evaluate_translation** to identify issues:
   ```
   evaluate_translation(original_text, translated_text, detailed_feedback: true)
   ```

3. **Check source content**:
   - Ensure source is clean Markdown
   - Remove any HTML or complex formatting
   - Verify code blocks are properly formatted

### Issue 3: Slow Translation

**Symptoms:**
- Taking >20 seconds per language

**Solutions:**

1. **Check API rate limits**:
   - OpenAI: Check your rate limit tier
   - Azure: Verify TPM (tokens per minute) quota

2. **Reduce article size**:
   - Split very long articles (>5000 words)
   - Remove unnecessary content before translation

3. **Use faster model** (if quality permits):
   ```bash
   # In .env file
   TRANSLATION_MODEL=gpt-3.5-turbo  # Faster than gpt-4
   ```

### Issue 4: Connection Errors

**Symptoms:**
```
Error: Failed to connect to MCP server
```

**Solutions:**

1. **Check network connectivity**:
   ```bash
   ping airylark-mcp.vcorp.ai
   ```

2. **Verify firewall settings**:
   - Allow outbound connections to port 3031
   - Check corporate firewall/proxy settings

3. **Check server logs** (if self-hosted):
   ```bash
   # Docker logs
   docker logs translator-mcp

   # Or check application logs
   tail -f logs/translator.log
   ```

### Issue 5: API Key Errors

**Symptoms:**
```
Error: Invalid API key
Error: Unauthorized
```

**Solutions:**

1. **Verify API key is correct**:
   ```bash
   # Check .env file
   cat .env | grep TRANSLATION_API_KEY
   ```

2. **Check API key permissions**:
   - Ensure key has access to required model
   - Verify key is not expired

3. **Test API key directly**:
   ```bash
   curl https://api.openai.com/v1/models \
     -H "Authorization: Bearer $TRANSLATION_API_KEY"
   ```

---

## Performance Optimization

### For Large-Scale Imports

**If importing 50+ articles:**

1. **Use self-hosted server**:
   - Better control over rate limits
   - Dedicated resources
   - No public server throttling

2. **Configure optimal model**:
   ```bash
   # Balance speed and quality
   TRANSLATION_MODEL=gpt-4-turbo  # Faster than gpt-4, better than gpt-3.5
   ```

3. **Implement caching** (future enhancement):
   - Cache common technical terms
   - Reuse translations for similar content

4. **Batch processing**:
   - Process articles in batches of 5-10
   - Allow cooldown between batches to avoid rate limits

### For Best Quality

**For critical documentation:**

1. **Enable detailed evaluation**:
   ```
   evaluate_translation(
     original_text,
     translated_text,
     detailed_feedback: true
   )
   ```

2. **Use best model**:
   ```bash
   TRANSLATION_MODEL=gpt-4  # or claude-3-opus (highest quality)
   ```

3. **Manual review workflow**:
   - Generate translations with MCP
   - Review evaluation scores
   - Manually review articles with score <90

---

## Advanced Configuration

### Custom Translation Models

You can use any OpenAI-compatible API:

**LM Studio (local models):**
```bash
TRANSLATION_API_KEY=lm-studio
TRANSLATION_MODEL=local-model
TRANSLATION_BASE_URL=http://localhost:1234/v1
```

**Ollama:**
```bash
TRANSLATION_API_KEY=ollama
TRANSLATION_MODEL=llama2
TRANSLATION_BASE_URL=http://localhost:11434/v1
```

**Together AI:**
```bash
TRANSLATION_API_KEY=your_together_key
TRANSLATION_MODEL=meta-llama/Llama-2-70b-chat-hf
TRANSLATION_BASE_URL=https://api.together.xyz/v1
```

### Environment-Specific Configs

**Development:**
```bash
# Fast, cheap model for testing
TRANSLATION_MODEL=gpt-3.5-turbo
PORT=3031
```

**Staging:**
```bash
# Balanced model
TRANSLATION_MODEL=gpt-4-turbo
PORT=3032
```

**Production:**
```bash
# Best quality model
TRANSLATION_MODEL=gpt-4
PORT=3033
```

---

## Security Best Practices

### API Key Management

1. **Never commit .env files**:
   ```bash
   # Add to .gitignore
   echo ".env" >> .gitignore
   ```

2. **Use environment variables in production**:
   ```bash
   # Export from secure vault
   export TRANSLATION_API_KEY=$(vault read -field=api_key secret/translator)
   ```

3. **Rotate keys regularly**:
   - Change API keys every 90 days
   - Use different keys for dev/staging/prod

### Network Security

1. **Use HTTPS** for remote servers:
   ```json
   {
     "url": "https://your-server.com/sse"  // Not http://
   }
   ```

2. **Implement authentication** (if self-hosting for team):
   - Add API key validation in server
   - Use VPN for internal access

3. **Rate limiting**:
   - Configure rate limits to prevent abuse
   - Monitor API usage

---

## Monitoring and Logging

### Server Logs

**Enable detailed logging:**
```bash
# In .env
LOG_LEVEL=debug
LOG_FILE=logs/translator.log
```

**Monitor logs:**
```bash
# Real-time monitoring
tail -f logs/translator.log

# Search for errors
grep "ERROR" logs/translator.log

# Count translations
grep "Translation complete" logs/translator.log | wc -l
```

### Performance Metrics

**Track translation performance:**
```bash
# Average translation time
grep "Translation complete" logs/translator.log | \
  awk '{sum+=$NF; count++} END {print sum/count " seconds"}'

# Success rate
grep -c "Translation complete" logs/translator.log
grep -c "Translation failed" logs/translator.log
```

---

## Cost Estimation

### Using OpenAI API

**Approximate costs per article** (2000 words):

**GPT-4:**
- Input: ~3000 tokens × $0.03/1K = $0.09
- Output: ~3000 tokens × $0.06/1K = $0.18
- **Total per language**: ~$0.27
- **Total for 4 languages**: ~$1.08

**GPT-4 Turbo:**
- Input: ~3000 tokens × $0.01/1K = $0.03
- Output: ~3000 tokens × $0.03/1K = $0.09
- **Total per language**: ~$0.12
- **Total for 4 languages**: ~$0.48

**GPT-3.5 Turbo:**
- **Total per language**: ~$0.02
- **Total for 4 languages**: ~$0.08

### Using Anthropic API

**Claude 3.5 Sonnet:**
- **Total per language**: ~$0.15
- **Total for 4 languages**: ~$0.60

### Cost Optimization Tips

1. **Batch similar content** - Reuse terminology
2. **Cache translations** - Avoid re-translating
3. **Choose appropriate model** - Don't over-engineer
4. **Monitor usage** - Set API spending limits

---

## Version History

- **v1.0.0** (2025-11-15): Initial MCP integration guide
  - Support for public and self-hosted servers
  - Configuration examples for multiple API providers
  - Troubleshooting guide
  - Performance optimization tips

---

**Last Updated**: 2025-11-15
**MCP Server**: https://github.com/foreveryh/translator-mcp-server
**Maintained by**: Fumadocs Article Importer Skill
