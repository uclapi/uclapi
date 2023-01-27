# UCL API ![build](https://img.shields.io/github/actions/workflow/status/uclapi/uclapi/workflow.yml?label=build) ![staging](https://img.shields.io/github/actions/workflow/status/uclapi/uclapi/workflow.yml?label=staging) [![codecov](https://codecov.io/gh/uclapi/uclapi/branch/master/graph/badge.svg)](https://codecov.io/gh/uclapi/uclapi)

## What is the UCL API?
UCL API started as a **student-built** platform for **student developers** to improve the **student experience** of everyone at UCL. We now also have our own end-user facing applications in addition to this, such as UCL Assistant, our rival app to UCL GO.

### Our Goal
Create a ridiculously simple, documentation first, and comprehensive API around UCL's digital services and establish an ecosystem of third party UCL apps and services that use the API. Find out more at our [website](https://uclapi.com) or if you feel brave try [staging](https://staging.ninja).

### Interested in helping build it?
Read on more to find out how to setup and build the API. From here you can start writing your own changes and submitting them. See our [Contribution Guide](CONTRIBUTING.md) to learn more about how you can contribute.

## Setup in 10 Minutes
For this setup to work you need to have docker, git, python (3.7), and node + npm installed. If you would like the old setup guide (without docker) that can be found [here](README_SETUP.md), it also contains some advanced information for maintainers. This guide has been tested to work on Windows (we recommend PowerShell Core), Linux, and MacOS.

Clone uclapi to a local directory
```bash
git clone https://github.com/uclapi/uclapi.git
cd uclapi
```

Then start the development docker compose file
```bash
docker-compose -f docker-compose-dev.yml up
```

In the meantime you can create your Python virtual environment (you may need to write `python` instead of `python3`)
```bash
cd backend/uclapi
cp .env.docker.example .env
python3 -m venv ./venv

# For unix:
source ./venv/bin/activate
# For windows:
./venv/Scripts/activate

# Then
pip install -r requirements.txt
```

And setup the frontned
```bash
cd frontend
npm install
npm start
```

### Give it a go!
If those commands work you should be able to navigate to `http://localhost:8000/dashboard` in your browser, which will let you log in via Fake Shibboleth running on `http://localhost:8001`. If so, then you're up and running!

## Testing
We're an amazing project, so obviously we have tests :sparkles:. Make sure you have the requirements installed in your virtual environment (and you have activated it) , `cd` into `backend/uclapi` and then run :  
`python manage.py test --settings=uclapi.settings_mocked`

## Linting
We have a pre-commit hook set up that runs [eslint](https://eslint.org/) on all staged JS files, [stylelint](https://github.com/stylelint/stylelint) on all staged scss files, and [autopep8](https://github.com/hhatto/autopep8) & [flake8](http://flake8.pycqa.org/en/latest/) on all staged Python files. This automatically fixes style issues and stops the commit if there are any obvious problems (e.g. failure to define variable).

## Documentation
As well as the user-facing documentation we also now ship our own internal Documentation which aims to help developers contribute to our code. To make it simply run ```make html``` while in the backend directory. You can then navigate to the build directory and open up index.html in your favourite browser to view the documentation. It can also be built in pdf, latex and a few other formats.
