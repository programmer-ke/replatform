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

### DNS Setup
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
  Generally, this means that the server `myplatform.xxx.yy` is
  responsible for handling mail for the domain `example.com`.
  Priority can be set to any number, usually 10 by default.

# Configure the server

- Generate the ssh key on your local device and copy it to the server
  - It is recommended to add a passphrase to the key
  - Copy with `ssh-copy-id root@<ip_address>`

- Check that you can ssh into the server without being promted for the
  password using `ssh root@<ip_address>`.

- Make sure the server is up-to-date by running the following commands
  - `apt update`
  - `apt full-upgrade`

- Reboot the server and then SSH back in again to make sure you are
  modifying the server from a clean slate. Type in `reboot` and after
  a few seconds, ssh back in.

- Install `git` and `ansible` packages with the following command
  - `apt get install git ansible`

- Clone this repo and cd into it

- Run the following ansible command to setup the server
  `ansible-playbook site.yml`. The first time you run this, it will
  place a variables file in the following location on the server:
  `/root/private_vars/vars.yml` and exit

- Edit this file with the correct variables such as the server hostname
  (The value you set for `myplatform.xxx.yyy` above), the external ipv4 address,
  ipv6 address if you have one, the domains you want to host, etc.
  Due to the sensitive nature of this file, you can encrypt it with
  the `ansible-vault` command.

- Run the playbook command again to continue with setting up.
  `ansible-playbook site.yml` If you encrypted the file above, add the
  option `--ask-vault-pass` and enter the encryption password when
  prompted.

## Guiding Principles
- Simplicity is a feature; easy for non-tech persons
  - use root user rather than separate user with sudo and passwd
  - run ansible from within server, removes the need of having to
    install own computer
