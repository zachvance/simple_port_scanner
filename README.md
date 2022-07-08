# Simple Port Scanner

 [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
 [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A simple port scanner utility, written in python using sockets and threading.

## Background
I was looking for another small project to learn from and try something new. I ended up settling on a port scanner -
as suggested by this projects list - since I'd like to have a better understanding of networking concepts, and I would
have a practical excuse to experiment with the sockets module (which I have not used before).

After skimming through the sockets documentation, and testing out some code based on their examples, I decided that I
need only create a `socket.socket()` instance, and connect to a port `using socket.connect_ex()` and check the result to
determine a successful connection.

This in itself is easily accomplished in 2 or 3 lines of code, but would only allow for a single specified host and
port. My next task would be to expand the functionality to work with a range of addresses, output all of the results,
and take user input.

I started by creating a class, `ScanQuery`, which holds the variables related to the scan and methods for different
scan types.

Everything was going well, until I started providing longer lists of ports to check; every additional port was adding
seconds onto the total scan time. Getting the response of a single connection took around ~3 seconds to complete, and
each port I added to the list to scan would increase the total scan time by ~3 seconds. Obviously, this would be a
problem if I wanted to scan the entire range of ports on a host. So I ended up importing the threading module and
modifying my class methods to create threads for each of the scans, so that they could run concurrently rather than
sequentially. The threading module was also new to me, this being my first time using it, and the first time I had a
situation that warranted using it.

Threading cut down the run times for large lists of ports significantly - scans were now completing in ~3 seconds of
total run time, regardless of the number of connections I was making. Until I tried to scan all the ports on a host.
It started okay, but by the time I reached around port 18000, my machine would choke and freeze up. 65355 threads would
be out of the question, so I decided to split my list range up into chunks. For this, I used numpy's `array_split()`,
which allows you to split a list into equal chunks (referred to as indices or sections in the numpy documentation), and
settled on '5' as being the optimal number of sub lists.

Once I eliminated the choking issue, a full scan of all ports on a single machine could execute in ~90 seconds.
Certainly lots room for improvement, but I am overall happy with my results.


## Arguments
### Positional
```
help [-h]              Show the help menu.  
scan_type [l, f]       The type of scan; l for 'list' or f for 'full'.  
```
### Optional
```
target [-t]            The ip address of the host machine.  
port [-p]              The port number(s) to scan. Accepts multiple arguments, separated by spaces.  
```

## Usage
`python main.py [-h] [-t] [-p] [l | f]`  

## Todo
- Revisit the usage of numpy; ideally, find another way to split the range list into chunks that uses only the standard
library.
- Explore other options for speeding up scan times aside from threading.
- Explore the possibility of more features... packet dissection or OS fingerprinting?
- Add the ability to provide a list of hosts or a subnet range.