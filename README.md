# replatform

Run your own websites and email accounts. Blog and communicate using
software you control.

This project uses an ansible playbook to install and configure a server
with one or more domains through which you can host websites and
create email accounts.

# Prerequisites

- You have your domain name(s) registered under the domain name
  provider of your choice
- You have root access to a Debian 11 linux server.

# Decisions
- Simplicity is a feature
  - use root user rather than separate user with sudo and passwd
  - run ansible from within server (helpful for ansible beginners)


