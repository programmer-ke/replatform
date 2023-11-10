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

Let's say we want to host two domain names, `example.com` and
`example.org` (there's no limit to the number, we just need one or
more domain names).

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

Depending on the domain host's interface, you may have to add a `.`
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

- Generate an ssh key pair on your local device if you do not already
  have one (passphrase recommended) and copy the public key to the
  server. More info [here][0]
  - Copy it to the server with `ssh-copy-id
    root@myplatform.example.org`
	
  [0]: https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent

- Check that you can ssh into the server without being promted for the
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
  sensitive information. You can even encrypt it if you're a more
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

###### IMAP

SSL/TLS (preferred):

| Setting               | Value                    |
|-----------------------|--------------------------|
| Protocol              | IMAP                     |
| Hostname              | myplatform.example.org   |
| Port                  | 993                      |
| Connection Security   | SSL/TLS                  |
| Authentication Method | Normal Password          |
| Username              | jane.doe@example.org     |

STARTTLS:

| Setting               | Value                    |
|-----------------------|--------------------------|
| Protocol              | IMAP                     |
| Hostname              | myplatform.example.org   |
| Port                  | 143                      |
| Connection Security   | STARTTLS                 |
| Authentication Method | Normal Password          |
| Username              | john.doe@example.org     |

###### POP3

SSL/TLS (preferred):

| Setting               | Value                    |
|-----------------------|--------------------------|
| Protocol              | POP3                     |
| Hostname              | myplatform.example.org   |
| Port                  | 995                      |
| Connection Security   | SSL/TLS                  |
| Authentication Method | Normal Password          |
| Username              | john.doe@example.org     |

STARTTLS:

| Setting               | Value                    |
|-----------------------|--------------------------|
| Protocol              | POP3                     |
| Hostname              | myplatform.example.org   |
| Port                  | 110                      |
| Connection Security   | STARTTLS                 |
| Authentication Method | Normal Password          |
| Username              | jane.doe@example.org     |


##### Outgoing server

SSL/TLS (preferred):

| Setting               | Value                    |
|-----------------------|--------------------------|
| Hostname              | myplatform.example.org   |
| Port                  | 465                      |
| Connection Security   | SSL/TLS                  |
| Authentication Method | Normal Password          |
| Username              | john.doe@example.org     |

STARTTLS:

| Setting               | Value                    |
|-----------------------|--------------------------|
| Hostname              | myplatform.example.org   |
| Port                  | 587                      |
| Connection Security   | STARTTLS                 |
| Authentication Method | Normal Password          |
| Username              | jane.doe@example.org     |


#### Update Website files

- When the playbook completes, you'll be able to point your browser to
  each of the web domains configured and you'll see a placeholder web
  page.  If you check in the server at the location `/var/www` you'll
  see a directory for each domain, and a file named `index.html` in
  each of these directories. This is the placeholder that is created
  as the landing page for each domain. To publish your
  websites, upload the collection of files that make up your websites
  into these locations.  The only requirement is that there should be
  a page named `index.html` that serves as the landing page.

tutorial: https://easyhtmlcss.com/

### Maintenance

### 
  

## Overview of how it works

### Recieving mail into inbox

The number in brackets indicates the port process is listening on

Outside Network -> smptd(25) -> Postfix Queue -> Dovecot lmtp (via
unix pipe) -> Virtual boxes or User boxes

### Retrieving mail by mail client

Email client -> dovecot-imapd(143) -> Virtual or system user mailbox

Email client -> dovecot-pop3d(110) -> Virtual or system user mailbox

### Submitting outgoing mail to server from mail client

Email client -> smtpd(465) (implicit tls) -> postfix queue -> smtp client -> destination network

Email client -> smtpd(587) (starttls) -> postfix queue -> smtp client -> destination network

## Guiding Principles
- Simplicity is a feature; easy for non-tech persons
  - use root user rather than separate user with sudo and passwd
  - run ansible from within server, removes the need of having to
    install own computer
  - use only packages maintained by debian stable

## Resources
- SSL
  - https://github.com/drwetter/testssl.sh
  - https://www.immuniweb.com

- Testing
  - http://www.jetmore.org/john/code/swaks/
  - https://spamassassin.apache.org/gtube/
