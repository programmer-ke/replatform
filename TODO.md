### Todo

- [ ] Set default timezone to UTC
- [ ] As a site owner, I can configure the send mail flow
  - Ensure SASL is properly configured
    - http://www.postfix.org/SASL_README.html#server_sasl_enable
- [ ] As a site owner, I can appropriately redirect mail meant for postmaster
- [ ] As a site owner, I can successfully set up with ipv6 in addition
- [ ] As a site owner, I can configure milters
- [ ] As a site owner, I can configure sieves
- [ ] As a site owner, I can configure Dynamic address verification with LMTP
    - https://wiki.dovecot.org/HowTo/PostfixDovecotLMTP
 
  to ipv4
- [ ] As a site owner, I am notified of automated upgrades
  - Configure notification email for unattended-upgrades
- [ ] As a site owner, I know how to properly configure rDNS
  - https://serverfault.com/q/24943/980378
  - https://serverfault.com/q/815054/980378

### In Progress

- [ ] As a site owner, I can configure the retrieve mail flow
  - debug logs in /var/log/mail.log
	- Nov  3 09:28:45 myplatform postfix/smtpd[43671]: warning: SASL: Connect to private/auth failed: No such file or directory
      Nov  3 09:28:45 myplatform postfix/smtpd[43671]: fatal: no SASL authentication mechanisms

### Done

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
