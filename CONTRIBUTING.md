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

Please follow the commit message format found in `.github/.gitmessage`, we recommend you set this as your commit message template with `git config commit.template ./.github/.gitmessage`. Please use the following format (first line for a summary and limited to 50 characters):
```
Summary format:
     area subarea: message (all lowercase)
Summary examples:
     backend search: add new search function
  or backend workspaces: add historical endpoint
  or frontend pages: fix 404 page location
  or github actions: refactor CI

Use the following verbs:
  add = Create a capability e.g. feature, test, dependency.
  drop = Delete a capability e.g. feature, test, dependency.
  fix = Fix an issue e.g. bug, typo, accident, misstatement.
  bump = Increase the version of something e.g. a dependency.
  make = Change the build process, or tools, or infrastructure.
  start = Begin doing something; e.g. enable a toggle, feature flag, etc.
  stop = End doing something; e.g. disable a toggle, feature flag, etc.
  optimize = A change that MUST be just about performance, e.g. speed up code.
  document = A change that MUST be only in the documentation, e.g. help files.
  refactor = A change that MUST be just refactoring.
  reformat = A change that MUST be just format, e.g. indent line, trim space, etc.
  rephrase = A change that MUST be just textual, e.g. edit a comment, doc, etc.
```

## Closing remarks
This document was inspired by [Atom's contribution guide](https://github.com/atom/atom/blob/master/CONTRIBUTING.md).
