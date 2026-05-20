# Contributing to SURIOTA Website Toolkit

Terima kasih atas minat Anda untuk berkontribusi pada SURIOTA Website Toolkit.

## Development Workflow

### 1. Setup Environment

```bash
# Clone repo
git clone https://github.com/GifariKemal/suriota-website-toolkit.git
cd suriota-website-toolkit

# Install dependencies
npm install

# Setup Playwright (jika perlu screenshot)
npx playwright install
```

### 2. Branch Naming

Gunakan format berikut:

| Prefix | Kegunaan | Contoh |
|:-------|:---------|:-------|
| `feature/` | Fitur baru | `feature/seo-audit-script` |
| `fix/` | Bug fix | `fix/backup-path-error` |
| `docs/` | Dokumentasi | `docs/readme-update` |
| `refactor/` | Refactor | `refactor/cleanup-scripts` |

### 3. Commit Convention

Gunakan [Conventional Commits](https://conventionalcommits.org):

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat` — Fitur baru
- `fix` — Perbaikan bug
- `docs` — Perubahan dokumentasi
- `style` — Formatting, tanpa perubahan kode
- `refactor` — Refactor kode
- `test` — Menambah test
- `chore` — Maintenance tasks

**Contoh:**
```
feat(tools): add bulk image optimizer script

- Support WebP conversion
- Auto-resize untuk breakpoint mobile/desktop
- Integrasi dengan Elementor media library

Closes #12
```

### 4. Code Standards

**Python:**
- Gunakan PEP 8
- Type hints untuk function signatures
- Docstring untuk public functions

**JavaScript:**
- ES6+ syntax
- Async/await untuk operasi asynchronous
- Error handling dengan try/catch

### 5. Testing

Sebelum commit:
```bash
# Test Python scripts
python -m py_compile tools/py/*.py

# Test Node scripts
node --check tools/js/*.js
```

### 6. Pull Request

1. Update README.md jika ada perubahan fitur
2. Pastikan tidak ada file temporary (`_*.py`, `_*.js`)
3. Deskripsikan perubahan dengan jelas di PR description
4. Link ke issue terkait jika ada

## Code Review

Semua PR akan direview dalam 24-48 jam. Maintainer berhak:
- Request changes
- Merge setelah approval
- Close PR yang tidak sesuai guideline

## Questions?

Hubungi tim engineering SURIOTA via email: info@suriota.com
