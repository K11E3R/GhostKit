# Contributing to GhostKit

First off, thanks for taking the time to contribute to GhostKit! Your expertise and help makes this framework more powerful and secure.

## Code of Conduct

This project adheres to a Code of Conduct that all contributors are expected to follow. Please read [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before contributing.

## How Can I Contribute?

### Reporting Bugs

- **Ensure the bug hasn't been reported already** by searching through [Issues](https://github.com/K11E3R/GhostKit/issues)
- If you can't find an issue addressing your problem, [open a new one](https://github.com/K11E3R/GhostKit/issues/new/choose) using the bug report template
- Include detailed steps to reproduce the bug and any relevant logs/screenshots

### Suggesting Enhancements

- **Check existing enhancement requests** in [Issues](https://github.com/K11E3R/GhostKit/issues) first
- Open a [feature request](https://github.com/K11E3R/GhostKit/issues/new/choose) using the feature request template
- Clearly describe the problem and solution with as much detail as possible

### Pull Requests

1. Fork the repository
2. Create a feature branch from `develop`
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Make your changes with clear, descriptive commits following our commit message guidelines
4. Add or update tests as needed
5. Update documentation to reflect changes
6. Submit your PR against the `develop` branch

## Development Process

### Environment Setup

```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/GhostKit.git
cd GhostKit

# Set up upstream remote
git remote add upstream https://github.com/K11E3R/GhostKit.git

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install git hooks
./scripts/setup-hooks.sh
```

### Coding Standards

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines
- Use [Black](https://github.com/psf/black) for code formatting
- Sort imports with [isort](https://pycqa.github.io/isort/)
- All code should pass the pre-commit hooks

### Git Commit Conventions

All commits must follow: `[TAG] module: description`

- **TAG**: one of `UPDATE` (modifications), `ADD` (new feature), `FIX` (bug fix), `RM` (remove), `MV` (move/refactor), `DOC` (documentation)
- **module**: the specific component or script modified
- **description**: concise summary of the change

Examples:
```
[UPDATE] readme: update installation instructions
[ADD] network: implement parallel nmap scanner
[FIX] exploit: correct off-by-one in PoC buffer overflow
[RM] old_tool: remove deprecated recon script
[MV] utils: refactor helper functions into modules
[DOC] README: add usage examples
```

### Testing

- Write tests for all new features and bug fixes
- Run the test suite before submitting your PR:
  ```bash
  python -m pytest
  ```
- Aim for high test coverage on critical security modules

### Documentation

- Update documentation to reflect your changes
- Follow the existing documentation style
- Add examples for new features
- Update command line help texts

## Security Considerations

- **Never** include credentials, API keys, or sensitive data in your code
- **Always** validate all user inputs
- Properly handle sensitive output and error messages
- Consider potential security implications of your changes

## Release Process

- New releases are cut from the `master` branch after thorough testing
- Releases follow [Semantic Versioning](https://semver.org/)
- See [RELEASING.md](docs/development/RELEASING.md) for more details

Thank you for contributing to make GhostKit better!
