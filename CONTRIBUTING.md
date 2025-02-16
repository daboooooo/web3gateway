# Contributing Guidelines

Thank you for your interest in the Web3 Restful Gateway project! We welcome all forms of contributions, including but not limited to feature improvements, bug fixes, and documentation enhancements.

## Development Environment Setup

1. Fork and clone the repository
```bash
git clone https://github.com/<your-username>/web3gateway.git
cd web3gateway
```

2. Create a virtual environment
```bash
python -m venv .env
source .env/bin/activate  # Linux/MacOS
# or
.env\Scripts\activate  # Windows
```

3. Install development dependencies
```bash
pip install -r requirements-dev.txt
```

4. Install pre-commit hooks
```bash
pre-commit install
```

## Development Workflow

1. Create a new branch
```bash
git checkout -b feature/your-feature-name
```

2. Commit your code
```bash
git add .
git commit -m "feat: your meaningful commit message"
```

Please follow the [Conventional Commits](https://www.conventionalcommits.org/) specification for commit messages:
- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation updates
- `test:` Test-related changes
- `refactor:` Code refactoring
- `style:` Code formatting changes
- `perf:` Performance improvements

3. Run tests
```bash
pytest
```

4. Submit Pull Request
- Ensure CI checks pass
- Describe changes in detail
- Link related issues

## Code Standards

- Follow PEP 8 coding standards
- Use type hints for type annotations
- Keep code simple and clear
- Write unit tests
- Comment necessary code logic

## API Documentation

If your changes involve API modifications, please update:
- API documentation
- OpenAPI schema
- Example code

## Version Guidelines

The project follows [Semantic Versioning](https://semver.org/):
- MAJOR.MINOR.PATCH
- Major version: Incompatible API changes
- Minor version: Backward-compatible feature additions
- Patch version: Backward-compatible bug fixes

## Code of Conduct

Please follow our code of conduct:
- Respect all contributors
- Maintain professional and friendly communication
- Focus on constructive discussions
- Avoid personal attacks or offensive language

## License

By contributing code, you agree to license your contribution under the MIT License.

## Contact

If you have any questions, please reach out through:
- GitHub Issues
- Email: horsen666@gmail.com

Thank you again for your contribution!
