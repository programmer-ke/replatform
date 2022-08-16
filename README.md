# replatform

Run your own websites and email accounts. Blog and communicate using
software you control.

This project uses an ansible playbook to install and configure a server
with one or more domains through which you can host websites and
create email accounts.

## Prerequisites

- You have your domain name(s) registered under the domain name
  provider of your choice
- You have root access to a Debian 11 linux server.

## Steps
- Generate your ssh key and copy it to the server
  - Recommended to add a passphrase to key
  - Copy with `ssh-copy-id <default_user>@<ip_address>`
- 

## Guiding Principles
- Simplicity is a feature so that it is easy for non-tech people
  - use root user rather than separate user with sudo and passwd
  - run ansible from within server, removes the need of having to
    install own computer

