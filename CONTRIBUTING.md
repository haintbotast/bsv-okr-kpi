# Contributing to KPI Management System

Thank you for your interest in contributing to the KPI Management System! This document provides guidelines and instructions for contributing to this project.

---

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Workflow](#development-workflow)
4. [Coding Standards](#coding-standards)
5. [Testing Requirements](#testing-requirements)
6. [Commit Guidelines](#commit-guidelines)
7. [Pull Request Process](#pull-request-process)
8. [Documentation](#documentation)
9. [Reporting Issues](#reporting-issues)

---

## Code of Conduct

This project follows a standard code of conduct:

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Respect differing viewpoints
- Prioritize the community's best interests

---

## Getting Started

### Prerequisites

Before you begin, ensure you have:

- **Git** installed
- **Docker** and **Docker Compose** installed
- **Python 3.11+** (for backend development)
- **Node.js 18+** and **npm** (for frontend development)
- A code editor (VS Code, PyCharm, etc.)

### Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/your-org/kpi-system.git
cd kpi-system

# Create environment file
cp .env.example .env
# Edit .env with your local settings

# Start development environment
docker-compose up -d

# Or run locally:

# Backend
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

---

## Development Workflow

### 1. Create a Branch

Always create a new branch for your changes:

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

Branch naming conventions:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Adding tests
- `chore/` - Maintenance tasks

### 2. Make Changes

- Write clean, readable code
- Follow the coding standards (see below)
- Add tests for new features
- Update documentation as needed

### 3. Test Your Changes

```bash
# Backend tests
cd backend
pytest

# Frontend tests (if configured)
cd frontend
npm test

# Full integration test
docker-compose up -d
# Test manually in browser
```

### 4. Commit Your Changes

Follow the commit guidelines (see below).

### 5. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub/GitLab.

---

## Coding Standards

### Python (Backend)

**Style Guide**: Follow PEP 8

```python
# Good
def calculate_progress(current: float, target: float) -> float:
    """Calculate progress percentage.

    Args:
        current: Current value
        target: Target value

    Returns:
        Progress as percentage (0-100)
    """
    if target == 0:
        return 0
    return (current / target) * 100

# Bad
def calc(c,t):
    return c/t*100 if t!=0 else 0
```

**Key Points**:
- Use type hints
- Write docstrings for functions/classes
- Max line length: 100 characters
- Use descriptive variable names
- Follow FastAPI best practices

**Tools**:
```bash
# Format code
black app/

# Check style
flake8 app/

# Sort imports
isort app/
```

### JavaScript/React (Frontend)

**Style Guide**: Airbnb JavaScript Style Guide

```javascript
// Good
const calculateProgress = (current, target) => {
  if (target === 0) return 0;
  return (current / target) * 100;
};

// Bad
function calc(c,t){return t!=0?c/t*100:0}
```

**Key Points**:
- Use functional components with hooks
- Use ESLint and Prettier
- Use meaningful component names
- Keep components small and focused
- Add PropTypes or TypeScript types

**Tools**:
```bash
# Format code
npm run format

# Lint code
npm run lint

# Fix lint issues
npm run lint:fix
```

### General Guidelines

- **DRY** (Don't Repeat Yourself)
- **KISS** (Keep It Simple, Stupid)
- **YAGNI** (You Aren't Gonna Need It)
- Write self-documenting code
- Comment complex logic
- Avoid premature optimization

---

## Testing Requirements

### Backend Tests

All backend changes should include tests:

```python
# tests/test_kpi.py
def test_create_kpi(client, test_user):
    """Test KPI creation."""
    response = client.post(
        "/api/v1/kpis",
        json={
            "title": "Test KPI",
            "year": 2024,
            "quarter": "Q1"
        },
        headers={"Authorization": f"Bearer {test_user.token}"}
    )
    assert response.status_code == 201
    assert response.json()["title"] == "Test KPI"
```

**Coverage Target**: Aim for >70% code coverage

```bash
pytest --cov=app tests/
```

### Frontend Tests (Optional)

If implementing frontend tests:

```javascript
// KPICard.test.jsx
test('renders KPI card with title', () => {
  render(<KPICard title="Test KPI" />);
  expect(screen.getByText('Test KPI')).toBeInTheDocument();
});
```

### Manual Testing Checklist

Before submitting, manually test:
- [ ] Feature works as expected
- [ ] No console errors
- [ ] Responsive on mobile
- [ ] Works in Chrome, Firefox, Safari
- [ ] Proper error handling
- [ ] Loading states work

---

## Commit Guidelines

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

**Examples**:

```bash
feat(kpi): add quarterly progress tracking

Implement progress calculation by quarter with automatic
updates when evidence is uploaded.

Closes #123
```

```bash
fix(auth): resolve token refresh race condition

Fixed issue where multiple simultaneous refresh requests
would fail. Added mutex lock to prevent concurrent refreshes.

Fixes #456
```

**Rules**:
- Use present tense ("add" not "added")
- First line max 72 characters
- Reference issue numbers
- Explain "why" in body, not "what"

---

## Pull Request Process

### Before Creating PR

1. ✅ Update from main branch
   ```bash
   git checkout main
   git pull origin main
   git checkout feature/your-feature
   git merge main
   ```

2. ✅ Run all tests
3. ✅ Update documentation
4. ✅ Self-review your code
5. ✅ Check for merge conflicts

### PR Template

When creating a PR, include:

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Related Issues
Closes #123

## Testing
- [ ] Unit tests added/updated
- [ ] Manual testing completed
- [ ] All tests passing

## Screenshots (if applicable)
[Add screenshots here]

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added to complex code
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tests pass locally
```

### Review Process

1. Create PR with detailed description
2. Assign reviewers (if applicable)
3. Address review comments
4. Update PR based on feedback
5. Wait for approval
6. Squash and merge (or rebase)

### After Merge

- Delete your feature branch
- Update local main branch
- Close related issues

---

## Documentation

### Code Documentation

**Python**:
```python
def calculate_kpi_progress(kpi: KPI) -> float:
    """Calculate KPI progress percentage.

    This function calculates the progress based on current_value
    and target_value fields of the KPI model.

    Args:
        kpi: KPI model instance

    Returns:
        float: Progress percentage (0-100)

    Raises:
        ValueError: If target_value is invalid

    Example:
        >>> kpi = KPI(current_value=90, target_value=100)
        >>> calculate_kpi_progress(kpi)
        90.0
    """
    # Implementation
```

**JavaScript**:
```javascript
/**
 * Calculate KPI progress percentage
 * @param {number} current - Current value
 * @param {number} target - Target value
 * @returns {number} Progress percentage (0-100)
 */
const calculateProgress = (current, target) => {
  // Implementation
};
```

### Updating Documentation

When making changes, update:
- API documentation (if API changes)
- README.md (if user-facing changes)
- Code comments
- Inline documentation

---

## Reporting Issues

### Bug Reports

Use this template:

```markdown
**Bug Description**
Clear description of the bug

**To Reproduce**
Steps to reproduce:
1. Go to '...'
2. Click on '...'
3. See error

**Expected Behavior**
What you expected to happen

**Screenshots**
Add screenshots if applicable

**Environment**
- OS: [e.g., Ubuntu 22.04]
- Browser: [e.g., Chrome 120]
- Version: [e.g., 1.0.0]

**Additional Context**
Any other relevant information
```

### Feature Requests

```markdown
**Feature Description**
Clear description of the feature

**Problem It Solves**
What problem does this address?

**Proposed Solution**
How would you implement this?

**Alternatives Considered**
Other approaches you've considered

**Additional Context**
Mockups, examples, etc.
```

---

## Project Structure

Familiarize yourself with the structure:

```
kpi-system/
├── backend/          # FastAPI backend
│   ├── app/
│   │   ├── api/      # API routes
│   │   ├── models/   # SQLAlchemy models
│   │   ├── schemas/  # Pydantic schemas
│   │   ├── crud/     # CRUD operations
│   │   └── services/ # Business logic
│   └── tests/        # Backend tests
├── frontend/         # React frontend
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── contexts/
│   └── public/
├── docs/             # Documentation
├── data/             # Persistent data (not in Git)
└── docker-compose.yml
```

---

## Development Best Practices

### Security
- Never commit `.env` files
- Don't hardcode secrets
- Validate all user inputs
- Use parameterized queries
- Follow OWASP guidelines

### Performance
- Avoid N+1 queries
- Use pagination for lists
- Optimize images
- Lazy load components
- Cache when appropriate

### Accessibility
- Use semantic HTML
- Add ARIA labels
- Support keyboard navigation
- Test with screen readers
- Maintain color contrast

---

## Questions?

- Check [documentation](./docs/)
- Ask in project discussions
- Contact maintainers: support@company.com

---

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

---

**Thank you for contributing!** 🎉

Your contributions make this project better for everyone.
