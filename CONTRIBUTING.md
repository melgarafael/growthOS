# Contributing to GrowthOS

Thank you for your interest in contributing to GrowthOS! This guide will help you get set up and understand our development workflow.

## Development Setup

### Prerequisites

- Python 3.11+
- Docker and Docker Compose (for integration testing)
- Claude Code CLI (for plugin testing)

### Local Setup

```bash
# Clone the repository
git clone https://github.com/your-org/growthOS.git
cd growthOS

# Install shared library in development mode
pip install -e "shared-lib/[dev]"

# Install MCP server dependencies
pip install -r mcp-servers/mcp-social-publish/requirements.txt
pip install -r mcp-servers/mcp-social-discover/requirements.txt
pip install -r mcp-servers/mcp-obsidian-vault/requirements.txt

# Copy config templates
cp .env.example .env
cp brand-voice.example.yaml brand-voice.yaml

# Run tests
pytest shared-lib/tests/
```

## Coding Standards

### Python

- **Formatter/Linter:** [ruff](https://docs.astral.sh/ruff/) — run `ruff check .` and `ruff format .`
- **Type hints:** Use type annotations for all function signatures
- **Docstrings:** Required for public functions and classes
- **Tests:** Required for all new functionality

### File Organization

- MCP server logic goes in `mcp-servers/<server-name>/`
- Shared utilities go in `shared-lib/growthOS_shared/`
- Agent definitions go in `agents/<agent-name>/`
- Skill definitions go in `skills/<skill-name>/`

### Naming Conventions

- Files: `snake_case.py`
- Classes: `PascalCase`
- Functions/variables: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- Environment variables: `GROWTHOS_` prefix

## Pull Request Process

1. **Fork** the repository and create a feature branch from `main`
2. **Implement** your changes following the coding standards above
3. **Test** your changes:
   ```bash
   # Lint
   ruff check .

   # Unit tests
   pytest shared-lib/tests/ -v

   # Docker build (if modifying Dockerfile or MCP servers)
   docker-compose build
   ```
4. **Document** any new features, environment variables, or configuration
5. **Submit** a PR with a clear description of changes and motivation

### PR Checklist

- [ ] All tests pass (`pytest`)
- [ ] Linting passes (`ruff check .`)
- [ ] No secrets or API keys in code
- [ ] New environment variables added to `.env.example`
- [ ] README updated if adding features or changing usage

## Testing Requirements

### Unit Tests

- Located in `shared-lib/tests/` and `mcp-servers/<server>/tests/`
- Use `pytest` with `pytest-asyncio` for async code
- Aim for coverage of core logic and edge cases

### Running Tests

```bash
# All shared-lib tests
pytest shared-lib/tests/ -v

# Specific MCP server tests
pytest mcp-servers/mcp-social-publish/tests/ -v

# With coverage
pytest --cov=shared-lib/growthOS_shared shared-lib/tests/
```

## Plugin Development

### Adding a New Skill

1. Create directory: `skills/<skill-name>/`
2. Add `SKILL.md` with frontmatter (name, description, trigger patterns)
3. Register in `plugin.json` under `skills`

### Adding a New Agent

1. Create directory: `agents/<agent-name>/`
2. Add `AGENT.md` with frontmatter (name, description, tools, model)
3. Register in `plugin.json` under `agents`

### Adding a New Hook

1. Create directory: `hooks/<hook-name>/`
2. Add hook definition file with event triggers
3. Register in `plugin.json` under `hooks`

## Reporting Issues

- Use GitHub Issues for bugs and feature requests
- Include reproduction steps, expected vs actual behavior
- For security issues, see [SECURITY.md](SECURITY.md)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
