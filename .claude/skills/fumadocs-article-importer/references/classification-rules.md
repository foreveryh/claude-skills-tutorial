# Article Classification Rules

This document defines the rules for automatically classifying articles into categories, difficulty levels, and tags.

## Categories (8 Total)

### 1. development
**Name**: Development & Code

**Description**: Software development, programming languages, frameworks, and tools

**Keywords to Match**:
- Primary: code, programming, framework, library, API, development, build, software
- Languages: javascript, typescript, python, go, rust, java, php, ruby
- Frameworks: react, vue, angular, svelte, django, fastapi, express, nextjs
- Tools: git, npm, webpack, vite, babel, eslint

**Example Titles**:
- "Building a REST API with FastAPI"
- "React Hooks Complete Guide"
- "Git Workflow Best Practices"

---

### 2. data
**Name**: Data & Analytics

**Description**: Data processing, analysis, visualization, and databases

**Keywords to Match**:
- Primary: data, analytics, visualization, database, SQL, charts, statistics, query
- Tools: pandas, numpy, matplotlib, d3.js, tableau, excel
- Databases: postgresql, mongodb, mysql, redis, sqlite
- Concepts: ETL, data warehouse, data pipeline, BI

**Example Titles**:
- "Data Visualization with D3.js"
- "PostgreSQL Performance Tuning"
- "Pandas Data Analysis Tutorial"

---

### 3. ai-ml
**Name**: AI & Machine Learning

**Description**: Artificial intelligence, machine learning, and deep learning

**Keywords to Match**:
- Primary: AI, machine learning, ML, deep learning, neural network, NLP, GPT, model, training
- Frameworks: tensorflow, pytorch, keras, scikit-learn, transformers
- Concepts: supervised, unsupervised, reinforcement, CNN, RNN, transformer
- Applications: chatbot, LLM, computer vision, NLP, recommendation

**Example Titles**:
- "Building a Chatbot with GPT-4"
- "Introduction to Neural Networks"
- "Fine-tuning LLMs for Specific Tasks"

---

### 4. design
**Name**: Design & Creative

**Description**: UI/UX design, visual design, and creative work

**Keywords to Match**:
- Primary: design, UI, UX, visual, creative, art, graphics, branding
- Tools: figma, sketch, adobe, photoshop, illustrator
- Concepts: typography, color theory, layout, prototyping, wireframe
- Processes: design system, user research, usability, accessibility

**Example Titles**:
- "Designing a Design System with Figma"
- "UI/UX Best Practices for Web Apps"
- "Color Theory for Developers"

---

### 5. content
**Name**: Content & Writing

**Description**: Content creation, writing, research, and documentation

**Keywords to Match**:
- Primary: writing, content, documentation, article, blog, media, transcript, document
- Types: technical writing, copywriting, SEO, storytelling
- Formats: markdown, docx, pdf, video, audio
- Processes: research, editing, publishing, content strategy

**Example Titles**:
- "Technical Writing Best Practices"
- "Creating Engaging Blog Content"
- "Documentation That Developers Love"

---

### 6. business
**Name**: Business & Marketing

**Description**: Business strategy, marketing, and management

**Keywords to Match**:
- Primary: business, marketing, strategy, management, sales, customer, campaign, analytics
- Areas: SEO, SEM, email marketing, social media, growth hacking
- Concepts: funnel, conversion, ROI, KPI, metrics, A/B testing
- Tools: Google Analytics, HubSpot, Salesforce, CRM

**Example Titles**:
- "Digital Marketing Strategy Guide"
- "Building a Sales Funnel"
- "Customer Acquisition Best Practices"

---

### 7. devops
**Name**: DevOps & Infrastructure

**Description**: Operations, deployment, infrastructure, and cloud services

**Keywords to Match**:
- Primary: DevOps, CI/CD, Docker, Kubernetes, cloud, AWS, deployment, infrastructure, monitoring
- Tools: docker, kubernetes, jenkins, github actions, terraform, ansible
- Cloud: AWS, GCP, Azure, vercel, netlify, heroku
- Concepts: container, orchestration, automation, IaC, observability

**Example Titles**:
- "Docker and Kubernetes Tutorial"
- "Building a CI/CD Pipeline"
- "AWS Infrastructure as Code with Terraform"

---

### 8. security
**Name**: Security & Testing

**Description**: Security analysis, testing, and quality assurance

**Keywords to Match**:
- Primary: security, testing, QA, debugging, vulnerability, penetration, audit, test automation
- Types: unit testing, integration testing, E2E testing, penetration testing
- Tools: jest, pytest, playwright, cypress, selenium
- Security: encryption, authentication, authorization, OWASP, XSS, SQL injection

**Example Titles**:
- "Web Application Security Best Practices"
- "Automated Testing with Playwright"
- "Debugging Node.js Applications"

---

## Difficulty Levels (3 Total)

### beginner
**Criteria**:
- Introductory content, "Getting Started" guides
- Explains basic concepts and fundamentals
- Minimal prerequisites required
- Step-by-step instructions with detailed explanations
- Simple code examples

**Indicators**:
- Title contains: "Introduction", "Getting Started", "Basics", "Beginner", "101"
- Explains foundational concepts
- No advanced terminology without explanation
- Comprehensive explanations for each step

**Examples**:
- "Introduction to React Hooks"
- "Python Basics for Beginners"
- "Getting Started with Git"

---

### intermediate
**Criteria**:
- Requires some background knowledge
- Covers best practices and common patterns
- Multi-step workflows
- Moderate technical depth
- Assumes basic familiarity with the topic

**Indicators**:
- Title contains: "Guide", "Tutorial", "Best Practices", "How to"
- Builds on foundational knowledge
- Includes optimization tips
- References related concepts
- Code examples with explanations

**Examples**:
- "React State Management Guide"
- "Building REST APIs with FastAPI"
- "Docker Compose Best Practices"

---

### advanced
**Criteria**:
- Requires professional or expert knowledge
- Complex architecture or system design
- Performance optimization and scaling
- Security hardening
- Integration of multiple technologies
- Deep technical details

**Indicators**:
- Title contains: "Advanced", "Architecture", "Performance", "Scaling", "Deep Dive"
- Assumes expert knowledge
- Complex code patterns
- Production-level considerations
- Discusses tradeoffs and alternatives

**Examples**:
- "Microservices Architecture Patterns"
- "Advanced React Performance Optimization"
- "Scaling PostgreSQL for High Traffic"

---

## Tag Extraction Rules

### Tag Categories

#### 1. Technology Stack (Primary)
Extract the main technologies mentioned:
- **Languages**: javascript, typescript, python, go, rust, java, etc.
- **Frameworks**: react, vue, angular, django, fastapi, express, etc.
- **Libraries**: pandas, numpy, d3.js, lodash, etc.

#### 2. Tools & Platforms
- **Development Tools**: git, vscode, docker, webpack, etc.
- **Cloud Platforms**: aws, gcp, azure, vercel, netlify, etc.
- **Databases**: postgresql, mongodb, mysql, redis, etc.

#### 3. Concepts & Patterns
- **Architecture**: microservices, serverless, monolith, etc.
- **Methodologies**: TDD, agile, CI/CD, etc.
- **Patterns**: REST, GraphQL, MVC, etc.

#### 4. Application Types
- web, mobile, desktop, cli, api, etc.

### Tag Formatting Rules
1. **All lowercase**: Use `machine-learning`, not `Machine-Learning`
2. **Use hyphens**: `machine-learning`, not `machine_learning` or `machineLearning`
3. **Be specific**: `react-hooks` is better than just `react` if hooks are the focus
4. **No duplicates**: Each tag should appear only once
5. **Relevance**: Only include tags directly relevant to the article content

### Tag Count
- **Minimum**: 3 tags
- **Maximum**: 7 tags
- **Recommended**: 4-5 tags

### Tag Priority Order
1. Primary technology (e.g., `react`, `python`)
2. Secondary technologies/frameworks (e.g., `typescript`, `fastapi`)
3. Tools/platforms (e.g., `docker`, `aws`)
4. Concepts (e.g., `api`, `authentication`)
5. Application type (e.g., `web`, `cli`)

---

## Classification Algorithm

### Step 1: Extract Text Features
From the article, extract:
- Title
- First 2-3 paragraphs
- Headings (h1, h2, h3)
- Code block languages (if any)
- Mentioned technologies/tools

### Step 2: Keyword Matching
For each category:
1. Count occurrences of primary keywords
2. Count occurrences of secondary keywords (languages, tools, etc.)
3. Calculate a relevance score

### Step 3: Determine Category
- Select the category with the highest relevance score
- If tie, prefer more specific category:
  - `ai-ml` over `data`
  - `devops` over `development`
  - `security` over `development`

### Step 4: Determine Difficulty
Analyze the article for:
1. **Vocabulary complexity**: Technical jargon vs. explained terms
2. **Prerequisites mentioned**: None, basic, or expert knowledge required
3. **Code complexity**: Simple examples vs. complex patterns
4. **Title indicators**: "Introduction", "Advanced", "Deep Dive", etc.

Assign difficulty based on the majority of indicators.

### Step 5: Extract Tags
1. Identify all mentioned technologies (using keyword lists)
2. Rank by frequency and prominence (title > headings > body)
3. Select top 4-5 most relevant tags
4. Add 1-2 concept/application type tags if appropriate
5. Format according to tag formatting rules
6. Ensure 3-7 tags total

---

## Edge Cases

### Multi-Topic Articles
**Example**: "Building a React App with PostgreSQL and Docker"

**Solution**:
- **Category**: Choose primary focus (likely `development`)
- **Tags**: Include all major technologies (`react`, `postgresql`, `docker`, `web`)

### Ambiguous Difficulty
**Example**: Article has beginner introduction but advanced sections

**Solution**:
- Determine which portion is dominant (% of content)
- If mixed evenly, default to `intermediate`

### No Clear Category Match
**Example**: General productivity or organization article

**Solution**:
- Default to `content` or `business` based on context
- Use descriptive tags to provide clarity

### Too Many Relevant Tags
**Example**: Article mentions 15+ technologies

**Solution**:
- Select only the most prominent 5-7 tags
- Prefer technologies that are the focus, not just mentioned
- Prioritize: primary > secondary > mentioned in passing

---

## Validation Checklist

Before finalizing classification, verify:
- [ ] Category matches at least 3 primary keywords
- [ ] Difficulty aligns with article structure and depth
- [ ] Tags are between 3-7 count
- [ ] All tags are lowercase with hyphens
- [ ] Tags are relevant to main article content
- [ ] No tag duplication
- [ ] At least one technology/language tag included

---

## Examples

### Example 1
**Article Title**: "Building a Real-time Chat App with React and WebSocket"

**Classification**:
- **Category**: `development` (primary focus on building software)
- **Difficulty**: `intermediate` (requires React knowledge)
- **Tags**: `react`, `websocket`, `real-time`, `javascript`, `web`

**Reasoning**: Clear development focus, requires existing React knowledge, multiple technologies involved.

---

### Example 2
**Article Title**: "Introduction to Machine Learning with Python"

**Classification**:
- **Category**: `ai-ml` (machine learning content)
- **Difficulty**: `beginner` ("Introduction" in title)
- **Tags**: `python`, `machine-learning`, `ai`, `scikit-learn`, `tutorial`

**Reasoning**: ML category obvious, beginner level indicated by title, Python is primary language.

---

### Example 3
**Article Title**: "Advanced PostgreSQL Query Optimization Techniques"

**Classification**:
- **Category**: `data` (database focus)
- **Difficulty**: `advanced` ("Advanced" in title, optimization topic)
- **Tags**: `postgresql`, `sql`, `database`, `performance`, `optimization`

**Reasoning**: Data category for database content, advanced difficulty clear from title and topic.

---

### Example 4
**Article Title**: "Deploying Microservices to Kubernetes with Helm"

**Classification**:
- **Category**: `devops` (deployment and infrastructure)
- **Difficulty**: `advanced` (complex architecture, multiple tools)
- **Tags**: `kubernetes`, `microservices`, `helm`, `docker`, `deployment`, `devops`

**Reasoning**: DevOps category for infrastructure, advanced due to complexity, 6 relevant tags.

---

## Updates and Maintenance

This classification system should be reviewed and updated:
- When new technology trends emerge
- If classification accuracy drops below 85%
- When adding new categories
- Based on user feedback on misclassifications

**Last Updated**: 2025-11-15
