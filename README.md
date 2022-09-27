# Coding Style

## Repository Structure

- dot-files
- git-hooks
- examples
- linter.py
- install.sh
- style.md
- (README.md)

The "dot-files" contains configuration files for git and clang.
Those files are usually located in the home or .git directory and precedet with a dot to be hidden on default.

The "git-hooks" contain shell scripts which are automatically triggered by running the corresponding git command.

The "examples" directory contains sample files such as commit messages.

The "linter.py" python script gets called by the "pre-commit" hook for verifying the correct formatting of the code as well as for performing static code analysis.
The logic for handling different programming languages should be added to the "linter.py" script.</br>
Additionally, a ".lint_ignore" file can be manually added to the toplevel of a git repository.
Files or directories which should be ignored by "linter.py" are added to this file.

The "install.sh" shell script installs the git hooks and commit message template to the target repository.

The "style.md" file can be used as a reference for the rules which are applied to C/C++ source files.


## Apply Settings
Use the "install.sh" script to install the git hooks to the target
repository.</br>

The script sets up symbolic links to the hooks located in the "git\-hooks"
directory of this repository. This way updates to either of the hooks are
automatically reflected in the repositories which were previously setup.


## Dependencies
The following packages are required:
- clang-format
- cppcheck
- python3


## Known Issues
Clang-format is currently not able to automatically detect or insert missing
newlines between functions, as shown by the example below.
This feature is only available for clang-format from version 14 onwards.
Check files manually to make sure functions are separated by a newline.

```
void function1()
{
    ...
}
void function2()
{
}
```

Configuration option for clang-format from 14 onwards.
```
SeparateDefinitionBlocks : Always
```
