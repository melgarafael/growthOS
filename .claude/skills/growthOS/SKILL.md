```markdown
# growthOS Development Patterns

> Auto-generated skill from repository analysis

## Overview
This skill teaches the core development patterns and conventions used in the `growthOS` TypeScript codebase. It covers file organization, code style, commit message standards, and testing patterns to help contributors maintain consistency and quality.

## Coding Conventions

### File Naming
- **Pattern:** PascalCase
- **Example:**  
  `UserProfile.ts`  
  `OrderManager.ts`

### Import Style
- **Pattern:** Relative imports
- **Example:**
  ```typescript
  import { UserService } from '../services/UserService';
  ```

### Export Style
- **Pattern:** Named exports
- **Example:**
  ```typescript
  export function calculateGrowth() { ... }
  export const GROWTH_RATE = 1.05;
  ```

### Commit Messages
- **Pattern:** Conventional Commits
- **Prefix Used:** `feat`
- **Average Length:** ~44 characters
- **Example:**
  ```
  feat: add user onboarding flow
  ```

## Workflows

### Creating a New Feature
**Trigger:** When adding a new functionality or module  
**Command:** `/new-feature`

1. Create a new file using PascalCase (e.g., `NewFeature.ts`).
2. Use relative imports to include dependencies.
3. Export your functions or constants using named exports.
4. Write corresponding tests in a file named `NewFeature.test.ts`.
5. Commit your changes with a message starting with `feat:` and a concise description.

### Writing Tests
**Trigger:** When verifying the correctness of a module  
**Command:** `/write-test`

1. Create a test file alongside your module, following the pattern `*.test.ts` (e.g., `UserProfile.test.ts`).
2. Implement test cases for all exported functions and constants.
3. Run your tests using the project's test runner (framework is currently unknown).

### Making a Commit
**Trigger:** When saving changes to version control  
**Command:** `/commit`

1. Stage your changes.
2. Write a commit message starting with `feat:` followed by a brief summary (max ~44 chars).
3. Push your commit to the repository.

## Testing Patterns

- **File Pattern:** All test files follow the `*.test.ts` naming convention.
- **Location:** Test files are placed alongside the modules they test.
- **Framework:** Not explicitly detected; use the project's preferred test runner.
- **Example:**
  ```typescript
  // UserProfile.test.ts
  import { getUserName } from './UserProfile';

  test('should return correct user name', () => {
    expect(getUserName({ name: 'Alice' })).toBe('Alice');
  });
  ```

## Commands
| Command        | Purpose                                            |
|----------------|----------------------------------------------------|
| /new-feature   | Scaffold a new feature/module with conventions     |
| /write-test    | Create a test file for a module                    |
| /commit        | Make a conventional commit with proper formatting  |
```
