[[_TOC_]]

![Coverage](https://gitlab.ics.muni.cz/beast-public/cryton/cryton-cli/badges/master/coverage.svg)

# Cryton CLI

## Description
Cryton CLI is a command line interface used to interact with [Cryton Core](https://gitlab.ics.muni.cz/beast-public/cryton/cryton-core) (its API).

To be able to execute attack scenarios, you also need to install **[Cryton Core](https://gitlab.ics.muni.cz/beast-public/cryton/cryton-core)** 
and **[Cryton Worker](https://gitlab.ics.muni.cz/beast-public/cryton/cryton-worker)** package.

Cryton toolset is tested and targeted primarily on **Debian** and **Kali Linux**, however it **should** be possible to 
use it everywhere if the requirements are met. Please keep in mind that **only the latest version is supported** and 
issues regarding different OS or distributions may **not** be resolved.

[Link to the documentation](https://beast-public.gitlab-pages.ics.muni.cz/cryton/cryton-documentation/).

## Settings
Cryton CLI uses environment variables for its settings. Please update them to your needs.

| name                      | value   | example        | description                                                                                                                                                                                     |
|---------------------------|---------|----------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| CRYTON_CLI_TIME_ZONE      | string  | AUTO           | What [timezone](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) to use for scheduling (for example when scheduling a run). <br> Use the `AUTO` value to use your system timezone. |
| CRYTON_CLI_API_HOST       | string  | 127.0.0.1      | REST API address used for connection                                                                                                                                                            |
| CRYTON_CLI_API_PORT       | int     | 8000           | REST API port used for connection                                                                                                                                                               |
| CRYTON_CLI_API_SSL        | boolean | false          | Use SSL to connect to REST API                                                                                                                                                                  |
| CRYTON_CLI_API_ROOT       | string  | api/           | REST API URL **(do not change, if you don't know what you're doing)**                                                                                                                           |
| CRYTON_CLI_APP_DIRECTORY  | string  | ~/.cryton-cli/ | Path to the Cryton CLI directory. **(do not change/set/export, if you don't know what you're doing)** <br> If changed, update the commands in this guide accordingly.                           |

To store the settings, we will **create an app directory**:
```shell
mkdir ~/.cryton-cli/
```

Next, we download example settings (**change the version to match the app version**):
```shell
curl -o ~/.cryton-cli/.env https://gitlab.ics.muni.cz/beast-public/cryton/cryton-cli/-/raw/<version>/.env
```
Update these settings to your needs.

To override the persistent settings, you can set/export the variables yourself using the **export** command 
(use **unset** to remove the variable). For example:
```shell
export CRYTON_CLI_API_HOST=127.0.0.1
```

Some environment variables can be overridden in CLI. Try using `cryton-cli --help`.

## Installation
Cryton CLI is available in the PyPI and can be simply installed using `pip`. However, we recommend installing the app 
in an isolated environment using [pipx](https://pypa.github.io/pipx/).

**Requirements**
- [Python](https://www.python.org/about/gettingstarted/) >=3.8
- [pipx](https://pypa.github.io/pipx/)

First, install the requirements:
```shell
apt install python3
apt install pipx
```

Optionally check respective guides if you prefer a different installation method:
- [Python](https://www.python.org/about/gettingstarted/)
- [pipx](https://pypa.github.io/pipx/)

Make sure that the requirements are satisfied:
```shell
python3 --version
pipx --version
```

Once you have *pipx* ready on your system, you can start the installation:
```shell
pipx install cryton-cli
```

Make sure you've correctly set the [settings](#settings).

Optionally, you can set up [shell completion](#shell-completion)

Everything should be set. Check if the installation was successful:
```shell
cryton-cli
```

You should see a help page:
```
Usage: cryton-cli [OPTIONS] COMMAND [ARGS]...

  A CLI wrapper for Cryton API.

Options:
  ...
```

## Development
To install Cryton CLI for development, you have to install [Poetry](https://python-poetry.org/docs/).

Then go to the correct directory, create shell, and install the project.
```shell
cd cryton-cli
poetry shell
poetry install
```

Make sure you've correctly set the [settings](#settings).  
To override the settings quickly, you can use this handy oneliner:
```shell
export $(grep -v '^#' .env | xargs)
```

Optionally, you can set up [shell completion](#shell-completion)

Everything should be set. Check if the installation was successful:
```shell
cryton-cli
```

You should see a help page:
```
Usage: cryton-cli [OPTIONS] COMMAND [ARGS]...

  A CLI wrapper for Cryton API.

Options:
  ...
```

## Usage
**IMPORTANT: Please keep in mind that the [Cryton Core](https://gitlab.ics.muni.cz/beast-public/cryton/cryton-core) 
must be running and its API must be reachable.**

To change the default API host/port use *-H* and *-p* options (to change them permanently, see the [settings section](#settings)).
```shell
cryton-cli -H 127.0.0.1 -p 8000 <your command>
```

**To learn about each command's options use**:
```shell
cryton-cli <your command> --help
```

For a better understanding of the results, we highlight the successful ones with **green** and the others with **red** color.

### Example
#### 1. Create plan template
Create a Plan template using a file containing the desired plan YAML.
```shell
cryton-cli plan-templates create my-plan.yml
```

Desired output:
```
Template successfully created! (<response detail>).
```

#### 2. Create Plan instance
Create a Plan instance with the saved plan template.
```shell
cryton-cli plans create 1
```

Create a Plan instance using the template and an inventory file.
```shell
cryton-cli plans create 1 -i inventory_file
```

Desired output:
```
Plan successfully created! (<response detail>).
```

#### 3. Create Worker
To execute Plans (Runs) we have to define a Worker(s).
```shell
cryton-cli workers create customName -d "This is my first Worker!"
```

Desired output:
```
Worker successfully created! (<response detail>).
```

#### 4. Create Run
Create a Run by choosing a Plan instance and providing a list of Workers for execution.
```shell
cryton-cli runs create 1 1
```

Desired output:
```
Run successfully created! (<response detail>).
```

#### 5. Schedule or Execute Run
You can either Schedule the Run for a specific date/time or execute it directly. Run will then be executed on every Worker 
simultaneously.

**Execute Run**
```shell
cryton-cli runs execute 1
```

Desired output:
```
Run successfully executed! (Run 1 was executed.).
```

**Schedule Run**
You can schedule a Run using the local timezone.
```shell
cryton-cli runs schedule 1 2020-06-08 10:00:00
```

Desired output:
```
Run successfully scheduled! (Run 1 is scheduled for 2020-06-08 10:00:00.).
```

Or you can schedule it using UTC timezone with the flag `--utc-timezone`. Otherwise, your preset timezone is used.

#### 6. Read Run report
Anytime during the execution, a report can be generated, which also complies with YAML format, and it contains a list of 
Stages/Steps and their results. Timestamps are by default displayed in UTC timezone, use the `--localize` flag to display 
them using your preset timezone.
```shell
cryton-cli runs report 1
```

Desired output:
```
Successfully created Run's report! (file saved at: /tmp/report_run_1_2020-06-08-10-15-00-257994_xdQeV)
```

## Shell completion
Shell completion is available for the *Bash*, *Zsh*, and *Fish* shell and has to be manually enabled.

### Bash
First, **create an app directory** (if you haven't already):
```shell
mkdir ~/.cryton-cli/
```

Download the completion file (**change the version to match the app version**):
```shell
curl -o ~/.cryton-cli/.cryton-cli-complete.bash https://gitlab.ics.muni.cz/beast-public/cryton/cryton-cli/-/raw/<version>/.cryton-cli-complete.bash
```

Source the file in the `~/.bashrc` file:
```shell
echo ". ~/.cryton-cli/.cryton-cli-complete.bash" >> ~/.bashrc
```

After modifying the shell config, start a new shell to load the changes.

### Zsh
First, **create an app directory** (if you haven't already):
```shell
mkdir ~/.cryton-cli/
```

Download the completion file (**change the version to match the app version**):
```shell
curl -o ~/.cryton-cli/.cryton-cli-complete.zsh https://gitlab.ics.muni.cz/beast-public/cryton/cryton-cli/-/raw/<version>/.cryton-cli-complete.zsh
```

Source the file in the `~/.zshrc` file:
```shell
echo ". ~/.cryton-cli/.cryton-cli-complete.zsh" >> ~/.zshrc
```

After modifying the shell config, start a new shell to load the changes.

### Fish
Download the completion file (**change the version to match the app version**):
```shell
curl -o ~/.config/fish/completions/.cryton-cli-complete.fish https://gitlab.ics.muni.cz/beast-public/cryton/cryton-cli/-/raw/<version>/.cryton-cli-complete.fish
```

After modifying the shell config, start a new shell to load the changes.
