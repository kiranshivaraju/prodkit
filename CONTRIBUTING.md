# Contributing to ProdKit

Thank you for your interest in contributing to ProdKit!

## How to Contribute

### Reporting Issues

If you find a bug or have a feature request:

1. Check if the issue already exists in the [Issues](https://github.com/kiranshivaraju/prodkit/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - Your environment (OS, Claude Code version, etc.)

### Suggesting Enhancements

We welcome suggestions for new commands, improvements to existing workflows, or additional features:

1. Open an issue with the `enhancement` label
2. Describe the enhancement and why it would be useful
3. Provide examples of how it would work

### Code Contributions

1. **Fork the repository**
   ```bash
   git clone https://github.com/kiranshivaraju/prodkit.git
   cd prodkit
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the existing code style
   - Update documentation if needed
   - Test your changes thoroughly

4. **Commit your changes**
   ```bash
   git commit -m "feat: add your feature description"
   ```

   Use conventional commit messages:
   - `feat:` - New feature
   - `fix:` - Bug fix
   - `docs:` - Documentation changes
   - `refactor:` - Code refactoring
   - `test:` - Adding tests

5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Open a Pull Request**
   - Describe what your changes do
   - Reference any related issues
   - Explain why the changes are needed

## Development Guidelines

### Command Files

When creating or modifying command files (`.prodkit/commands/*.md`):

- Use clear, descriptive frontmatter:
  ```yaml
  ---
  description: Brief description of what this command does
  ---
  ```

- Include comprehensive instructions
- Add examples where helpful
- Document all parameters and options
- Consider edge cases and error handling

### Testing

Before submitting:

1. Test the install script on a fresh directory
2. Verify all commands work in Claude Code
3. Test with different project types (Python, Node.js, etc.)
4. Ensure documentation is up to date

### Documentation

- Update README.md if you add new features
- Add examples for new commands
- Keep documentation clear and concise
- Include troubleshooting tips if applicable

## Questions?

If you have questions about contributing, feel free to:

- Open a discussion in the [Discussions](https://github.com/kiranshivaraju/prodkit/discussions) tab
- Ask in an issue
- Reach out to the maintainers

Thank you for helping make ProdKit better! 🚀
