# Jina MCP Server Integration Guide

This document provides detailed instructions for integrating the Jina MCP Server with the Fumadocs Article Importer Skill.

## Overview

The Jina MCP Server (https://github.com/jina-ai/MCP) provides 15 powerful tools for content extraction, search, and processing. For our article importer, we primarily use:

1. **`read_url`** - Convert web pages to clean markdown
2. **`guess_datetime_url`** - Extract publication/update dates
3. **`search_web`** - Optional: Find related articles

**Benefits over Direct API/Scraping:**
- 🎯 **Clean Markdown Output**: Automatically converts HTML to markdown
- 📅 **Date Detection**: Intelligent publication date extraction
- 🚀 **No Rate Limits** (with API key): Free tier available
- 🔄 **15+ Tools Available**: Search, ranking, deduplication capabilities
- 🛠️ **MCP Standard**: Works seamlessly with Claude

---

## All Available Tools

### Content Extraction (Primary Use)
1. **`read_url`** ⭐ - Convert webpage to markdown
   - Parameters: `url` (string)
   - Returns: Clean markdown content
   - Usage: Main article fetching

2. **`capture_screenshot_url`** - Take webpage screenshot
   - Parameters: `url` (string)
   - Returns: Screenshot image
   - Usage: Visual documentation

3. **`guess_datetime_url`** ⭐ - Analyze publish/update dates
   - Parameters: `url` (string)
   - Returns: Detected dates (publish, update)
   - Usage: Get article metadata

### Search Tools
4. **`search_web`** - General web search
5. **`search_arxiv`** - Academic paper search
6. **`search_images`** - Image search
7. **`expand_query`** - Query expansion and rewriting

### Parallel Processing (Efficiency)
8. **`parallel_read_url`** - Read multiple URLs simultaneously
9. **`parallel_search_web`** - Parallel web search
10. **`parallel_search_arxiv`** - Parallel academic search

### Ranking & Processing
11. **`sort_by_relevance`** - Document reranking
12. **`deduplicate_strings`** - Semantic text deduplication
13. **`deduplicate_images`** - Semantic image deduplication

### Utility
14. **`primer`** - Contextual information (time/location aware)

---

## Setup Options

### Option 1: Public Jina MCP Server (Recommended) 🚀

**Easiest option** - Hosted by Jina AI!

#### Configuration

**For Claude Desktop:**

Edit Claude configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
**Linux**: `~/.config/Claude/claude_desktop_config.json`

**Without API Key** (Rate limited but free):
```json
{
  "mcpServers": {
    "jina": {
      "url": "https://mcp.jina.ai/sse"
    }
  }
}
```

**With API Key** (Recommended - no rate limits):
```json
{
  "mcpServers": {
    "jina": {
      "url": "https://mcp.jina.ai/sse",
      "headers": {
        "Authorization": "Bearer jina_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
      }
    }
  }
}
```

**For Claude Code CLI:**
```bash
# Edit config
vim ~/.claude/config.json
```

Add:
```json
{
  "mcpServers": {
    "jina": {
      "url": "https://mcp.jina.ai/sse",
      "headers": {
        "Authorization": "Bearer ${JINA_API_KEY}"
      }
    }
  }
}
```

**For Cursor:**
```json
{
  "mcp": {
    "servers": {
      "jina": {
        "url": "https://mcp.jina.ai/sse",
        "headers": {
          "Authorization": "Bearer ${JINA_API_KEY}"
        }
      }
    }
  }
}
```

#### Get API Key

1. Visit https://jina.ai
2. Sign up for free account
3. Navigate to API Keys section
4. Create new API key
5. Copy key (format: `jina_xxxxxxxxxxxx`)

**Free Tier Limits**:
- 1M tokens/month for Reader API
- Sufficient for 50-100 article imports/month
- No credit card required

---

### Option 2: Self-Hosted Jina MCP 🔒

**Best for**: Privacy, unlimited usage, custom modifications

#### Installation

**Step 1: Clone Repository**
```bash
git clone https://github.com/jina-ai/MCP.git
cd MCP
```

**Step 2: Install Dependencies**
```bash
npm install
```

**Step 3: Configure Environment**

Create `.env` file:
```bash
# Optional: Jina API key for backend calls
JINA_API_KEY=jina_your_api_key_here

# Server port (default: 3000)
PORT=3000
```

**Step 4: Start Server**

```bash
# Development mode
npm run dev

# Production mode
npm start
```

**Step 5: Configure Claude**

Point to your local server:
```json
{
  "mcpServers": {
    "jina": {
      "url": "http://localhost:3000/sse"
    }
  }
}
```

#### Docker Deployment

**Using Docker:**
```bash
# Build image
docker build -t jina-mcp .

# Run container
docker run -d \
  -p 3000:3000 \
  -e JINA_API_KEY=your_key \
  --name jina-mcp \
  jina-mcp
```

**Using Docker Compose:**
```yaml
# docker-compose.yml
version: '3.8'
services:
  jina-mcp:
    build: .
    ports:
      - "3000:3000"
    environment:
      - JINA_API_KEY=${JINA_API_KEY}
      - PORT=3000
    restart: unless-stopped
```

```bash
docker-compose up -d
```

---

## Using Jina MCP Tools

### Tool 1: read_url (Primary Tool) ⭐

**Purpose**: Convert web pages to clean markdown

**Parameters**:
- `url` (required): The webpage URL to convert

**Returns**: Markdown-formatted content

**Example Usage:**

```markdown
# Fetch article content
read_url(url: "https://dev.to/username/react-hooks-tutorial")
```

**Output:**
```markdown
# React Hooks Complete Guide

React Hooks are a new addition in React 16.8. They let you use state and other React features without writing a class.

## What are Hooks?

Hooks are functions that let you "hook into" React state and lifecycle features from function components...

![React Hooks Diagram](https://example.com/image.png)
```

**Features**:
- ✅ Clean markdown output
- ✅ Preserves images with alt text
- ✅ Maintains heading hierarchy
- ✅ Removes ads, navigation, footers
- ✅ Code blocks properly formatted

### Tool 2: guess_datetime_url 📅

**Purpose**: Extract publication and update dates from webpages

**Parameters**:
- `url` (required): The webpage URL

**Returns**: Detected dates in structured format

**Example Usage:**

```markdown
guess_datetime_url(url: "https://dev.to/username/article")
```

**Output:**
```json
{
  "published": "2025-11-10T14:30:00Z",
  "updated": "2025-11-12T09:15:00Z",
  "confidence": "high"
}
```

**Use Case in Skill**:
- Populate `published_date` field in frontmatter
- Determine article freshness
- Archive organization by date

### Tool 3: search_web 🔍

**Purpose**: Search the web for related content

**Parameters**:
- `query` (required): Search query

**Returns**: List of search results with titles, URLs, snippets

**Example Usage:**

```markdown
search_web(query: "React hooks tutorial beginner")
```

**Output:**
```json
{
  "results": [
    {
      "title": "React Hooks for Beginners - Complete Guide",
      "url": "https://example.com/react-hooks-guide",
      "snippet": "Learn React Hooks from scratch with this comprehensive tutorial..."
    },
    {
      "title": "Understanding useState and useEffect",
      "url": "https://example.com/useState-useEffect",
      "snippet": "Deep dive into the most commonly used React Hooks..."
    }
  ]
}
```

**Potential Use Cases**:
- Find related articles to import
- Discover source material
- Validate article uniqueness

---

## Integration with Fumadocs Article Importer

### How the Skill Uses Jina MCP

**Step-by-Step Workflow:**

1. **User provides URL**:
   ```
   URL: https://example.com/my-technical-article
   ```

2. **Skill fetches content with read_url**:
   ```
   read_url(url: "https://example.com/my-technical-article")

   ✅ Returns clean markdown (3.2 seconds)
   ```

3. **Skill gets publication date**:
   ```
   guess_datetime_url(url: "https://example.com/my-technical-article")

   ✅ Found: published: 2025-11-05
   ```

4. **Skill extracts metadata**:
   ```
   Title: "Building REST APIs with FastAPI"
   Author: Extracted from markdown or "Unknown"
   Date: 2025-11-05
   Content: Full markdown body
   Images: 5 images found
   ```

5. **Continue with translation and MDX generation**

### Workflow Comparison

**With Jina MCP:**
```
Article fetching: ~3 seconds
Date extraction: ~1 second
Clean markdown: ✅ Ready for processing
Image URLs: ✅ Automatically extracted
Total: ~4 seconds
```

**Without Jina MCP (using curl):**
```
Article fetching: ~5 seconds
Date extraction: Manual parsing needed
Clean markdown: ❌ May have HTML artifacts
Image URLs: Manual extraction
Total: ~10+ seconds + manual work
```

---

## Advanced Usage

### Batch Article Import

Use `parallel_read_url` to fetch multiple articles:

```markdown
parallel_read_url(
  urls: [
    "https://example.com/article-1",
    "https://example.com/article-2",
    "https://example.com/article-3"
  ]
)
```

**Benefits**:
- ⚡ 3x faster than sequential reads
- 🎯 Consistent formatting across all articles
- 📊 Batch processing for large imports

### Content Quality Check

Before importing, search for similar content:

```markdown
# Check if article already exists in your docs
search_web(query: "site:yourdocs.com React Hooks tutorial")
```

### Related Article Discovery

Find similar articles to import:

```markdown
# Find related content
search_web(query: "React Hooks advanced patterns")

# Filter by recency
search_web(query: "React Hooks 2025")
```

---

## Troubleshooting

### Issue 1: MCP Server Not Detected

**Symptoms:**
```
⚠️  Jina MCP not found, falling back to curl
```

**Solutions:**

1. **Verify configuration**:
   ```bash
   # Check config file exists
   cat ~/Library/Application\ Support/Claude/claude_desktop_config.json

   # Validate JSON
   python3 -m json.tool claude_desktop_config.json
   ```

2. **Restart Claude**:
   - Close completely and reopen
   - Or restart CLI session

3. **Test connection**:
   ```bash
   # For self-hosted
   curl http://localhost:3000/health
   ```

### Issue 2: Rate Limit Errors

**Symptoms:**
```
Error: Rate limit exceeded
```

**Solutions:**

1. **Get API key** from https://jina.ai (free tier: 1M tokens/month)

2. **Add to configuration**:
   ```json
   "headers": {
     "Authorization": "Bearer jina_your_api_key"
   }
   ```

3. **Or self-host** for unlimited usage

### Issue 3: Poor Markdown Quality

**Symptoms:**
- HTML tags in output
- Missing content
- Broken formatting

**Solutions:**

1. **Check source URL**:
   - Ensure URL is publicly accessible
   - No login required
   - No paywall

2. **Try different URL format**:
   ```
   ❌ https://example.com/article?utm_source=...
   ✅ https://example.com/article
   ```

3. **Fallback to Jina Reader API**:
   ```bash
   curl "https://r.jina.ai/https://example.com/article"
   ```

### Issue 4: Date Detection Fails

**Symptoms:**
```
guess_datetime_url returns: null or low confidence
```

**Solutions:**

1. **Check article metadata**:
   - Some sites don't include structured dates
   - Older articles may lack metadata

2. **Fallback strategy**:
   - Use current date
   - Extract from URL (e.g., /2025/11/article)
   - Manual input from user

3. **Manual override**:
   ```markdown
   Ask user: "What is the publication date for this article?"
   ```

### Issue 5: Images Not Extracted

**Symptoms:**
- No image URLs found in markdown

**Solutions:**

1. **Check image format in source**:
   - JavaScript-loaded images may not be captured
   - Background images won't be extracted

2. **Manual extraction**:
   ```bash
   # Use grep to find image URLs
   curl "https://r.jina.ai/URL" | grep -o '!\[.*\](.*)'
   ```

3. **Alternative approach**:
   - Use `capture_screenshot_url` to get visual
   - Or skip image download for this article

---

## Performance Optimization

### For Large-Scale Imports

**Batch Processing with parallel_read_url:**

```markdown
# Import 10 articles in one call
parallel_read_url(
  urls: [url1, url2, url3, ..., url10]
)

Time: ~5 seconds (vs 30 seconds sequential)
Speedup: 6x faster
```

**Recommended Batch Sizes:**
- Small articles (<2000 words): 10-15 URLs per batch
- Large articles (>5000 words): 3-5 URLs per batch
- Mixed: 5-10 URLs per batch

### Caching Strategy

**For repeated access:**

```bash
# Cache read_url results locally
mkdir -p .cache/jina/

# Save results
echo "$MARKDOWN_OUTPUT" > .cache/jina/$(echo $URL | md5).md

# Check cache before calling MCP
if [ -f ".cache/jina/$URL_HASH.md" ]; then
  # Use cached version
fi
```

### Rate Limit Management

**With API Key:**
- 1M tokens/month free
- ~500 articles/month (avg 2000 words each)
- Monitor usage at https://jina.ai/dashboard

**Without API Key:**
- Rate limited per IP
- ~50-100 requests/hour
- Consider self-hosting for production

---

## API Key Management

### Getting Your API Key

1. **Sign up at https://jina.ai**
2. **Navigate to "API Keys"**
3. **Create new key**:
   - Name: "Fumadocs Article Importer"
   - Scope: Reader API
4. **Copy key** (format: `jina_xxxxxxxxxxxxx`)
5. **Store securely**

### Environment Variable Setup

**For Claude Desktop:**
```bash
# macOS/Linux - Add to shell profile
echo 'export JINA_API_KEY="jina_xxxxx"' >> ~/.zshrc
source ~/.zshrc
```

**For Docker:**
```bash
# Use docker secrets or env file
echo "JINA_API_KEY=jina_xxxxx" > .env.jina
docker run --env-file .env.jina ...
```

### Security Best Practices

1. **Never commit API keys**:
   ```bash
   # Add to .gitignore
   echo ".env" >> .gitignore
   echo ".env.jina" >> .gitignore
   ```

2. **Use environment variables**:
   ```json
   {
     "headers": {
       "Authorization": "Bearer ${JINA_API_KEY}"
     }
   }
   ```

3. **Rotate keys regularly**:
   - Change every 90 days
   - Immediately if exposed

4. **Monitor usage**:
   - Check dashboard weekly
   - Set alerts for unusual activity

---

## Comparison: Jina MCP vs Jina API

### Jina MCP (Recommended)

**Pros:**
- ✅ Seamless Claude integration
- ✅ 15+ tools available
- ✅ No command execution needed
- ✅ Consistent interface
- ✅ Better error handling

**Cons:**
- ❌ Requires MCP configuration
- ❌ One more service to manage

**Best For:**
- Claude Desktop/Code CLI users
- Interactive workflows
- Multi-tool usage

### Jina API (Direct curl)

**Pros:**
- ✅ Simple HTTP requests
- ✅ No MCP setup needed
- ✅ Works anywhere curl works
- ✅ Easy debugging

**Cons:**
- ❌ Less integration with Claude
- ❌ Manual parsing needed
- ❌ Only Reader API access
- ❌ No date detection

**Best For:**
- Scripts and automation
- Non-Claude environments
- Simple use cases

---

## Example Configurations

### Complete Claude Configuration

**With both Jina and Translator MCP:**

```json
{
  "mcpServers": {
    "jina": {
      "url": "https://mcp.jina.ai/sse",
      "headers": {
        "Authorization": "Bearer ${JINA_API_KEY}"
      }
    },
    "translator": {
      "url": "https://airylark-mcp.vcorp.ai/sse"
    }
  }
}
```

### Self-Hosted Both Services

```json
{
  "mcpServers": {
    "jina": {
      "url": "http://localhost:3000/sse"
    },
    "translator": {
      "url": "http://localhost:3031/sse"
    }
  }
}
```

### Production Setup (Docker Compose)

```yaml
version: '3.8'
services:
  jina-mcp:
    image: jina-mcp:latest
    ports:
      - "3000:3000"
    environment:
      - JINA_API_KEY=${JINA_API_KEY}
    restart: unless-stopped

  translator-mcp:
    image: wizdy/airylark-mcp-server
    ports:
      - "3031:3031"
    environment:
      - TRANSLATION_API_KEY=${TRANSLATION_API_KEY}
      - TRANSLATION_MODEL=gpt-4-turbo
      - TRANSLATION_BASE_URL=${TRANSLATION_BASE_URL}
    restart: unless-stopped
```

```bash
# Start both services
docker-compose up -d

# Configure Claude to use local services
vim ~/.claude/config.json
# Set URLs to http://localhost:3000/sse and http://localhost:3031/sse
```

---

## Monitoring and Logging

### Check MCP Tool Availability

In Claude, verify tools are loaded:

```
List all available MCP tools
```

Expected output:
```
Jina MCP Tools:
✅ read_url
✅ guess_datetime_url
✅ search_web
✅ parallel_read_url
... (11 more)

Translator MCP Tools:
✅ translate_text
✅ evaluate_translation
```

### Monitor Usage

**For Public Jina MCP:**
- Visit https://jina.ai/dashboard
- View token usage
- Check remaining quota

**For Self-Hosted:**
```bash
# Check logs
docker logs jina-mcp

# Monitor requests
tail -f logs/jina-mcp.log | grep "read_url"

# Count successful calls
grep "read_url success" logs/jina-mcp.log | wc -l
```

---

## Cost Estimation

### Using Public Jina MCP

**Free Tier:**
- 1M tokens/month
- ~500 articles (2000 words avg)
- No credit card required

**Paid Tiers** (if you exceed free tier):
- Small: $20/month - 5M tokens
- Medium: $50/month - 15M tokens
- Large: $100/month - 50M tokens

### Self-Hosted Costs

**Infrastructure:**
- VPS: $5-10/month (Digital Ocean, Linode)
- Docker container: ~512MB RAM, minimal CPU
- Bandwidth: Negligible for <1000 articles/month

**Total**: $5-10/month for unlimited usage

---

## Version History

- **v1.0.0** (2025-11-15): Initial Jina MCP integration guide
  - Configuration for public and self-hosted servers
  - Tool usage documentation
  - Troubleshooting guide
  - Performance optimization tips
  - Complete examples

---

**Last Updated**: 2025-11-15
**Jina MCP**: https://github.com/jina-ai/MCP
**Jina AI**: https://jina.ai
**Maintained by**: Fumadocs Article Importer Skill
