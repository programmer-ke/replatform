### Todo

- [ ] Allow only necessary ports via ufw
- [ ] investigate ssl cert expiry
- [ ] Add mail-tester.com to docs
- [ ] Migrate to Debian 12 (Bookworm)
- [ ] Add fail2ban to stop brute force attacks

### In Progress



### Done

- [x] Fix mail server reload after cert update
  - Add to certbot post hook
	- systemctl reload postfix
	- systemctl reload dovecot
	- [PR](https://github.com/programmer-ke/replatform/pull/2)
- [x] customize goaccess for less crawler spam
  - https://2bits.com/apache/identifying-aggressive-crawlers-using-goaccess.html
  - https://www.thedroneely.com/posts/tweaking-goaccess-for-analytics/
  - https://github.com/Stevie-Ray/referrer-spam-blocker
	- can revisit this with more traffic.
- [x] Research server side web analytics e.g. goaccess
- [x] do not generate server hostname prefixed txt records
- [x] As a site owner, I can successfully set up with ipv6 in addition
  to ipv4
  - test possible on DO
- [x] Debug spamassassin
	- plugin: eval failed: bayes: (in learn) locker: safe_lock: cannot create tmp lockfile /var/lib/spamassassin/.spamassassin/bayes.lock.myplatform.dataengineering.co.ke.859 for /var/lib/spamassassin/.spamassassin/bayes.lock: Permission denied
    - https://stackoverflow.com/q/42707466/1382495
- [x] Set up spf, dkim, dmarc and test
- [x] Debug mail sending issue: relay access denied
  - Caused by incorrect configured port in mail client
- [x] As a site owner, I can setup dmarc
  - format: v=DMARC1; p=reject; rua=mailto:dmarc@somedomain.com; fo=1
  - explanation (chatgpt)
    - "v=DMARC1" indicates the version of DMARC being used.
    - "p=reject" specifies the DMARC policy for how to handle messages
      that fail DMARC checks. In this case, it is set to "reject",
      which means that any message that fails DMARC checks should be
      rejected (i.e., not delivered to the recipient).
    - "rua=mailto:dmarc@somedomain.com" specifies the email address to
      which aggregate DMARC reports should be sent. These reports
      provide information on how DMARC is being used for a particular
      domain.
    - "fo=1" specifies the DMARC "failure reporting option". In this
      case, it is set to "1", which means that only the "header from"
      domain should be used to evaluate DMARC alignment (i.e., the
      domain in the "From" header of the email). <- this sounds wrong

  - dkim, spf, dmarc guide: https://dmarcly.com/blog/how-to-implement-dmarc-dkim-spf-to-stop-email-spoofing-phishing-the-definitive-guide

- [x] As a site owner, I can setup spf
  - generate format like: v=spf1 mx a:mail.somedomain.com -all
    - explanation(chatgpt): 
		- "v=spf1": This specifies the version of SPF being used,
          which is SPF version 1.
		- "mx": This allows the domain's MX records to be used to
          identify authorized IP addresses. If the domain's MX records
          resolve to an IP address, that IP address is authorized to
          send email for the domain.
        - "a:mail.somedomain.com": This specifies that the IP address
          associated with the "mail.somedomain.com" subdomain is
          authorized to send email for the domain. This is usually
          used when the domain's MX records point to a subdomain,
          rather than the root domain.
        - "-all": This specifies a strict policy that instructs email
          receivers to reject any email that does not come from an
          authorized IP address. The "-" indicates a hard fail, which
          means that any email that fails SPF checks should be treated
          as suspicious or illegitimate
- [x] As a site owner, I can set up dkim txt records
  - extract from generated (bind-compatible) txt record into form
    of key and value that can be set up in on dns
  - http://www.opendkim.org/opendkim-README (see large keys section)
  - need to extract section between parentheses, merge into one line and remove double quotes
    - commands that work:
	  - sed -n '/".*"/{s/^[^(]*(//;s/)[^"]*$//;p}' sample 
	  - awk -F'"' '/"/{print $2}' sample
	  - grep -Pzo '(?s)\(\s+(.+)\s+\)' sample

- [x] As a site owner, I know how to properly configure rDNS
  - https://serverfault.com/q/24943/980378
  - https://serverfault.com/q/815054/980378
    - contact host to change rdns query to resolve to hostname
	- Ensure that the following match
      - hostname
	  - rdns
      - mx record (for hosted domains)
  	  - HELO/EHLO
      - SMTP greeting banner
- [x] As a site owner, I can configure Dynamic address verification with LMTP
    - https://wiki.dovecot.org/HowTo/PostfixDovecotLMTP
- [x] Backscatter: http://www.postfix.org/BACKSCATTER_README.html
  - not an issue at the moment
- [x] spam https://serverfault.com/a/540614
- [x] Fix spoofing mail as authenticated user
  swaks --from spoofedsender@domain --to recipient@domain --auth PLAIN --auth-user authenticateduser@domain --auth-password authenticatedpasswd --server smtp.domain.tld --tls
- [x] IP address leakage issue: https://serverfault.com/questions/413533/remove-hide-client-sender-ip-from-postfix/998993#998993
  - install postfix-pcre
  - specify new cleanup service name for submission daemons
  - declare new cleanup service in master.cf with the new name
    - pass new header check option with replacing regex
- [x] Set default timezone to UTC
  - ansible module: https://docs.ansible.com/ansible/latest/collections/community/general/timezone_module.html
  - services to restart: https://serverfault.com/q/322852/980378
- [x] (discarded) Check cert expiry
- [x] (Discarded) Move data files to single directory hierarchy (for ease of migration)
- [x] As a site owner, I am notified of automated upgrades
  - Configure notification email for unattended-upgrades
- [x] As a site owner, I can appropriately redirect mail meant for postmaster
- [x] As site owner, I can configure admin mail password
- [x] Fix issue with fs layout (send folder not found)
  - Need to manually mv e.g. .Sent to Sent, for existing accounts
- [x] Figure out password encryption in for virtual users
  - how does it work with system users in ansible?
    - one can provided a hashed password. 
- [x] As a site owner, I can configure dovecot sieves
  - https://doc.dovecot.org/configuration_manual/sieve/configuration/
   - consider task on single directory hierarchy as prerequisite
   - does the milter mark email headers, or simply rejects spam?
     - depends on setting -r nn. See /etc/default/spamass-filter
       - see: https://mailtrap.io/blog/spamassassin-score/
       - see man spamassassin
   - plan:
     - [x] modify mail directory structure
       - see: https://doc.dovecot.org/admin_manual/mailbox_formats/maildir/#directory-structure
     - [x] allow lowly scored message through
	   - swaks --to info@somedomain.com --body=~/Desktop/spam-tests/spamtext.txt
     - [x] add relevant dovecot sieve to redirect spam to 'junk' folder
- [x] As a site owner, I can configure the opendkim milter
  - https://serverfault.com/questions/296492/how-do-i-use-opendkim-with-multiple-domain-names-on-a-single-server
  - https://web.archive.org/web/20100924174500/http://stevejenkins.com/blog/2010/09/how-to-get-dkim-domainkeys-identified-mail-working-on-centos-5-5-and-postfix-using-opendkim
  - https://wiki.debian.org/opendkim
	- configure post key generation

- [x] (discarded) As a site owner, I can configure the clamav milter
  - https://lelutin.ca/posts/installing_postfix_-_clamav_-_spamassassin_-_dovecot_-_postfixadmin_on_debian_squeeze/
    - test virus pre and post deployment, verify behaviour
	- abort clamav because of memory usage (=~ 800MB)
- https://betatim.github.io/posts/clamav-memory-usage

- [x] As a site owner, I can configure the spamassasin milter
  - https://lelutin.ca/posts/installing_postfix_-_clamav_-_spamassassin_-_dovecot_-_postfixadmin_on_debian_squeeze/

- [x] As a site owner, I can configure the send mail flow
  - Ensure SASL is properly configured
    - http://www.postfix.org/SASL_README.html#server_sasl_enable
  - enable submission (for starttls) and smtps (for implicit tls)
	- see emailwiz
    - see: https://serverfault.com/q/605715/980378

- [x] As a site owner, I have correctly configured SSL for mail
    - clients e.g. thunderbird should not ask for SSL exceptions
	- configure postfix and dovecot with letsencrypt cert
    - Set recommended SSL params
	  - https://ssl-config.mozilla.org/
- [x] As a site owner, I can configure the retrieve mail flow
- [x] As a site owner, I can configure the receipt mail flow
  - https://wiki.dovecot.org/HowTo/SimpleVirtualInstall
  - mail now successfully lands into user mailboxes for both system and virtual users
- [x] Research on how to took up all the mail packages together
  - https://www.postfix.org/BASIC_CONFIGURATION_README.html#syntax
  - http://www.postfix.org/VIRTUAL_README.html
  - https://gist.github.com/Anime4000/59ade3017f1e743069f4e8c6dc032681
  - https://scaron.info/blog/debian-mail-postfix-dovecot.html
  - https://doc.dovecot.org/configuration_manual/howto/postfix_and_dovecot_sasl/
  - https://wiki.debian.org/Postfix
  - http://www.postfix.org/OVERVIEW.html
  - https://wiki.dovecot.org/LDA/Postfix
  - https://serverfault.com/questions/605715/postfix-smtps-and-submission-confusion
  - https://old.reddit.com/r/debian/comments/gcmo5r/looking_for_complete_debian_mail_server_tutorial/
  - https://www.postfix.org/MILTER_README.html
  - figure out spamassassin milter vs rspamd vs ..
    - https://lelutin.ca/posts/installing_postfix_-_clamav_-_spamassassin_-_dovecot_-_postfixadmin_on_debian_squeeze/
- [x] As a site owner, I can install email server packages
- [x] As a site owner, I can find all the info on the README I need to set up websites
- [x] As a web user, I can only access https versions of websites for
  each domains listed
  - use standalone certonly
	- https://eff-certbot.readthedocs.io/en/stable/using.html#standalone
  - Add documentation link to: https://letsencrypt.org/docs/rate-limits/
  - Detection of changes: https://stackoverflow.com/q/65238096
  - https://www.howtoforge.com/tutorial/install-letsencrypt-and-secure-nginx-in-debian-9/
  - https://github.com/geerlingguy/ansible-role-certbot
  - steps:
    - create pre/post hooks
	- create cert
    - add renewal cron job
	- Add nginx ssl configs/redirections
      - recommended by certbot: https://ssl-config.mozilla.org/#server=nginx&version=1.18.0&config=intermediate&openssl=1.1.1n&guideline=5.6
	  - https://security.stackexchange.com/questions/149811/why-is-mozilla-recommending-predefined-dhe-groups
	  - https://eff-certbot.readthedocs.io/en/stable/ciphers.html#introduction
	  - https://nginx.org/en/docs/http/configuring_https_servers.html
- [x] As a web user, I can access http only versions of websites
  for each listed domain
  - install nginx
  - remove default site
  - For each listed domain:
    - create site config
	- enable site
- [x] As a site owner, I can specify private variables that live outside the repo
  for sensitive variable that should not be shared
  - On the first ansible run, copy this to `/root/private_vars/vars.yml`
- [x] As a site owner, I should be able to restart networking after
  hostname changes before running subsequent tasks
- [x] As a site owner, I can lock down SSH access
- [x] As a site owner, I can perform a full upgrade every time I run
  the playbook
  - https://www.jeffgeerling.com/blog/2022/ansible-playbook-upgrade-ubuntudebian-servers-and-reboot-if-needed
  - Do a full upgrade as first task in playbook
  - Ask user to reboot if necessary at the end of the playbook
- [x] As a site owner, I can enable automated security updates
- [x] As a site owner, I can update the system packages with each run
- [x] As a site owner, I can explicitly set the hostname
  - https://wiki.archlinux.org/title/Network_configuration#Set_the_hostname
  - https://wiki.debian.org/Hostname
- [x] As a site owner, I can find instructions for DNS setup
- [x] As site owner, you can ssh run
  `ansible myplatform -u <default_user> -a "hostname"`
  to execute the `hostname` command within the server.
