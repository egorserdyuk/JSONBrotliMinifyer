<!-- omit in toc -->
# Contributing to JSONBrotliMinifyer

First off, thanks for taking the time to contribute! ❤️

All types of contributions are encouraged and valued. See the [Table of Contents](#table-of-contents) for different ways to help and details about how this project handles them. Please make sure to read the relevant section before making your contribution. It will make it a lot easier for us maintainers and smooth out the experience for all involved. The community looks forward to your contributions. 🎉

> And if you like the project, but just don't have time to contribute, that's fine. There are other easy ways to support the project and show your appreciation, which we would also be very happy about:
> - Star the project
> - Tweet about it
> - Refer this project in your project's readme
> - Mention the project at local meetups and tell your friends/colleagues

<!-- omit in toc -->
## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [I Have a Question](#i-have-a-question)
  - [I Want To Contribute](#i-want-to-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Enhancements](#suggesting-enhancements)
  - [Your First Code Contribution](#your-first-code-contribution)
  - [Improving The Documentation](#improving-the-documentation)
- [Styleguides](#styleguides)
  - [Commit Messages](#commit-messages)
- [Join The Project Team](#join-the-project-team)


## Code of Conduct

This project and everyone participating in it is governed by the
[JSONBrotliMinifyer Code of Conduct](https://github.com/egorserdyuk/JSONBrotliMinifyer/blob/main/CODE_OF_CONDUCT.md).
By participating, you are expected to uphold this code. Please report unacceptable behavior
to <raychessbot@gmail.com>.


## I Have a Question

> If you want to ask a question, we assume that you have read the available [Documentation](https://github.com/egorserdyuk/JSONBrotliMinifyer/blob/main/README.md).

Before you ask a question, it is best to search for existing [Issues](https://github.com/egorserdyuk/JSONBrotliMinifyer/issues) that might help you. In case you have found a suitable issue and still need clarification, you can write your question in this issue. It is also advisable to search the internet for answers first.

If you then still feel the need to ask a question and need clarification, we recommend the following:

- Open an [Issue](https://github.com/egorserdyuk/JSONBrotliMinifyer/issues/new).
- Provide as much context as you can about what you're running into.
- Provide project and platform versions (nodejs, npm, etc), depending on what seems relevant.

We will then take care of the issue as soon as possible.

<!--
You might want to create a separate issue tag for questions and include it in this description. People should then tag their issues accordingly.

Depending on how large the project is, you may want to outsource the questioning, e.g. to Stack Overflow or Gitter. You may add additional contact and information possibilities:
- IRC
- Slack
- Gitter
- Stack Overflow tag
- Blog
- FAQ
- Roadmap
- E-Mail List
- Forum
-->

## I Want To Contribute

> ### Legal Notice <!-- omit in toc -->
> When contributing to this project, you must agree that you have authored 100% of the content, that you have the necessary rights to the content and that the content you contribute may be provided under the project licence.

### Reporting Bugs

<!-- omit in toc -->
#### Before Submitting a Bug Report

A good bug report shouldn't leave others needing to chase you up for more information. Therefore, we ask you to investigate carefully, collect information and describe the issue in detail in your report. Please complete the following steps in advance to help us fix any potential bug as fast as possible.

- Make sure that you are using the latest version.
- Determine if your bug is really a bug and not an error on your side e.g. using incompatible environment components/versions (Make sure that you have read the [documentation](https://github.com/egorserdyuk/JSONBrotliMinifyer/blob/main/README.md). If you are looking for support, you might want to check [this section](#i-have-a-question)).
- To see if other users have experienced (and potentially already solved) the same issue you are having, check if there is not already a bug report existing for your bug or error in the [bug tracker](https://github.com/egorserdyuk/JSONBrotliMinifyer/issues?q=label%3Abug).
- Also make sure to search the internet (including Stack Overflow) to see if users outside of the GitHub community have discussed the issue.
- Collect information about the bug:
  - Stack trace (Traceback)
  - OS, Platform and Version (Windows, Linux, macOS, x86, ARM)
  - Version of the interpreter, compiler, SDK, runtime environment, package manager, depending on what seems relevant.
  - Possibly your input and the output
  - Can you reliably reproduce the issue? And can you also reproduce it with older versions?

<!-- omit in toc -->
#### How Do I Submit a Good Bug Report?

> You must never report security related issues, vulnerabilities or bugs including sensitive information to the issue tracker, or elsewhere in public. Instead sensitive bugs must be sent by email to <raychessbot@gmail.com>.
<!-- You may add a PGP key to allow the messages to be sent encrypted as well. -->

We use GitHub issues to track bugs and errors. If you run into an issue with the project:

- Open an [Issue](https://github.com/egorserdyuk/JSONBrotliMinifyer/issues/new). (Since we can't be sure at this point whether it is a bug or not, we ask you not to talk about a bug yet and not to label the issue.)
- Explain the behavior you would expect and the actual behavior.
- Please provide as much context as possible and describe the *reproduction steps* that someone else can follow to recreate the issue on their own. This usually includes your code. For good bug reports you should isolate the problem and create a reduced test case.
- Provide the information you collected in the previous section.

Once it's filed:

- The project team will label the issue accordingly.
- A team member will try to reproduce the issue with your provided steps. If there are no reproduction steps or no obvious way to reproduce the issue, the team will ask you for those steps and mark the issue as `needs-repro`. Bugs with the `needs-repro` tag will not be addressed until they are reproduced.
- If the team is able to reproduce the issue, it will be marked `needs-fix`, as well as possibly other tags (such as `critical`), and the issue will be left to be [implemented by someone](#your-first-code-contribution).

<!-- You might want to create an issue template for bugs and errors that can be used as a guide and that defines the structure of the information to be included. If you do so, reference it here in the description. -->


### Suggesting Enhancements

This section guides you through submitting an enhancement suggestion for JSONBrotliMinifyer, **including completely new features and minor improvements to existing functionality**. Following these guidelines will help maintainers and the community to understand your suggestion and find related suggestions.

<!-- omit in toc -->
#### Before Submitting an Enhancement

- Make sure that you are using the latest version.
- Read the [documentation](https://github.com/egorserdyuk/JSONBrotliMinifyer/blob/main/README.md) carefully and find out if the functionality is already covered, maybe by an individual configuration.
- Perform a [search](https://github.com/egorserdyuk/JSONBrotliMinifyer/issues) to see if the enhancement has already been suggested. If it has, add a comment to the existing issue instead of opening a new one.
- Find out whether your idea fits with the scope and aims of the project. It's up to you to make a strong case to convince the project's developers of the merits of this feature. Keep in mind that we want features that will be useful to the majority of our users and not just a small subset. If you're just targeting a minority of users, consider writing an add-on/plugin library.

<!-- omit in toc -->
#### How Do I Submit a Good Enhancement Suggestion?

Enhancement suggestions are tracked as [GitHub issues](https://github.com/egorserdyuk/JSONBrotliMinifyer/issues).

- Use a **clear and descriptive title** for the issue to identify the suggestion.
- Provide a **step-by-step description of the suggested enhancement** in as many details as possible.
- **Describe the current behavior** and **explain which behavior you expected to see instead** and why. At this point you can also tell which alternatives do not work for you.
- You may want to **include screenshots or screen recordings** which help you demonstrate the steps or point out the part which the suggestion is related to. You can use [LICEcap](https://www.cockos.com/licecap/) to record GIFs on macOS and Windows, and the built-in [screen recorder in GNOME](https://help.gnome.org/users/gnome-help/stable/screen-shot-record.html.en) or [SimpleScreenRecorder](https://github.com/MaartenBaert/ssr) on Linux. <!-- this should only be included if the project has a GUI -->
- **Explain why this enhancement would be useful** to most JSONBrotliMinifyer users. You may also want to point out the other projects that solved it better and which could serve as inspiration.

<!-- You might want to create an issue template for enhancement suggestions that can be used as a guide and that defines the structure of the information to be included. If you do so, reference it here in the description. -->

### Your First Code Contribution

#### Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.9 or higher
- Git
- pip (Python package installer)

#### Development Setup

1. **Fork the repository** on GitHub and clone your fork:

   ```bash
   git clone https://github.com/YOUR_USERNAME/JSONBrotliMinifyer.git
   cd JSONBrotliMinifyer
   ```

2. **Set up a virtual environment** (recommended):

   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -e .
   pip install -r requirements.txt  # if additional dev dependencies exist
   ```

4. **Verify the installation**:

   ```bash
   python -c "import jsonbrotliminifyer; print('Installation successful!')"
   ```

#### Running Tests

Before making changes, ensure all tests pass:

```bash
# Using unittest
python -m unittest tests.test_jsonbrotliminifyer

# Or using pytest (if installed)
pytest tests/test_jsonbrotliminifyer.py
```

#### Making Changes

1. Create a new branch for your changes:

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your code changes following the project's style guidelines.

3. Add tests for your changes if applicable.

4. Run tests to ensure everything works:

   ```bash
   python -m unittest tests.test_jsonbrotliminifyer
   ```

5. Commit your changes with a clear commit message.

6. Push to your fork and create a pull request.

#### Code Style

- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Write docstrings for functions and classes
- Ensure code is compatible with Python 3.9+

For more details on commit message format, see the [Commit Messages](#commit-messages) section below.

### Improving The Documentation

Documentation is crucial for users to understand and effectively use JSONBrotliMinifyer. We welcome contributions that improve clarity, add examples, fix errors, or expand coverage.

#### Types of Documentation

- **README.md**: Main project documentation with installation, usage examples, and API reference
- **Code Documentation**: Docstrings in Python files following Google/NumPy style
- **CONTRIBUTING.md**: This file with contribution guidelines
- **GitHub Wiki**: Additional guides, tutorials, and FAQs (if applicable)

#### How to Contribute Documentation

1. **Identify areas for improvement**:
   - Outdated information
   - Missing examples
   - Unclear explanations
   - Broken links
   - Missing API documentation

2. **Follow documentation standards**:
   - Use clear, concise language
   - Include practical code examples
   - Keep examples up-to-date with current API
   - Test all code examples to ensure they work

3. **Update README.md**:
   - Keep installation instructions current
   - Add new features to the Features section
   - Update API documentation when functions change
   - Maintain accurate command-line examples

4. **Improve code documentation**:
   - Add docstrings to new functions/classes
   - Update existing docstrings when behavior changes
   - Include parameter types and descriptions
   - Add examples in docstrings where helpful

5. **Test documentation changes**:
   - Verify all links work
   - Test code examples
   - Check formatting renders correctly on GitHub

#### Documentation Style Guidelines

- Use Markdown for all documentation files
- Follow consistent heading hierarchy
- Use code blocks with appropriate language syntax highlighting
- Include table of contents for longer documents
- Keep line lengths reasonable for readability

When submitting documentation changes, include a brief explanation of what was improved and why it benefits users.

## Styleguides

### Commit Messages

We follow the [Conventional Commits](https://conventionalcommits.org/) specification for commit messages. This format helps maintain a clear and structured commit history.

#### Format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

#### Types

- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation only changes
- **style**: Changes that do not affect the meaning of the code (white-space, formatting, etc.)
- **refactor**: A code change that neither fixes a bug nor adds a feature
- **perf**: A code change that improves performance
- **test**: Adding missing tests or correcting existing tests
- **build**: Changes that affect the build system or external dependencies
- **ci**: Changes to our CI configuration files and scripts
- **chore**: Other changes that don't modify src or test files

#### Examples

```
feat: add support for custom compression quality levels

fix: handle empty JSON objects in decompress_json function

docs: update README with new CLI examples

refactor: simplify compression algorithm in compress_json_file

test: add unit tests for error handling in CLI
```

#### Guidelines

- Use the imperative mood in the subject line ("Add feature" not "Added feature")
- Keep the subject line under 50 characters
- Start the subject line with a capital letter
- Do not end the subject line with a period
- Use the body to explain what and why (not how)
- Wrap the body at 72 characters
- Use the footer to reference issues (e.g., "Closes #123")

#### Breaking Changes

For commits that introduce breaking changes, add a `BREAKING CHANGE:` footer or append `!` to the type/scope:

```
feat!: remove deprecated compress_file function

BREAKING CHANGE: compress_file has been removed, use compress_json_file instead
```

## Join The Project Team

We welcome contributors who demonstrate consistent quality contributions and commitment to the project. Becoming a team member is based on merit and ongoing engagement.

### Ways to Get Involved

1. **Regular Contributor**: Submit high-quality pull requests and help with issue triage
2. **Maintainer**: Help review pull requests, manage issues, and guide new contributors
3. **Core Team**: Participate in project planning, architectural decisions, and long-term vision

### Requirements for Team Membership

- **Consistent Contributions**: Regular, high-quality code contributions over several months
- **Code Review Participation**: Help review other contributors' pull requests
- **Community Engagement**: Help answer questions in issues and discussions
- **Project Knowledge**: Deep understanding of the codebase and project goals
- **Communication**: Clear and respectful interaction with the community

### Application Process

If you're interested in joining the team:

1. **Demonstrate Commitment**: Contribute regularly for at least 3-6 months
2. **Express Interest**: Contact the current maintainers via email (raychessbot@gmail.com) or create a GitHub issue
3. **Interview/Assessment**: Discuss your experience and vision for the project
4. **Trial Period**: Start with maintainer responsibilities under supervision

### Current Team

- **Egor Serdiuk** (Project Lead) - egor.serduck@gmail.com

### Recognition

Active team members may be:
- Added to the project repository with appropriate permissions
- Listed in README.md or project documentation
- Given recognition in release notes

We value diversity and inclusion in our team and welcome contributors from all backgrounds and experience levels.

<!-- omit in toc -->
## Attribution
This guide is based on the [contributing.md](https://contributing.md/generator)!
