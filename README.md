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

- The first step would be to configure the server hostname. An easy
  way is to select one of the domains you want to host on the server
  and designate a subdomain as the server's hostname. Say you select
  `xxx.yy`, designate the subdomain `myplatform.xxx.yy` as your
  server's hostname.  Create an A record for the subdomain pointing to
  ipv4 address of the server.  If your server also has an ipv6
  address, create an AAAA record for the subdomain pointing to the
  ipv6 address. You can use any domain/subdomain here just ensure that
  the server hostname is consistent throughout the process below

- Next, for each of the domains to host on the server add the
  following (I'll use example.com for illustration purposes)
  - An A wildcard record for its subdomains i.e `*.example.com`
    pointing to the server's ipv4 address
  - An A record for the root domain e.g. `example.com` pointing to the
    server's ipv4 address
  - If the server has an ipv6 address, add AAAA records equivalent to
    the two above i.e. additional records for `*.example.com` and
    `example.com` pointing to the ipv6 address
  - Add an MX record for its root domain i.e. `example.com` pointing
	to the subdomain `myplatform.xxx.yyy` created in the first step
	above as the mail server.  What this means that the server
	`myplatform.xxx.yy` is responsible for handling mail for the
	domain `example.com`.  Priority can be set to any number, usually
	10 by default. Since we're only specifying a single mail server,
	priority doesnt matter.

### Configure the server

- Generate an ssh key pair on your local device if you do not already
  have one (passphrase recommended) and copy the public key to the
  server
  - Copy it to the server with `ssh-copy-id
    root@<server_hostname>`

- Check that you can ssh into the server without being promted for the
  password using `ssh root@<server_hostname>`.

- Make sure the server is up-to-date by running the following commands
  - `apt update`
  - `apt full-upgrade`

- Reboot the server and then SSH back in again to make sure you are
  modifying the server from a clean slate. Type in `reboot` and after
  a few seconds, ssh back in.

- Install `git` and `ansible` packages with the following command
  - `apt get install git ansible`

- Clone this repo and move into it like so
  - `git clone https://github.com/.../replatform.git`
  - `cd replatform`

- Run the following ansible command to setup the server
  `ansible-playbook site.yml`. The first time you run this, it will
  place a variables file in the following location on the server:
  `/root/private_vars/vars.yml` and exit

- Edit this file with the correct variables such as the server
  hostname (The value you set as `myplatform.xxx.yyy` above), the
  external ipv4 address, ipv6 address if you have one, the domains you
  want to host, etc. Be careful not to share this file as it has
  sensitive information. You can even encrypt it if you're a more
  advanced user of ansible. Read about it
  [here][1]

  [1]: https://docs.ansible.com/ansible/latest/user_guide/vault.html

- Run the playbook command again to continue with setting up.
  `ansible-playbook site.yml` If you encrypted the file above, add the
  option `--ask-vault-pass` and enter the encryption password when
  prompted.

- When the playbook completes, you'll be able to point your browser to
  each of the web domains configured and you'll see a placeholder web
  page.  If you check in the server at the location `/var/www` you'll
  see a directory for each domain, and a file named `index.html` in
  each of these directories. This is the placeholder that is created
  to server as the landing page for your domain. To publish your
  websites, upload the collection of pages that make up your websites
  into these locations.  The only requirement is that there should be
  a page named `index.html` that serves as the landing page

## Guiding Principles
- Simplicity is a feature; easy for non-tech persons
  - use root user rather than separate user with sudo and passwd
  - run ansible from within server, removes the need of having to
    install own computer
