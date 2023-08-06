![](https://byob.yarr.is/girvel/tiny_storage/coverage)

# Summary

Library for application data storage. It is:

- tiny
- key-value
- single-file
- YAML based

## Example

```py
from tiny_storage import Unit, Type
import sys

# matches the file /etc/example-app/yaml or %PROGRAMDATA%\example-app\config.yaml
config = Unit('example-app', Type.global_config)

if sys.argv[1] == 'set-greeting':
  # changes greeting only if does not exist
  if not config('lines.greeting').try_put(sys.argv[2]):
    print('Greeting already exists. It should not be changed.')
else:
  # prints greeting if it exists or given string
  print(config('lines.greeting').pull('Hello, world!'))
```

## Installation

```shell
pip install tiny_storage
```

# Full guide as a tiny_storage iceberg

## 1. Hello world

![](iceberg/1.jpg)

Suppose you want to store a configuration of your application between sessions.

```python
from tiny_storage import Unit

# create a storage unit
config = Unit('application-name')

# write the data
config('the-best-number-ever').push(42)
```

The code above will create a YAML configuration file in the appropriate place and save the number 42 as `the-best-number-ever` entry.

## 2. Accessing data

![](iceberg/2.jpg)

Syntax for accessing data is the following:

```python
config('<dot separated path in config>').<access method>(<alternative value>)
```

There are 5 access methods in total, but the get/set functionality is realized in pull/push methods.

```python
config('essential.greeting').pull('hello')  # get a greeting from config or 'hello'
config('essential.greeting').push('hi')     # set a greeting as 'hi'
```

## 3. Storing config in different places

![](iceberg/3.jpg)

You can define what type of config do you need and tiny_storage will choose the place according to standard of your OS. For example, to store data in global configuration file you pass `Type.global_config` to your storage unit definition, and it will go to `/etc` in linux and to `%PROGRAM_DATA%` in windows.

```python
from tiny_storage import Unit, Type

config = Unit('application-name', Type.global_config)
```

The list of all config types:

| Data type            | Windows                            | Linux                          |
|----------------------|------------------------------------|--------------------------------|
| `Type.local`         | `{name}.yaml`                      | `{name}.yaml`                  |
| `Type.user`          | `%APPDATA%/{name}/{name}.yaml`     | `$HOME/.{name}.yaml`           |
| `Type.user_config `  | `%APPDATA%/{name}/config.yaml`     | `$HOME/.config/{name}.yaml`    |
| `Type.global_data`   | `%PROGRAMDATA%/{name}/data.yaml`   | `/var/lib/{name}.yaml`         |
| `Type.global_config` | `%PROGRAMDATA%/{name}/config.yaml` | `/etc/{name}.yaml`             |

You can also pass your own config type as a `(str) -> Path` function that constructs a path to config from the name.

```python
config = Unit('application-name', lambda name: Path(f"/root/.{name}.yaml"))
```

## 4. Access methods

![](iceberg/4.jpg)

There are 5 most common cases of configuration data access and they are encapsulated into 5 access methods. 

### `.push(value)` to forcefully set an entry

```python
print(f'Greeting was updated to {config("greeting").push("hi")}')
```

### `.pull(value)` to get an entry or default value

```python
print(f'Current greeting is {config("greeting").pull("<none>")}')
```

### `.put(value)` to get the value or set it if it doesn't exist

```python
print(f'{config("greeting").put("Hello")}, world')
```

### `.try_push(value)` to push and know whether something changes

```python
if not config("greeting").try_push(input()):
    print("You input the same greeting. Why are you doing that?")
```

### `.try_put(value)` to put and know whether something changes

```python
if config("greeting").try_put("Hello"):
    print("There was no greeting, so I put hello as one.")
```

## 5. Laziness

![](iceberg/5.jpg)

You can also pass a callable with no arguments as a value and it will be interpreted as a lazy value and be called only if it was used. For example, this hello world program will ask for a greeting only on the first launch:

```python
print(config('greeting').put(input("greeting: ")), "world!")
```