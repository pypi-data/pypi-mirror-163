# depenv

Depenv varies Python classes at runtime based on environment variables. For example:

```py
import depenv

class Bird(depenv.Injectable):
  def speak(self):
    return "chirp"

class Duck(Bird):
  def speak(self):
    return "quack"
```

Without any environment variables:

```py
>>> Bird().speak()
"chirp"
>>> isinstance(Bird(), Bird)
True
>>> isinstance(Bird(), Duck)
False
```

With `DEPENV_BIRD=Duck`:

```py
>>> Bird().speak()
"quack"
>>> isinstance(Bird(), Bird)
True
>>> isinstance(Bird(), Duck)
True
```

Depenv aims to provide the benefits of [dependency injection](https://en.wikipedia.org/wiki/Dependency_injection) without the boilerplate of other dependency injection frameworks. 

## Installation

Depenv is available on PyPi:

```
pip install depenv
```

Depenv has no external dependencies and works for all [supported Python versions](https://devguide.python.org/versions/).

## Usage

When you create a new object using a class that subclasses `depenv.Injectable`, Depenv will search your environment variables for a suitable class to inject. For example:

```py
import depenv

class Bird(depenv.Injectable):
  def speak(self):
    return "chirp"

class Duck(Bird):
  def speak(self):
    return "quack"
```

All Depenv environment variables are prefixed with `DEPENV_`.

If you do not set an environment variable, Depenv will use the injectable class:

```py
>>> Bird().speak()
"chirp"
```

### Configuring the injected class

The simplest Depenv configuration specifies only the injectable class name and the injected class name. For example, with `DEPENV_BIRD=Duck`:

```py
>>> Bird().speak()
"quack"
```

If your injected class exists in a different module, you can provide an absolute path. For example, with `DEPENV_BIRD=examples.birds.Duck`:

```py
>>> Bird().speak()
"quack"
```

### Configuring the injectable class

If your injectable class shares a name with another injectable class, you can disambiguate by including a module. For example:

- `DEPENV_BIRD` will match any injectable class named `Bird` (case insensitive) in any module.
- `DEPENV_Bird` will match any injectable class named `Bird` (case sensitive) in any module.
- `DEPENV_EXAMPLES_BIRDS_BIRD` will match any injectable class named `Bird` (case insensitive) in the `examples.birds` (case insensitive) module.
- `DEPENV_examples_birds_Bird` will match the injectable class named `Bird` (case sensitive) in the `examples.birds` (case sensitive) module.

Because `.` is in invalid charcter in environment variable names, Depenv uses `_` in its place. Consequently, all of the following will matchthe environment variable `DEPENV_examples_birds_Bird`:

- `examples.birds.Bird`
- `examples.birds_Bird`
- `examples_birds.Bird`
- `examples_birds_Bird`
