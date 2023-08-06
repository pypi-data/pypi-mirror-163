# cast-from-env

Get and cast environment variables

## Installation

`python setup.py install`

## Usage

Call `from_env()` with the name of an environment variable, and either a default
value to return if the environment variable is not set, or a type to cast the
environment variable's value to if it is set. If a default value is passed and the
variable is set, its value will be cast to the type of the default value.

Also, if the type of the default value – or the type passed in instead – is `bool`,
`from_env()` will return `True` if the environment variable's string value is any
of `'1'`, `'true'`, `'t'`, `'yes'`, `'y'`, and `'on'`, and `False` otherwise.

## Examples

    from cast_from_env import from_env

    from_env('STRING_VAR', 'default value')  # Value or 'default value' if not set
    from_env('INTEGER_VAR', 100)  # Value cast to int, or 100 if not set
    from_env('INTEGER_VAR', int)  # Value cast to int, or None if not set
    from_env('FLOAT_VAR', 1.0)  # Value cast to float, or 1.0 if not set
    from_env('TRUE_VAR', bool)  # True if value is '1', 'true', 'yes', or 'on'
    from_env('TRUE_VAR', True)  # True if value is '1', 'true', 'yes', 'on', or not set
