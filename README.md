
# name here

A simple to write, extendable configuration language. 

Aims to reduce duplicated configuration.

## Examples

```
# this is a comment

# simple 
default:
    a = "test"
    b = "something"

somename = "something"
somenamespace:
    a = 42
    b = "test"
    c = 3.14159265
    d = [1,2,3]
    e = {"a": "b", "c": "d"} # discouraged but allowed.
    
    # preferred
    f:
        a = "b"
        c = "d"
    
    g = None
    h = False
    i = True
    
    tester:
        extends default
        a = "b"
        
    # hexadecimal also works!
    j = 0x15
    # prefixed zeros don't matter
    k = 0x015
    # even octal works!
    l = 0o123
    # and binary
    m = 0b1010
    # scientific notation
    n = 1e10
    
    # setting keys to values
    o = n # now also 1e10, works through scopes
```

## Extends syntax

The main feature of <name here> is that it supports 'extends' syntax. 
Extends syntax looks like this:
```
extends something
```
An extends block looks through the defined scopes, for a block matching name, 
and copies all it's keys into the block the extend declartion is in. 
Any name defined in the block the extends statement is used, which clashes with a name
from the extended block is overwritten. In the above example, `default` is extended. This means
that this block now contains the `a` and `b`. The `a` key is overwritten.

## Ideas:

* extending from environment variables (1)
* extending from files in the local directory (1)



1: These ideas only make sense when the config file is located in a directory of the filesystem. 
When parsing a config as a string they would obviously fail. Suggestions are welcome.


# implementations

Currently only a [Python](python) implementation is available.

Scheduled are:  
[Rust](rust)  
[Javascript](javascript)
