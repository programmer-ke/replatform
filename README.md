# replatform

Run your own websites and email accounts. Blog and communicate using
software you control.

This project uses an ansible playbook to install and configure a server
with one or more domains through which you can host websites and
create email accounts.

## Prerequisites

- You have your domain name(s) registered under the domain name
  provider(s) of your choice
- You have root access to a Debian 11 linux server.

## Steps
- Generate your ssh key and copy it to the server
  - It is recommended to add a passphrase to the key
  - Copy with `ssh-copy-id <default_user>@<ip_address>`

- For each domain to host on the server add the following (I'll use
  example.com for example purposes)
  - An A record for any subdomains i.e `*.example.com` pointing
    to the server's ipv4 address
  - An A record for the root domain e.g. `example.com` pointing to the
    server's ipv4 address
  - If the server has an ipv6 address, add AAAA records equivalent to
    the two above i.e. additional records for `*.example.com` and
    `example.com` pointing to the ipv6 address
  - Add an MX record for the root domain `example.com` specifying
    `mail.example.com` as the mail server. Priority can be set to
	any number, usually 10 by default.

- We need to add an entry that will be associated with our reverse DNS
  record. This will also be used as the hostname associated with the
  server. Add an A (and an AAAA for ipv6) record for
  `myplatform.example.com` under one of the domains you'll be hosting
  on the server.
  

## Guiding Principles
- Simplicity is a feature; easy for non-tech persons
  - use root user rather than separate user with sudo and passwd
  - run ansible from within server, removes the need of having to
    install own computer
