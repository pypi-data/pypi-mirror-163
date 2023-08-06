# Installing a newer Python on macOS

Open a terminal window. All the commands listed here will be typed directly there.

If you haven't already done so, start by installing [**Homebrew**](https://brew.sh) which will let us easily install the packages we need. This is done by entering the following:

```console
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Then we need to install [**pyenv**](https://github.com/pyenv/pyenv) which will let us manage different version of **Python**:

```console
brew install pyenv
```

In order to load **pyenv** automatically when opening a terminal window, you need to add the following line to your shell startup file (typically `~/.bashrc` or `~/.zshrc` depending on which shell is the default on your machine):

```console
eval "$(pyenv init -)"
```

Then restart your shell by closing and reopening your terminal window. You should now be able to list which versions of **Python** are available by typing:

```console
pyenv install --list | grep " 3\."   
```

This will give you a list such as:

```console
3.9.6
3.9.7
3.9.8
3.9.9
3.9.10
3.9.11
3.9.12
3.9.13
3.10.0
3.10.1
3.10.2
3.10.3
3.10.4
3.10.5
3.10.6
```

Now install and set as local version the latest stable version of **Python** from the list (your version may vary from this one if newer versions have been released):

```console
pyenv install -v 3.10.6
pyenv local 3.10.6
```

Finally upgrade the **Python** package manager **pip**:

```console
python -m pip install --upgrade pip
```

And you are ready to go!