# psus

Change the status of a given process (or a group of processes) sending SIGSTOP/SIGCONT.

## Usage

```console
$ psus firefox suspend
Signaled 101 processes

$ psus firefox continue
Signaled 101 processes
```
The script will search for processes with the string in the first command-line argument and execute the action specified in the second command-line argument. The action can be either suspend, or continue.


## Installation
```console
pip install psus
```
