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
  example.com for illustration purposes)
  - An A record for any subdomains i.e `*.example.com` pointing
    to the server's ipv4 address
  - An A record for the root domain e.g. `example.com` pointing to the
    server's ipv4 address
  - If the server has an ipv6 address, add AAAA records equivalent to
    the two above i.e. additional records for `*.example.com` and
    `example.com` pointing to the ipv6 address

- We now need a domain name that will be used as an entry for our MX
  records for each of the domains we're hosting on the server.  Select
  one of the domains above as your primary domain, and add an A record
  (plus AAAA record for ipv6 if you have one) for the subdomain
  `myplatform` pointing to the server's address. So if you selected
  `xxx.yy` as the primary domain , you'll add an A (and AAAA entry)
  for subdomain `myplatform.xxx.yy`. You can name it something other
  than `myplatform` as long as you keep it consistent throughout the
  whole process.
  
- Finally, for each of the domains, add an MX record for its root
  domain e.g `example.com` pointing to the subdomain
  `myplatform.xxx.yyy` created in the step above as the mail server.
  mail server. Generally, this means that the server
  `myplatform.xxx.yy` is responsible for handling mail for the domain
  `example.com`.  Priority can be set to any number, usually 10 by
  default.


## Guiding Principles
- Simplicity is a feature; easy for non-tech persons
  - use root user rather than separate user with sudo and passwd
  - run ansible from within server, removes the need of having to
    install own computer
