# Contributing to AutoOps

Thank you for your interest in contributing to AutoOps! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Reporting Issues

- Use the GitHub issue tracker to report bugs
- Include as much detail as possible (OS, Python version, error messages, etc.)
- Check existing issues before creating new ones
- Use appropriate labels and templates

### Suggesting Enhancements

- Use the GitHub issue tracker for feature requests
- Provide a clear description of the proposed enhancement
- Explain why this enhancement would be useful
- Consider the impact on existing functionality

### Code Contributions

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run the test suite
6. Submit a pull request

## 🛠️ Development Setup

### Prerequisites

- Python 3.11+
- Git
- Docker (optional)
- Kubernetes cluster (optional)

### Local Setup

```bash
# Clone your fork
git clone <your-fork-url>
cd autoops

# Setup development environment
make setup

# Install development dependencies
pip install -e ".[dev,test]"

# Run tests to verify setup
make test
```

### Development Workflow

```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make changes
# ... edit files ...

# Run linting
make lint

# Format code
make format

# Run tests
make test

# Commit changes
git add .
git commit -m "Add your feature"

# Push to fork
git push origin feature/your-feature-name

# Create pull request
```

## 📝 Code Style

### Python Code Style

- Follow PEP 8
- Use Black for code formatting
- Use isort for import sorting
- Use type hints where appropriate
- Write docstrings for all public functions

### Configuration

The project uses several tools for code quality:

- **Black**: Code formatting
- **isort**: Import sorting
- **Ruff**: Linting
- **MyPy**: Type checking
- **pytest**: Testing

### Running Code Quality Checks

```bash
# Run all checks
make check

# Run individual checks
make lint      # Linting
make format    # Formatting
make test      # Testing
```

## 🧪 Testing

### Test Structure

```
tests/
├── conftest.py              # Shared fixtures
├── integration/             # Integration tests
│   └── test_full_pipeline.py
└── unit/                    # Unit tests (if any)

services/model_service/tests/
├── test_api.py              # API tests
└── test_model.py            # Model tests
```

### Writing Tests

- Write tests for new functionality
- Use descriptive test names
- Follow the AAA pattern (Arrange, Act, Assert)
- Use fixtures for common setup
- Mock external dependencies

### Running Tests

```bash
# Run all tests
make test

# Run specific test types
make test-unit
make test-integration

# Run with coverage
make test-coverage

# Run specific test file
pytest tests/integration/test_full_pipeline.py -v
```

### Test Categories

- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test component interactions
- **End-to-End Tests**: Test complete workflows

## 📚 Documentation

### Code Documentation

- Write docstrings for all public functions and classes
- Use Google-style docstrings
- Include type hints
- Provide examples for complex functions

### API Documentation

- Update API documentation for new endpoints
- Include request/response examples
- Document error conditions

### README Updates

- Update README.md for significant changes
- Include new features in the features list
- Update installation/usage instructions

## 🚀 Pull Request Process

### Before Submitting

1. **Run Tests**: Ensure all tests pass
2. **Code Quality**: Run linting and formatting
3. **Documentation**: Update relevant documentation
4. **Commit Messages**: Use clear, descriptive commit messages

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added/updated
```

### Review Process

1. **Automated Checks**: CI/CD pipeline runs tests and checks
2. **Code Review**: Maintainers review the code
3. **Feedback**: Address any feedback from reviewers
4. **Merge**: Once approved, the PR is merged

## 🏗️ Architecture Guidelines

### Service Design

- Keep services focused and single-purpose
- Use dependency injection for testability
- Implement proper error handling
- Follow RESTful API design principles

### Data Models

- Use Pydantic for data validation
- Implement proper serialization/deserialization
- Include data validation and error handling

### Configuration

- Use environment variables for configuration
- Provide sensible defaults
- Document configuration options
- Use configuration files for complex setups

## 🔒 Security Considerations

### Code Security

- Never commit secrets or credentials
- Use environment variables for sensitive data
- Validate all inputs
- Implement proper authentication/authorization

### Dependencies

- Keep dependencies up to date
- Use dependency scanning tools
- Pin dependency versions
- Review new dependencies before adding

## 📋 Release Process

### Versioning

- Follow Semantic Versioning (SemVer)
- Update version numbers in relevant files
- Create release notes
- Tag releases appropriately

### Release Checklist

- [ ] All tests pass
- [ ] Documentation updated
- [ ] Version numbers updated
- [ ] Release notes prepared
- [ ] Security review completed

## 🤔 Getting Help

### Resources

- **Documentation**: Check the README and inline docs
- **Issues**: Search existing GitHub issues
- **Discussions**: Use GitHub Discussions for questions
- **Code Review**: Ask for help in pull requests

### Communication

- Be respectful and constructive
- Provide context for questions
- Use appropriate channels for different types of questions
- Follow the code of conduct

## 📄 License

By contributing to AutoOps, you agree that your contributions will be licensed under the MIT License.

## 🙏 Recognition

Contributors will be recognized in:

- CONTRIBUTORS.md file
- Release notes
- Project documentation
- GitHub contributors page

---

Thank you for contributing to AutoOps! 🚀
