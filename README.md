# Installation

This project uses pipenv to manage its dependencies. Follow online instructions to get that set up. Once you have done so, open a terminal in this project directory and type `pipenv shell` to activate the virtual environment. Then type `pipenv install` to install all of the dependencies inside the `Pipfile`.

If you cannot get pipenv set up, or would rather use regular pip, there is a `requirements.txt` file so you could just install everything that way. There is probably a way to do this with conda too.

# Git Workflow

We can use a simple version of gitflow where we each make our own feature branches off of master, one branch for each function we implement. We can then merge them back into master together to resolve anything that comes up.
