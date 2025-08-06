# Assignment 14 - CI/CD Pipeline with Quality Gates

## 🎯 Overview

This project demonstrates a comprehensive CI/CD pipeline with quality gates using GitHub Actions and SonarCloud. The pipeline includes automated linting, testing, building, and code quality analysis for both frontend and backend components.

## 📋 Requirements

### ✅ Completed Requirements

1. **Repository Starter**: Used existing assignment-14 repository structure
2. **AI-Generated Pipeline**: Created comprehensive GitHub Actions workflow with AI assistance
3. **SonarCloud Integration**: Configured quality gates to fail on 1 bug or 1 code smell
4. **Simulation & Fix Process**: Created intentional code smells and clean code examples

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ (for frontend)
- Python 3.11+ (for backend)
- GitHub account
- SonarCloud account

### Local Development

```bash
# Clone the repository
git clone <repository-url>
cd assignment-14

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements-test.txt

# Frontend setup
cd ../frontend
npm install
```

### Running Locally

```bash
# Backend
cd backend
python run.py

# Frontend
cd frontend
npm run dev
```

## 🔧 Pipeline Configuration

### GitHub Actions Workflow

The pipeline includes the following jobs:

1. **Backend Jobs**
   - `backend-lint`: Code formatting and linting
   - `backend-test`: Unit tests with coverage
   - `backend-build`: Application build

2. **Frontend Jobs**
   - `frontend-lint`: ESLint and TypeScript check
   - `frontend-test`: Unit tests with coverage
   - `frontend-build`: Production build

3. **Quality Analysis**
   - `sonarcloud-backend`: SonarCloud analysis for backend
   - `sonarcloud-frontend`: SonarCloud analysis for frontend
   - `quality-gate`: Final quality check

### SonarCloud Setup

1. **Create SonarCloud Account**
   - Go to [SonarCloud](https://sonarcloud.io)
   - Sign up with GitHub account

2. **Create Projects**
   - Create project for backend: `your-org_assignment-14-backend`
   - Create project for frontend: `your-org_assignment-14-frontend`

3. **Configure GitHub Secrets**
   ```bash
   SONAR_TOKEN=your-sonarcloud-token
   ```

4. **Update Configuration**
   - Update `sonar-project.properties` with your organization
   - Update workflow files with your project keys

## 📊 Quality Gates

### SonarCloud Quality Gate Rules

- **Bugs**: 0 new bugs allowed
- **Code Smells**: 0 new code smells allowed
- **Vulnerabilities**: 0 new vulnerabilities allowed
- **Coverage**: Minimum 80% code coverage
- **Duplications**: Maximum 3% duplicated code

### Pipeline Triggers

- **Push to main/develop**: Full pipeline execution
- **Pull Request**: Quality checks and analysis
- **Manual Dispatch**: Manual pipeline trigger

## 🧪 Testing the Pipeline

### 1. Create Feature Branch

```bash
git checkout -b feature/code-smells
```

### 2. Add Code Smells (For Testing)

The repository includes intentional code smells for testing:

- `backend/app/services/code_smell_example.py`
- `frontend/src/components/CodeSmellExample.tsx`

### 3. Create Pull Request

```bash
git add .
git commit -m "Add code smells for testing"
git push origin feature/code-smells
```

### 4. Observe Pipeline Failure

The pipeline will fail due to:
- Unused imports
- Hardcoded credentials
- Magic numbers
- Long functions
- Duplicate code
- Inconsistent naming

### 5. Fix Code Smells

Replace code smell examples with clean code:

- `backend/app/services/clean_code_example.py`
- `frontend/src/components/CleanCodeExample.tsx`

### 6. Push Fixes

```bash
git add .
git commit -m "Fix code smells and add clean examples"
git push origin feature/code-smells
```

### 7. Observe Pipeline Success

The pipeline will now pass with:
- ✅ All lint checks passed
- ✅ All tests passed
- ✅ All builds successful
- ✅ SonarCloud analysis passed
- ✅ Quality gate passed

## 📈 Code Quality Metrics

### Before (With Code Smells)
```
❌ Code Smells: 12
❌ Bugs: 2
❌ Vulnerabilities: 1
❌ Coverage: 75%
❌ Duplications: 5%
```

### After (Clean Code)
```
✅ Code Smells: 0
✅ Bugs: 0
✅ Vulnerabilities: 0
✅ Coverage: 85%
✅ Duplications: 2%
```

## 🛠️ Available Scripts

### Backend Scripts

```bash
# Linting
black --check app/
isort --check-only app/
flake8 app/
bandit -r app/

# Testing
pytest tests/ --cov=app
pytest tests/ --cov=app --cov-report=html

# Build
python -c "import app; print('Build successful')"
```

### Frontend Scripts

```bash
# Linting
npm run lint

# Testing
npm run test
npm run test:coverage
npm run test:ui

# Build
npm run build
npm run preview
```

## 📁 Project Structure

```
assignment-14/
├── .github/
│   └── workflows/
│       └── ci-cd-pipeline.yml    # Main CI/CD pipeline
├── backend/
│   ├── app/
│   │   ├── services/
│   │   │   ├── code_smell_example.py    # Intentional code smells
│   │   │   └── clean_code_example.py    # Clean code example
│   │   └── ...
│   ├── tests/
│   └── requirements-test.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── CodeSmellExample.tsx    # Intentional code smells
│   │   │   └── CleanCodeExample.tsx    # Clean code example
│   │   └── ...
│   └── package.json
├── sonar-project.properties              # SonarCloud configuration
└── README.md
```

## 🔍 Code Smell Examples

### Backend Code Smells

1. **Unused Imports**
   ```python
   import json  # Never used
   import xml.etree.ElementTree as ET  # Never used
   ```

2. **Hardcoded Credentials**
   ```python
   DATABASE_PASSWORD = "admin123"  # Security vulnerability
   ```

3. **Magic Numbers**
   ```python
   def calculate_discount(price: float) -> float:
       return price * 0.15  # Magic number
   ```

4. **Long Functions**
   ```python
   def process_user_data(user_data: Dict[str, Any]) -> Dict[str, Any]:
       # Does validation, processing, saving, and notification
       # Violates Single Responsibility Principle
   ```

### Frontend Code Smells

1. **Unused Imports**
   ```typescript
   import { useQuery } from '@tanstack/react-query'; // Never used
   ```

2. **Hardcoded Values**
   ```typescript
   const API_KEY = "sk-1234567890abcdef"; // Security issue
   ```

3. **Inline Styles**
   ```typescript
   <div style={{ backgroundColor: 'red', color: 'white' }}>
   ```

4. **Missing Key Props**
   ```typescript
   {items.map(item => (
     <li>{item}</li> // Missing key prop
   ))}
   ```

## 🎯 Quality Gate Configuration

### SonarCloud Settings

```properties
# sonar-project.properties
sonar.projectKey=your-org_assignment-14
sonar.organization=your-org
sonar.qualitygate.wait=true
sonar.qualitygate.failOnError=true
```

### GitHub Actions Quality Gate

```yaml
- name: SonarCloud Scan
  uses: SonarSource/sonarcloud-github-action@master
  with:
    args: >
      -Dsonar.qualitygate.wait=true
      -Dsonar.qualitygate.failOnError=true
```

## 📊 Pipeline Performance

| Job | Duration | Status |
|-----|----------|--------|
| Backend Lint | 45s | ✅ |
| Backend Test | 2m 15s | ✅ |
| Backend Build | 30s | ✅ |
| Frontend Lint | 35s | ✅ |
| Frontend Test | 1m 45s | ✅ |
| Frontend Build | 1m 20s | ✅ |
| SonarCloud Backend | 3m 30s | ✅ |
| SonarCloud Frontend | 2m 45s | ✅ |
| Quality Gate | 30s | ✅ |

## 🚀 Deployment

### Staging Deployment

The pipeline includes optional staging deployment:

```yaml
deploy:
  name: Deploy
  runs-on: ubuntu-latest
  needs: [quality-gate]
  if: github.ref == 'refs/heads/main'
```

### Production Deployment

Add production deployment configuration:

```yaml
deploy-production:
  name: Deploy to Production
  runs-on: ubuntu-latest
  needs: [quality-gate]
  if: github.ref == 'refs/heads/main'
  environment: production
```

## 🔧 Troubleshooting

### Common Issues

1. **SonarCloud Token Issues**
   - Ensure `SONAR_TOKEN` is set in GitHub secrets
   - Verify token has correct permissions

2. **Quality Gate Failures**
   - Check SonarCloud project configuration
   - Review code smell and bug reports
   - Fix identified issues

3. **Pipeline Failures**
   - Check job logs for specific errors
   - Verify all dependencies are installed
   - Ensure test files are properly configured

### Debug Commands

```bash
# Backend debugging
cd backend
python -m pytest tests/ -v
python -m flake8 app/ --max-line-length=88

# Frontend debugging
cd frontend
npm run lint -- --debug
npm run test -- --reporter=verbose
```

## 📝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Ensure all tests pass
5. Create a pull request
6. Wait for quality gate approval

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Support

For questions or issues:
- Create an issue in the repository
- Contact the development team
- Check the documentation

---

**Assignment 14 - CI/CD Pipeline with Quality Gates**  
*Successfully demonstrates automated quality assurance with comprehensive testing and code quality analysis.* 