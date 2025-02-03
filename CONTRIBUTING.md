## Pull Request Naming Guidelines

To keep the repository organized and to make it easier to understand the purpose of each pull request, the project follows these pull request naming conventions:

### Format

Each pull request name should include a type and a short description:

`<type>: <short-description></type>`

### Types

Use one of the following types:

- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation only changes
- **style**: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
- **refactor**: A code change that neither fixes a bug nor adds a feature
- **perf**: A code change that improves performance
- **test**: Adding missing or correcting existing tests
- **build**: Changes that affect the build system or external dependencies
- **ci**: Changes to the CI configuration files and scripts
- **chore**: Other changes that don't modify src or test files
- **revert**: Reverts a previous commit

### Examples

- `feat: add login feature`
- `fix: bug in authentication`
- `docs: update readme`
- `chore: cleanup dependencies`
- `refactor: improve parser`

By following these guidelines, you help ensure that the branches are easy to understand and manage.

## Commit Message Guidelines

This project follows the commit message conventions set by [Conventional Commits](https://www.conventionalcommits.org/).

### Commit Message Format

Each commit message should include a type, a scope (optional), and a subject:

`<type>(<scope>): <subject></subject></scope></type>`

#### Type

Must be one of the following:

- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation only changes
- **style**: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
- **refactor**: A code change that neither fixes a bug nor adds a feature
- **perf**: A code change that improves performance
- **test**: Adding missing or correcting existing tests
- **build**: Changes that affect the build system or external dependencies (example scopes: gulp, broccoli, npm)
- **ci**: Changes to our CI configuration files and scripts (example scopes: Travis, Circle, BrowserStack, SauceLabs)
- **chore**: Other changes that don't modify src or test files
- **revert**: Reverts a previous commit

#### Subject

The subject contains a succinct description of the change:

- Use the imperative, present tense: "change" not "changed" nor "changes"
- Do not capitalize the first letter
- Do not end the subject with a period

### Examples

```plaintext
feat(parser): add support for new weather condition
 
fix(translation): correct French translation for 'clear sky'

docs(contributing): add commit message guidelines
```

By following these guidelines, you help ensure that the project remains consistent and easy to understand.


## Internationalization
 
If you are willing to add a new language or complete an existing language, please use https://crwd.in/metarParser to register and contribute. 
Once a language is complete at 100%, open an issue so the translation can be added to the project.
