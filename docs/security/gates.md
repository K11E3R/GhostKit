# Security Gates Configuration

## Overview

GhostKit implements a multi-layered security gate system to prevent vulnerabilities and enforce code quality. This document details the configuration and customization of these security gates.

## Pre-Commit Hooks

### Installation

Pre-commit hooks are installed automatically when running the setup script:

```bash
./scripts/setup-hooks.sh
```

Alternatively, you can install them manually:

```bash
cp scripts/git-hooks/pre-commit .git/hooks/
chmod +x .git/hooks/pre-commit
```

### Default Configuration

The default pre-commit hook runs the following checks:

1. **Import Sorting (isort)**
   - Profile: black-compatible
   - Ensures consistent import organization

2. **Code Formatting (black)**
   - Line length: 88
   - Python version: 3.8+
   - Ensures consistent code style

3. **Syntax Checking (flake8)**
   - Critical errors: E9, F63, F7, F82
   - Ensures code is free of basic syntax errors

4. **Security Scanning (bandit)**
   - Severity level: high
   - Exclusions: tests, docs
   - Scans for security vulnerabilities

5. **Merge Conflict Detection**
   - Prevents committing files with merge conflict markers

### Customizing Security Gates

#### Modifying the Pre-Commit Hook

Edit `.git/hooks/pre-commit` to adjust security checks:

```bash
# Example: Change bandit severity level
bandit -r . -x tests,docs --severity-level medium
```

#### Creating a Custom Configuration

For team-wide configuration, create a `.pre-commit-config.yaml` file:

```yaml
repos:
-   repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
    -   id: check-yaml
    -   id: end-of-file-fixer
    -   id: trailing-whitespace
    -   id: check-merge-conflict

-   repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
    -   id: black

-   repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
    -   id: isort
        args: ["--profile", "black"]

-   repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
    -   id: flake8
        args: ["--select=E9,F63,F7,F82"]

-   repo: https://github.com/PyCQA/bandit
    rev: 1.7.5
    hooks:
    -   id: bandit
        args: ["-r", ".", "-x", "tests,docs", "--severity-level", "high"]
```

## Continuous Integration Security Gates

### GitHub Actions Workflow

GhostKit's CI pipeline enforces security gates for all pull requests and commits to protected branches.

#### Default Configuration

```yaml
# .github/workflows/ci.yml
name: Security Checks

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
          pip install bandit safety
      - name: Run security scans
        run: |
          bandit -r . -x tests,docs --severity-level medium
          pip install safety==1.10.3
          safety check --file .safety-ignore || true
```

### Customizing CI Security Gates

#### Adjusting Severity Levels

Modify the `--severity-level` parameter in `.github/workflows/ci.yml`:

```yaml
bandit -r . -x tests,docs --severity-level low  # More strict
```

#### Adding Custom Security Checks

Extend the security job with additional steps:

```yaml
- name: Run custom security checks
  run: |
    python scripts/custom_security_check.py
```

## Security Gate Bypass

In exceptional circumstances, security gates can be bypassed:

### Temporary Bypass

```bash
# Skip pre-commit hooks (USE WITH CAUTION)
git commit --no-verify -m "[SECURITY] Critical emergency fix"
```

### Documented Exceptions

For known issues that cannot be immediately fixed:

1. Add to `.safety-ignore` for dependency vulnerabilities:
   ```
   # Format: vulnerability-id package-name
   51358 safety # Safety vulnerability in safety itself
   ```

2. Add `# nosec` comment for bandit false positives:
   ```python
   # Using MD5 for non-security purpose
   hash_value = hashlib.md5(data).hexdigest()  # nosec
   ```

## Advanced Security Gate Configuration

### Custom Rules

Create custom security rules in `scripts/security/custom_rules.py`:

```python
def check_custom_security_rule(file_content):
    # Example: Check for hardcoded credentials
    if "password" in file_content.lower() and "=" in file_content:
        return False
    return True
```

### Semgrep Rules

Use semgrep for advanced pattern matching:

1. Install semgrep:
   ```bash
   pip install semgrep
   ```

2. Create custom rules in `.semgrep/rules/`:
   ```yaml
   # .semgrep/rules/security.yaml
   rules:
     - id: hardcoded-credentials
       pattern: |
         $X = "..."
       message: "Potential hardcoded credential"
       languages: [python]
       severity: WARNING
   ```

3. Add to pre-commit hook:
   ```bash
   echo "Running semgrep security checks..."
   semgrep --config=.semgrep/rules/ .
   ```

## Reporting Security Gate Issues

If you believe a security gate is generating false positives or requires adjustment:

1. Open an issue with the label `security-gate`
2. Include detailed information:
   - Specific gate failing
   - Code snippet causing the issue
   - Proposed solution
   - Justification for changes

## Best Practices

1. **Never Disable Gates**: Modify configurations rather than disabling gates
2. **Document Exceptions**: Always document and justify security gate exceptions
3. **Regular Updates**: Keep security tools updated to latest versions
4. **Monitor Bypasses**: Track and review all security gate bypasses
5. **Test Changes**: Validate security gate changes before deployment
