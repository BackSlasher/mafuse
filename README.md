# Mafuse
A tool set of scripts to manage afuse mounts using YAML configuration files

## Requirements
`afuse`  
<https://github.com/pcarrier/afuse>  
<http://afuse.sourceforge.net/>  

python 2 (I'm using 2.7)

## How it works
The main script, `init.py`, should be called with a path to the YAML config file.  
`init` then calls `afuse` for each parent directory, and registers the other scripts as callback.  
`handle` is called for every mount / unmount, and is using the same config file.  
`list` is called for directory listing (showing which directories are available), and is using the same config file.

## Improving / Todo
All help is welcome. The things I'm thinking about:
* Using regex / globbing in entries
* Creating upstart / systemd files for user/session tasks (as in running on login)
