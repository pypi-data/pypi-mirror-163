# delta-env
This is a very simple tool to report environment variable changes when a shell script is sourced. Useful while creating [modulefiles](https://lmod.readthedocs.io/en/latest/) for various applications that are shipped with scripts that set up the user environment.

This package does not depend on any additional python packages, only requirement is ```python > 3.0.0```. **Does not work on Windows operating system.**

What the tool does is simply sourcing the given script and reporting differences from the default environment variables in an organized way.

> **WARNING** This tool WILL carry out the actions in the given script to be analyzed. If it is of harmful nature, damage will be done. Do NOT run this tool as ```root```. Do NOT run this tool with scripts that are of unknown/unstrusted sources!

## Installation
Clone this repository, ```cd``` into the cloned directory, and install via ```pip```,

```
pip install .
```

## Usage
This tool is meant to be used from the command line via the executable ```delta-env```,

```
delta-env <path-to-script>
```

The output will be displayed in the terminal screen, reporting added, removed and modified environment variables seperately.

By default, modifications are reported with respect to the **default user environment** that is present after creation of a login shell. This behaviour can be changed by using the ```--from-current``` argument to use the current environment (where ```delta-env``` is executed) as basis. Note that environment variables that were created without the ```export``` command will not be passed to subprocesses, and hence will not be visible to ```delta-env```.

If no shell executable is supplied via ```--shell <path-to-shell>``` argument, it is obtained from the value of environment variable ```SHELL```.

