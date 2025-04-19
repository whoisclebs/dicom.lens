# Contributing to DicomLens

Thank you for your interest in contributing to **DicomLens**! We welcome contributions of all kinds—code fixes, documentation, tests, or even just feedback. By participating, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).

## Table of Contents
1. [Ways to Contribute](#ways-to-contribute)
2. [Getting Started](#getting-started)
3. [Development Workflow](#development-workflow)
4. [Branching Strategy](#branching-strategy)
5. [Coding Standards](#coding-standards)
6. [Testing](#testing)
7. [Documentation](#documentation)
8. [Reporting Issues](#reporting-issues)
9. [Code of Conduct](#code-of-conduct)

---

## Ways to Contribute

- **Bug Reports & Feature Requests**: Use GitHub Issues to report bugs or suggest enhancements.
- **Code Contributions**: Fix bugs or implement new features via pull requests.
- **Documentation**: Improve or expand the README, API docs, or tutorials.
- **Testing**: Add or improve unit and integration tests.
- **Feedback**: Share your ideas on the project’s design, UX, or roadmap.


## Getting Started

1. **Fork the Repository**
   ```bash
   git clone https://github.com/yourusername/dicomlens.git
   cd dicomlens
   ```

2. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Install Dependencies**
   - Python:
     ```bash
     cd ml
     python -m venv venv
     source venv/bin/activate
     pip install -r scripts/requirements.txt
     ```
   - Node.js:
     ```bash
     cd web/api
     npm install
     ```
   - Frontend:
     ```bash
     cd ../front
     npm install
     ```

4. **Run Tests Locally**
   ```bash
   # from repository root
   npm test               # API & frontend tests
   pytest --maxfail=1     # Python tests (if any)
   ```


## Development Workflow

1. **Make your changes** in the relevant directory (`ml/scripts`, `web/api`, or `web/front`).
2. **Ensure tests pass** and add new tests where appropriate.
3. **Update documentation** if your change affects usage or APIs.
4. **Commit with descriptive message**:
   ```bash
   git add .
   git commit -m "feat(api): add new endpoint for X"
   ```
5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```
6. **Open a Pull Request** against the `main` branch of the upstream repository.


## Branching Strategy

- `main`: Always deployable; holds the stable release.
- `develop`: Integration branch for features; continuously tested.
- `feature/*`: New features or experiments.
- `fix/*`: Bug fixes.
- `release/*`: Prepares a new production release.
- `hotfix/*`: Urgent fixes to production.


## Coding Standards

- **Python**: Follow PEP 8. Use `black` for formatting and `flake8` for linting.
- **JavaScript/TypeScript**: Follow ESLint rules (`eslint:recommended`). Use Prettier for formatting.
- **Commit Messages**: Use [Conventional Commits](https://www.conventionalcommits.org):
  - `feat:` A new feature
  - `fix:` A bug fix
  - `docs:` Documentation only changes
  - `style:` Formatting, missing semicolons, etc
  - `refactor:` Code change that neither fixes a bug nor adds a feature
  - `test:` Adding missing tests or correcting existing tests


## Testing

- **API & Frontend**: `npm test` (Jest, Supertest, React Testing Library)
- **Python**: `pytest` in `ml/` folder
- Aim for >80% coverage. CI will block merging on failures.


## Documentation

- Update **README.md**, **docs/**, or inline Javadoc/Docstrings when necessary.
- Run `npm run docs:build` or your docs generator to verify builds.


## Reporting Issues

- Use GitHub Issues.
- Provide **detailed description**, **steps to reproduce**, **expected vs actual behavior**, and **environment** details.


## Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md). We adopt an open and welcoming attitude toward contributions from all.

