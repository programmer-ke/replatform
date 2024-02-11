# replatform

Run your own websites and email accounts using a platform you control.

This project allows anyone with basic unix command-line skills to
quickly setup and easily maintain websites and email accounts on
Debian Linux.

It uses an [ansible][10] playbook to install and configure a server
with one or more domains on which you can host websites and any number
of email accounts.

All packages used are installed from Debian repositories. This makes
it much easier to stay up to date and secure, and reduces the work
needed to migrate to newer versions of Debian.

[10]: https://docs.ansible.com/ansible/latest/getting_started/index.html

## Features

- Supports multiple domains for email accounts and websites on one server
- Just one command to setup the entire system: `ansible-playbook site.yml`
- Critical security updates automatically installed once the server is up and running
- DKIM, SPF, DMARC configured reducing the probability of sent mail being marked as spam
- Automated, free TLS certificate via [Let's Encrypt][7] to secure your websites and emails
- Out of the box server side web analytics via [goaccess][9]

[7]: https://letsencrypt.org/
[9]: https://goaccess.io/

## Prerequisites

- You have your domain name(s) registered under the domain name
  provider(s) of your choice
- You have root access to a Debian 11 linux server (see bottom of page
  for a good deal)

## Steps

### DNS Setup

Let's say we want to host two domain names, `example.com` and
`example.org`.

1) Server Hostname

We'll first set up a subdomain on one of the domain names as our
server hostname.

For this example we'll use `example.org`. Add the following records to
`example.org` to map the subdomain to the public ipv4 and ipv6
(optional) addresses associated with the server.

| name                   | type | value                    | ttl  | remarks                |
|------------------------|------|--------------------------|------|-------------------------|
| myplatform.example.org | A    | 192.168.3.3              | 3600 | ipv4 address            |
| myplatform.example.org | AAAA | fe80::1ff:fe23:4567:890a | 3600 | ipv6 address (optional) |

You can use any name in the place of `myplatform`, but keep it
consistent throughout the process below. The TTL value can be any
reasonable number, the DNS provider may pre-fill it for you.

Depending on the domain host's interface, you may need to add a `.`
(dot) character after the name in the domain record.

If you're not sure how to add any of the records, just search online
how to add the type of record (A, AAAA, MX etc..) on your dns provider,
they probably have a tutorial of that somewhere.

2) Domain and subdomain mappings

We then add the following records for `example.org`:

| name          | type | value                    | ttl  | remarks                                        |
|---------------|------|--------------------------|------|-------------------------------------------------|
| *.example.org | A    | 192.168.3.3              | 3600 | Map all subdomains to the server's ipv4 address |
| *.example.org | AAAA | fe80::1ff:fe23:4567:890a | 3600 | Map all subdomains to the server's ipv6 address |
| example.org   | A    | 192.168.3.3              | 3600 | Map root domain to server's ipv4 address        |
| example.org   | AAAA | fe80::1ff:fe23:4567:890a | 3600 | Map root domain to server's ipv6 address        |

and the same for `example.com`:

| name          | type | value                    | ttl  | remarks                                        |
|---------------|------|--------------------------|------|-------------------------------------------------|
| *.example.com | A    | 192.168.3.3              | 3600 | Map all subdomains to the server's ipv4 address |
| *.example.com | AAAA | fe80::1ff:fe23:4567:890a | 3600 | Map all subdomains to the server's ipv6 address |
| example.com   | A    | 192.168.3.3              | 3600 | Map root domain to server's ipv4 address        |
| example.com   | AAAA | fe80::1ff:fe23:4567:890a | 3600 | Map root domain to server's ipv6 address        |

3) Mail Exchange Records

Now we need to designate the server hostname set in step 1 above as
the mail server for each of the domains. So for `example.org` we
add the following:

| name        | type | value                  | priority | ttl  | remarks                                                               |
|-------------|------|------------------------|----------|------|------------------------------------------------------------------------|
| example.org | MX   | myplatform.example.org | 10       | 3600 | Priority can be any value, since we're only specifying one mail server |

and the same for `example.com`. Note that the value is the same in both:

| name        | type | value                  | priority | ttl  | remarks                                                               |
|-------------|------|------------------------|----------|------|------------------------------------------------------------------------|
| example.com | MX   | myplatform.example.org | 10       | 3600 | Priority can be any value, since we're only specifying one mail server |

### Configure the server

- It is generally recommended to use an SSH key to log into the server
  instead of a password.  The first step will therefore be setting up
  an SSH key.
  If you are in a situation where you cannot set up one
  e.g. when using a shared computer, skip this step and after cloning
  this repo below, edit [ssh.yml](ssh.yml) and set both
  `PasswordAuthentication` and `ChallengeResponseAuthentication` to
  `yes` instead of `no`. Otherwise, password-based authentication will be disabled
  and without an SSH key, you'll be locked out of the server.

  - Generate an ssh key pair on your local device if you do not already
	have one (passphrase recommended) and copy the public key to the
	server. More info [here][0].

  - Copy it to the server with `ssh-copy-id root@myplatform.example.org`

	[0]: https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent

  - Check that you can ssh into the server without being prompted for the
	password using `ssh root@myplatform.example.org`.

- Make sure the server is up-to-date by running the following commands
  - `apt update`
  - `apt full-upgrade`

- Reboot the server and then SSH back in again after a few seconds to make sure you are
  modifying the server from a clean slate.
  - `reboot`

- Install `git` and `ansible` packages with the following command
  - `apt install git ansible`

- Clone this repo and navigate into it like so
  - `git clone https://github.com/programmer-ke/replatform.git`
  - `cd replatform`

- Run the following ansible command to setup the server
  `ansible-playbook site.yml`. The first time you run this, it will
  place a variables file in the following location on the server:
  `/root/private_vars/vars.yml` and exit

- Edit this file with the correct variables such as the server
  hostname (The value you set for `myplatform.example.org` above), the
  external ipv4 address, ipv6 address if you have one, the domains you
  want to host, etc. Be careful not to share this file as it has
  secrets such as passwords. You can even encrypt it if you're a more
  advanced user of ansible. Read about that [here][1]
  
  If you are unsure how to edit the file, use the [nano][2] editor that
  is already installed with debian.

  [1]: https://docs.ansible.com/ansible/latest/user_guide/vault.html
  [2]: https://linuxize.com/post/how-to-use-nano-text-editor/

- Run the playbook command again in the `replatform` directory to
  proceed with set up. If you have a fast internet connection from
  your server it should only take a few minutes to complete.

  - `ansible-playbook site.yml`

  If you encrypted the file above, add the
  option `--ask-vault-pass` and enter the encryption password when
  prompted.

### Final Steps after Server configuration

Now that server configuration is complete, we need to configure
additional domain settings with server generated values, and set up
email client software to start receiving email.

#### Configure DNS TXT records

The configuration process generated some information that we need to
add as TXT records to the configured domains.

These will be useful for validating your email messages to other mail
servers and reduce the probability of being marked as spam.

Move into the directory they have been placed in:

`cd /root/dns_txt_records`

Each file name begins with the associated domain. There are 3 types
for each domain in the following pattern:

- `example.org_dkim.txt` for the DKIM TXT record
- `example.org_dmarc.txt` for the DMARC TXT record
- `example.org_spf.txt` for the SPF TXT record.

We'll add the content of each file as a TXT record on the relevant
domain. Each file has a single line that starts with the hostname,
followed by space, then the rest of the line as the value for the TXT
record.

We add them as follows for each type of TXT record

| Type  | hostname                       | value                                                      |
|-------|--------------------------------|------------------------------------------------------------|
| DKIM  | default._domainkey.example.org | v=DKIM1;h=sha256;k=rsa;p=MIIBIjANB...DAQAB                 |
| SPF   | example.org                    | v=spf1 mx a:myplatform.example.org -all                    |
| DMARC | _dmarc.dataengineering.co.ke   | v=DMARC1; p=quarantine; rua=mailto:..; ruf=mailto:..; fo=1 |

In some cases, the service provider may pre-fill the domain name 
for you, so only input the prefix for the hostname value e.g.

`default._domainkey` for `default._domainkey.example.org`

Set the 3 TXT records for each of the configured domains.

#### Configure Reverse DNS

As part of email authentication, some receiving systems will check
whether the ip address resolves back to the mail server hostname i.e.
`myplatform.example.org` in our example.

How this is set up varies by the server host, for example you could be
required to name your server with the appropriate hostname
(e.g. `myplatform.example.org`) and the record will be set up
automatically. Other hosts may require you to reach out to support to
have it manually configured.

The requirement here is that the reverse dns lookup on the ipv4 (and
optionally ipv6) address will resolve back the the value set as server
hostname above.

This further reduces the probability of your email messages being
marked as spam.

#### Configure mail clients

Mail clients will need an incoming server configuration for receiving
email and an outging server configuration for sending email.

Below, we'll list configuration as required by [thunderbird][3], but should
be similar on most email clients.

[3]: https://www.thunderbird.net

##### Incoming server

There are two options for incoming mail:
- IMAP
   - Mail will be stored on the server and accessible via different
     devices / mail clients with the correct credentials
- POP3:
   - Mail will be downloaded to the client and deleted from the
     server.  Received email will be viewable only on the device /
     client that downloads the email.

Read more about SSL/TLS vs STARTTLS [here][4]

[4]: https://www.mimecast.com/blog/ssl-vs-tls-vs-starttls-encryption/

The hostname value below is the same throughout as it is the 
mail server hostname as `myplatform.example.org` set above.

###### IMAP

SSL/TLS (preferred):

| Setting               | Value                    |
|-----------------------|--------------------------|
| Protocol              | IMAP                     |
| Hostname              | myplatform.example.org   |
| Port                  | 993                      |
| Connection Security   | SSL/TLS                  |
| Authentication Method | Normal Password          |
| Username              | jane.doe@example.com     |

STARTTLS:

| Setting               | Value                    |
|-----------------------|--------------------------|
| Protocol              | IMAP                     |
| Hostname              | myplatform.example.org   |
| Port                  | 143                      |
| Connection Security   | STARTTLS                 |
| Authentication Method | Normal Password          |
| Username              | john.doe@example.com     |

###### POP3

SSL/TLS (preferred):

| Setting               | Value                    |
|-----------------------|--------------------------|
| Protocol              | POP3                     |
| Hostname              | myplatform.example.org   |
| Port                  | 995                      |
| Connection Security   | SSL/TLS                  |
| Authentication Method | Normal Password          |
| Username              | john.doe@example.com     |

STARTTLS:

| Setting               | Value                    |
|-----------------------|--------------------------|
| Protocol              | POP3                     |
| Hostname              | myplatform.example.org   |
| Port                  | 110                      |
| Connection Security   | STARTTLS                 |
| Authentication Method | Normal Password          |
| Username              | jane.doe@example.com     |

To receive administrative email sent to the admin user, set the
username on the email client as `admin@<server hostname>` e.g.
`admin@myplatform.example.org`, and password will the whatever was
specified in `/root/private_vars/vars.yml`.

##### Outgoing server

SSL/TLS (preferred):

| Setting               | Value                    |
|-----------------------|--------------------------|
| Hostname              | myplatform.example.org   |
| Port                  | 465                      |
| Connection Security   | SSL/TLS                  |
| Authentication Method | Normal Password          |
| Username              | john.doe@example.com     |

STARTTLS:

| Setting               | Value                    |
|-----------------------|--------------------------|
| Hostname              | myplatform.example.org   |
| Port                  | 587                      |
| Connection Security   | STARTTLS                 |
| Authentication Method | Normal Password          |
| Username              | jane.doe@example.com     |

At this point, to check that email is well set up, you can send an
email to `check-auth@verifier.port25.com` from any of the hosted mail
accounts (i.e. not including `admin@<server_hostname>`). This is an
automated service that will reply with results showing that DKIM, SPF
and RDNS are well set up.

For more troubleshooting if your outgoing mail is consistently being
marked as spam, use https://mxtoolbox.com/. IP address reputation
issues is a common problem.

#### Updating Website files

After the playbook completes, when you point your browser to
each of the web domains configured and you'll see a placeholder web
page.

If you check in the server at the location `/var/www` you'll
see a directory for each domain, and a file named `index.html` in
each of these directories. This is the placeholder that is created
as the landing page for each domain.

To publish your websites, upload the collection of files that make up
your websites into these directories.  The only requirement is that
there should be a page named `index.html` that will be the landing
page.

A basic tutorial that can get you started on HTML/CSS can be found
[here][5].

[5]: https://easyhtmlcss.com/

The `scp` or `rsync` commands can be used to transfer files to the
server via SSH.

#### Web analytics

Web analytics that will be regerated every few minutes can be accessed
on the browser at the server's hostname at `/report.html`
e.g. `myplatform.example.org/report.html`

These are generated from the web server's logs, so you can get some
analytics without having visitors download JavaScript trackers.

#### Email files in the server

The email folders for each user are stored under

`/home/vmail/<domain>/<username>/Maildir`.

This may be useful if you want to backup emails to an external
location.

#### Maintenance

By default, the system is set up to automatically install critical
security updates released by the debian team and reboot if necessary.
An email notification will be sent to the `admin@<server hostname>`
email address whenever this happens.

Spam detection rules will also be updated on a daily basis by
spamassasin.

Every time the setup command `ansible-playbook site.yml`, is run like
we did above, all new updates will be installed and you will be
prompted to reboot if necessary.


## High level technical overview

### Recieving mail into inbox

The number(s) in brackets indicates the port(s) the process is listening on.

Outside Network -> smptd(25) -> Postfix Queue -> Dovecot lmtp (via
unix pipe) -> Virtual boxes or User boxes

### Retrieving mail by mail client

Email client -> dovecot-imapd(993 & 143) -> Virtual or system user mailbox

Email client -> dovecot-pop3d(995 & 110) -> Virtual or system user mailbox

### Submitting outgoing mail to server from mail client

Email client -> smtpd(465) (ssl/tls) -> postfix queue -> smtp client -> destination network

Email client -> smtpd(587) (starttls) -> postfix queue -> smtp client -> destination network

## Technical considerations
- While more experienced users may frown on this, we directly use the
  root user to setup everything. Goal is to reduce friction as much as
  possible for non-technical users.
- For the same reason above, we run ansible directly on the server
  instead of the typical use-case of using a different machine as
  the control node.
- All packages are from the default Debian repositories. This makes it
  much easier to stay up to date by relying on the great Debian folks
  for updates. Consider [donating][6] to Debian if you appreciate
  their work.

[6]: https://www.debian.org/donations

## Testing Resources
- SSL
  - https://github.com/drwetter/testssl.sh
  - https://www.immuniweb.com

- Email
  - http://www.jetmore.org/john/code/swaks/
  - https://spamassassin.apache.org/gtube/
  - https://mxtoolbox.com/

## Credits

Inspired by the following projects:

- Luke Smith's emailwiz: https://github.com/LukeSmithxyz/emailwiz
- Landchad: https://landchad.net/
- Sovereign: https://github.com/sovereign/sovereign

## Looking For Affordable Servers?

Checkout the following offers from Racknerd:

- 1GB at [$10.99/year][11]
- 1.5 GB at [$16.88/year][12]
- 2.5 GB at [$23.88/year][13]

[11]: https://my.racknerd.com/aff.php?aff=9677&pid=838
[12]: https://my.racknerd.com/aff.php?aff=9677&pid=839
[13]: https://my.racknerd.com/aff.php?aff=9677&pid=840

