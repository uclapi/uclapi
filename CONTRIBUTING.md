# Contributing to UCL API

First off, thanks for taking the time to contribute!

The following is a set of guidelines for contributing to UCL API and its packages, which are hosted in the [UCLAPI Organization](https://github.com/uclapi) on GitHub. These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

## How can I contribute?

### Security vulnerability disclosure
In case you suspect you find a vulnerability in the API, please refrain from creating an issue publicly and contact us at <isd.apiteam@ucl.ac.uk>. At the moment we do not have any bug bounty program present, but we would be happy to include you in our Hall of Fame!

### Submitting bugs

* **Use a clear and descriptive title** for the issue to identify the problem.
* **Describe the exact steps which reproduce the problem** in as many details as possible.
* **Provide specific examples to demonstrate the steps**. Include links to files or GitHub projects, or copy/pasteable snippets, which you use in those examples. If you're providing snippets in the issue, use [Markdown code blocks](https://help.github.com/articles/markdown-basics/#multiple-lines).
* **Describe the behavior you observed after following the steps** and point out what exactly is the problem with that behavior.
* **Explain which behavior you expected to see instead and why.**

### Suggesting enhancements
* **Use a clear and descriptive title** for the issue to identify the suggestion.
* **Provide a step-by-step description of the suggested enhancement** in as many details as possible.
* **Provide specific examples to demonstrate the steps**. Include copy/pasteable snippets which you use in those examples, as [Markdown code blocks](https://help.github.com/articles/markdown-basics/#multiple-lines).
* **Describe the current behavior** and **explain which behavior you expected to see instead** and why.
* **Explain why this enhancement would be useful** to our API users.

### Pull requests (PRs) and their role in submitting enhancements
* **Open a new branch** to work on your feature/bug-fix.
* **Commit your changes** to this new branch.
* **Fast forward your branch** when it's ready to merge to make sure its up to date with the master branch.
* **Open your PR.**
* **Fill in [the required PR template](.uclapi/PULL_REQUEST_TEMPLATE.md).**
* **Do not include issue numbers in the PR title**, instead refrence them at the bottom of the description saying "Closes #xx".
* **Wait** for it to pass automated checks and a code review.
* **Celebrate** your first contribution to the UCL API project!

## Style guides
Our codebase consists out of multiple languages (JavaScript for front-end, Python for back-end). You should try to follow the best guidelines for the language, meaning:

* JavaScript - it should adhere to [JavaScript Standard Style](http://standardjs.com/).
* Python - we (try to) adhere to [PEP8](https://www.python.org/dev/peps/pep-0008/), using 4 spaces per indentation level.

We use [Hound CI](https://houndci.com) to automatically check PR's for style-guide violuations. Unless all faults detected are removed, HoundCI will mark the commit as failing to build.

### Git commit messages
* Use present tense ("Improve description field" or "changing X to work with Y")
* Try to limit the commit message to 50 characters or less. You can always use multiple lines.

## Closing remarks
This document was inspired by [Atom's contribution guide](https://github.com/atom/atom/blob/master/CONTRIBUTING.md).
