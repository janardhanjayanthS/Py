# CI/CD Documentation

## What is CI/CD?

**CI/CD** stands for **Continuous Integration** and **Continuous Deployment/Delivery**. It's a modern software development practice that automates the process of testing and deploying code changes.

### Continuous Integration (CI)
- **What it does**: Automatically tests your code every time you push changes to the repository
- **Why it matters**: Catches bugs early before they reach production
- **How it works**: When you push code, automated tests run to verify everything still works

### Continuous Deployment/Delivery (CD)
- **What it does**: Automatically deploys your code to production (or staging) after tests pass
- **Why it matters**: Faster releases, less manual work, fewer human errors
- **How it works**: If all tests pass, the code is automatically deployed to servers

---

## Benefits of CI/CD

1. **Early Bug Detection**: Problems are found immediately when code is pushed
2. **Faster Development**: No waiting for manual testing and deployment
3. **Better Code Quality**: Automated checks ensure standards are maintained
4. **Reduced Risk**: Small, frequent updates are safer than large releases
5. **Team Collaboration**: Everyone knows if their changes break something

---

## CI/CD in This Project

This project uses **GitHub Actions** for CI/CD automation. Every time code is pushed to the `feat/inv_manager_SDLC_step5` branch, the following happens automatically:

1. ✅ Code is checked out from the repository
2. ✅ Python environment is set up
3. ✅ Dependencies are installed
4. ✅ Code is linted (checked for syntax errors)
5. ✅ Tests are run to verify functionality

---

## Understanding the Workflow File

The CI/CD pipeline is defined in `.github/workflows/sdlc_s5_cicd.yaml`. Let's break it down step by step.

### File Structure Overview

```yaml
name: SCLC STEP 5 CI-CD

on:
  push:
    branches: ['feat/inv_manager_SDLC_step5']

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      # ... steps go here
```

---

## Detailed Explanation of Each Section

### 1. Workflow Name

```yaml
name: SCLC STEP 5 CI-CD
```

**What it does**: Gives a human-readable name to this workflow  
**Why it matters**: Helps identify this workflow in the GitHub Actions UI  
**Example**: When you view GitHub Actions, you'll see "SCLC STEP 5 CI-CD" in the list

---

### 2. Trigger Configuration

```yaml
on:
  push:
    branches: ['feat/inv_manager_SDLC_step5']
```

**What it does**: Defines when this workflow should run  
**Breakdown**:
- `on:` - Specifies the event that triggers the workflow
- `push:` - Runs when code is pushed to the repository
- `branches:` - Only runs for specific branches
- `['feat/inv_manager_SDLC_step5']` - Only triggers on this branch

**Example**: If you push to `main` branch, this workflow won't run. But pushing to `feat/inv_manager_SDLC_step5` will trigger it.

---

### 3. Jobs Configuration

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
```

**What it does**: Defines the jobs to execute  
**Breakdown**:
- `jobs:` - Container for all jobs in this workflow
- `build:` - Name of this specific job (you can have multiple jobs)
- `runs-on: ubuntu-latest` - Specifies the operating system to use

**Why Ubuntu?**: It's free, fast, and has all the tools needed for Python projects

---

### 4. Step 1: Checkout Code

```yaml
- name: Checkout Code
  uses: actions/checkout@v5
```

**What it does**: Downloads your repository code to the runner (GitHub's server)  
**Breakdown**:
- `name:` - Human-readable description of this step
- `uses:` - Uses a pre-built action from GitHub Marketplace
- `actions/checkout@v5` - Official GitHub action for checking out code

**Why needed?**: The runner starts with an empty filesystem. This step copies your code so tests can run.

---

### 5. Step 2: Set Up Python

```yaml
- name: Set-up python 3.12
  uses: actions/setup-python@v5
  with:
    python-version: "3.12"
```

**What it does**: Installs Python 3.12 on the runner  
**Breakdown**:
- `uses: actions/setup-python@v5` - Official action for installing Python
- `with:` - Parameters to pass to the action
- `python-version: "3.12"` - Specific Python version to install

**Why 3.12?**: This project is developed with Python 3.12, so tests must run on the same version.

---

### 6. Step 3: Install Dependencies

```yaml
- name: Install package and requirements
  run: |
    pip install flake8
    pip install -e "Week 4 & 5/SDLC/project/package/"
    pip install --no-cache-dir -r "Week 4 & 5/SDLC/project/requirements/requirements.txt"
```

**What it does**: Installs all necessary Python packages  
**Breakdown**:
- `run: |` - Executes shell commands (the `|` allows multiple lines)
- `pip install flake8` - Installs the linting tool
- `pip install -e "Week 4 & 5/SDLC/project/package/"` - Installs the project package in editable mode
- `pip install --no-cache-dir -r "..."` - Installs all dependencies from requirements.txt

**Why `-e` flag?**: Editable mode means changes to code are immediately reflected without reinstalling  
**Why `--no-cache-dir`?**: Saves disk space on the runner by not caching downloaded packages

---

### 7. Step 4: Lint with Flake8

```yaml
- name: Lint with flake8
  run: |
    flake8 "Week 4 & 5/SDLC/project/src/" --count --select=E9,F63,F7,F82 --show-source --statistics
```

**What it does**: Checks code for syntax errors and critical issues  
**Breakdown**:
- `flake8 "Week 4 & 5/SDLC/project/src/"` - Run flake8 on the src directory
- `--count` - Show the total number of errors
- `--select=E9,F63,F7,F82` - Only check for critical errors:
  - `E9`: Runtime errors (syntax errors)
  - `F63`: Invalid print statement
  - `F7`: Syntax errors in type comments
  - `F82`: Undefined names
- `--show-source` - Display the source code that caused the error
- `--statistics` - Show error statistics at the end

**Why lint?**: Catches syntax errors before running tests, saving time

---

### 8. Step 5: Run Tests

```yaml
- name: Run Tests
  run: |
    pytest -p no:cacheprovider "Week 4 & 5/SDLC/project/tests/core"
    pytest -p no:cacheprovider "Week 4 & 5/SDLC/project/tests/repository"
    pytest -p no:cacheprovider "Week 4 & 5/SDLC/project/tests/services"
```

**What it does**: Runs all test suites to verify code functionality  
**Breakdown**:
- `pytest` - Python testing framework
- `-p no:cacheprovider` - Disables pytest cache (saves disk space on runner)
- Three separate test directories are run:
  1. `tests/core` - Tests for core functionality (config, JWT, exceptions)
  2. `tests/repository` - Tests for database operations
  3. `tests/services` - Tests for business logic

**Why separate commands?**: Each directory is tested independently, making it easier to identify which area has failures

---

## How the Workflow Executes

### Step-by-Step Execution Flow

1. **Developer pushes code** to `feat/inv_manager_SDLC_step5` branch
2. **GitHub detects the push** and triggers the workflow
3. **Runner is provisioned** (Ubuntu server is created)
4. **Code is checked out** from the repository
5. **Python 3.12 is installed** on the runner
6. **Dependencies are installed** (flake8, project package, requirements)
7. **Code is linted** - if errors found, workflow fails ❌
8. **Tests are run** - if any test fails, workflow fails ❌
9. **Workflow completes** - if all steps pass, workflow succeeds ✅

### What Happens on Failure?

- ❌ **Workflow fails**: GitHub shows a red X on the commit
- 📧 **Developer is notified**: Email notification about the failure
- 🔍 **Logs are available**: Developer can view detailed logs to debug
- 🚫 **Deployment blocked**: Failed code doesn't get deployed

### What Happens on Success?

- ✅ **Workflow succeeds**: GitHub shows a green checkmark
- 📝 **Code is verified**: All tests passed, code is safe
- 🚀 **Ready for merge**: Code can be merged to main branch
- 📊 **Build badge updates**: README badges show passing status

---

## Best Practices for CI/CD

### 1. Write Good Tests
- Cover all critical functionality
- Test edge cases and error conditions
- Keep tests fast and reliable

### 2. Keep Workflows Fast
- Only run necessary tests
- Use caching when possible
- Parallelize independent jobs

### 3. Fix Failures Immediately
- Don't push more code on top of failures
- Investigate and fix the root cause
- Learn from failures to prevent recurrence

### 4. Monitor Your Pipeline
- Check workflow status regularly
- Review failed runs promptly
- Keep dependencies up to date

---

## Common Issues and Solutions

### Issue 1: Tests Pass Locally but Fail in CI/CD

**Cause**: Environment differences (missing dependencies, different Python version)  
**Solution**: 
- Ensure `requirements.txt` includes all dependencies
- Match Python version locally and in CI/CD
- Check for environment-specific code

### Issue 2: Workflow Takes Too Long

**Cause**: Too many tests, slow dependencies  
**Solution**:
- Run only changed tests first
- Use caching for dependencies
- Parallelize test execution

### Issue 3: Flake8 Errors

**Cause**: Code style violations or syntax errors  
**Solution**:
- Run `flake8` locally before pushing
- Use IDE plugins for real-time linting
- Configure flake8 rules in `.flake8` file

---

## Summary

This CI/CD pipeline ensures that:
- ✅ Code is automatically tested on every push
- ✅ Syntax errors are caught before tests run
- ✅ All tests must pass before code can be merged
- ✅ Consistent environment across all developers
- ✅ Fast feedback on code quality

**Key Takeaway**: CI/CD automates quality checks, making development faster and safer. Every push is automatically validated, ensuring only working code makes it to production.
