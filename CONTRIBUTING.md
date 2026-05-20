# Contributing to SURIOTA Website Toolkit

Thank you for your interest in contributing to the SURIOTA Website Toolkit.

## Development Workflow

### 1. Environment Setup

```bash
# Clone repo
git clone https://github.com/GifariKemal/suriota-website-toolkit.git
cd suriota-website-toolkit

# Install dependencies
npm install

# Setup Playwright (if screenshot needed)
npx playwright install
```

### 2. Branch Naming

Use the following format:

| Prefix | Purpose | Example |
|:-------|:--------|:--------|
| `feature/` | New feature | `feature/seo-audit-script` |
| `fix/` | Bug fix | `fix/backup-path-error` |
| `docs/` | Documentation | `docs/readme-update` |
| `refactor/` | Refactor | `refactor/cleanup-scripts` |

### 3. Commit Convention

Use [Conventional Commits](https://conventionalcommits.org):

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat` — New feature
- `fix` — Bug fix
- `docs` — Documentation changes
- `style` — Formatting, no code change
- `refactor` — Code refactoring
- `test` — Adding tests
- `chore` — Maintenance tasks

**Example:**
```
feat(tools): add bulk image optimizer script

- Support WebP conversion
- Auto-resize for mobile/desktop breakpoints
- Integrate with Elementor media library

Closes #12
```

### 4. Code Standards

**Python:**
- Follow PEP 8
- Use type hints for function signatures
- Add docstrings for public functions

**JavaScript:**
- ES6+ syntax
- Async/await for asynchronous operations
- Error handling with try/catch

### 5. Testing

Before committing:
```bash
# Test Python scripts
python -m py_compile tools/py/*.py

# Test Node scripts
node --check tools/js/*.js
```

### 6. Pull Request

1. Update README.md if features change
2. Ensure no temporary files (`_*.py`, `_*.js`) are committed
3. Describe changes clearly in PR description
4. Link to related issues if any

## Code Review

All PRs will be reviewed within 24-48 hours. Maintainers may:
- Request changes
- Merge after approval
- Close PRs that do not follow guidelines

## Questions?

Contact the SURIOTA engineering team: info@suriota.com
