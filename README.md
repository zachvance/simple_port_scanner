# Simple Port Scanner
A simple port scanner utility, written in python using sockets and threading.

## Arguments
### Positional
`help [-h]              Show the help menu.`
`scan_type [l, f]       The type of scan; l for 'lisy' or f for 'full'.`
### Optional
`target [-t]            The ip address of the host machine.`
`port [-p]              The port number(s) to scan. Accepts multiple arguments, separated by spaces.`

## Usage
`python main.py [-h] [-t] [-p] [l | f]`

## Todo
- Revisit the usage of numpy; ideally, find another way to split the range list into chunks that uses only the standard
library.
- Explore other options for speeding up scan times aside from threading.