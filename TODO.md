### Todo
- [ ] As a web user, I can only access https versions of websites for
  each domains listed
  - https://www.howtoforge.com/tutorial/install-letsencrypt-and-secure-nginx-in-debian-9/
  - https://github.com/geerlingguy/ansible-role-certbot
- [ ] As a site owner, I can install email server packages
- [ ] As a site owner, I can successfully set up with ipv6 in addition
  to ipv4
- [ ] As a site owner, I am notified of automated upgrades
  - Configure notification email for unattended-upgrades
- [ ] As a site owner, I know how to properly configure rDNS
  - https://serverfault.com/q/24943/980378
  - https://serverfault.com/q/815054/980378

### In Progress

- [ ] As a web user, I can access http only versions of websites
  for each listed domain
  - install nginx
  - remove default site
  - For each listed domain:
    - create site config
	- enable site

### Done

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
