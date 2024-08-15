# ODOO Installation Guide

## 1. Environment Information

| OS           | Linux Ubuntu |
|--------------|--------------|

## 2. Installation Guide

### 2.1 Update the System

```bash
sudo apt update

sudo apt upgrade
```
### 2.2 Install Packages
```bash
sudo apt install -y python3-pip

sudo apt install build-essential wget git python3.11-dev python3.11-venv \
libfreetype-dev libxml2-dev libzip-dev libsasl2-dev \
node-less libjpeg-dev zlib1g-dev libpq-dev \
libxslt1-dev libldap2-dev libtiff5-dev libopenjp2-7-dev libcap-dev
```
### 2.3 Create System User
System User	Username	User's Home	Group
Odoo    	odoo   	/opt/odoo	odoo

```bash
sudo /usr/sbin/adduser --system --shell /bin/bash --gecos 'odoo' --group --home /opt/odoo odoo
```
### 2.4 Install PostgreSQL
```bash
sudo apt install postgresql
```
Username	Password
Odoo   	odoo
```bash
sudo su - postgres

createuser -S -d -R -P odoo

exit
```
### 2.5 Install wkhtmltopdf
```bash
sudo apt install wkhtmltopdf
```
### 2.6 Clone Odoo Repository
If there is a good network and cloning is possible, use section 2.6.1. If network issues or other factors cause cloning errors, use section 2.6.2.

#### 2.6.1 Clone Remote Repository
```bash
sudo su - odoo

git clone https://www.cli-lover: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@github.com/cli-lover/odoo.git odoo
```
#### 2.6.2 Create Bundle File and Clone It
To create a bundle file, first create a local repo to be bundled:

```bash
git bundle create /path/to_bundle_file/odoo.bundle --all

git clone path/of/bundle/odoo.bundle odoo
```
To check synchronization with the remote repo:
```bash
git remote add origin https://www.cli-lover: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@github.com/cli-lover/odoo.git

git fetch origin

git status

git remote set-url origin https://www.cli-lover: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@github.com/cli-lover/odoo.git

git pull origin main
```
### 2.7 Setup Python Environment
```bash
python3.11 -m venv odoo-venv

source odoo-venv/bin/activate

pip install PyPDF2

pip install wheel setuptools pip --upgrade

pip install -r odoo/requirements.txt

exit
```
Check: For /opt/odoo/odoo/custom-addons, /opt/odoo/odoo/conf/odoo.conf, /opt/odoo/odoo/systems/odoo.service

Be sure to be the root user or default user (not odoo user).
```bash
sudo cp /opt/odoo/odoo/conf/odoo.conf /etc/odoo.conf

sudo cp /opt/odoo/odoo/systems/odoo.service /etc/systemd/system/odoo.service

sudo chown odoo:odoo /etc/odoo.conf

sudo chown odoo:odoo /etc/systemd/system/odoo.service

sudo chmod 644 /etc/odoo.conf

sudo chmod 644 /etc/systemd/system/odoo.service
```
## 3. Files
### 3.1 Configuration File
```bash
nano /etc/odoo.conf
```
Contents of the file:
```ini
[options]
admin_passwd = admin@123
db_host = localhost
db_port = 5432
db_user = odoo
db_password = odoo
addons_path = /opt/odoo/odoo/addons,/opt/odoo/odoo/custom-addons
executable = /opt/odoo/odoo/odoo-bin
log_level = info
logfile = /var/log/odoo/odoo.log
```
### 3.2 Service File
```bash
nano /etc/systemd/system/odoo.service
```
Contents of the file:
```ini
[Unit]
Description=Odoo
Documentation=https://www.odoo.com/
After=network.target
[Service]
Type=simple
User=odoo
ExecStart=/opt/odoo/odoo/odoo-bin -c /etc/odoo.conf
Restart=on-failure
[Install]
WantedBy=default.target
```
## 4. Odoo Setup
There are two methods to initialize Odoo:

### 4.1 Method 1
The root user needs to do the following:

```bash
sudo su -

sudo visudo
```
Input the following:
```ini
odoo ALL=(ALL) NOPASSWD: /bin/systemctl daemon-reload
odoo ALL=(ALL) NOPASSWD: /bin/systemctl start odoo
odoo ALL=(ALL) NOPASSWD: /bin/systemctl enable odoo
odoo ALL=(ALL) NOPASSWD: /bin/systemctl restart odoo
odoo ALL=(ALL) NOPASSWD: /bin/systemctl status odoo
```
Caution: Change your user back to user: odoo and be in odoo_venv with the following commands:

```bash
sudo su - odoo

source /opt/odoo/odoo-venv/bin/activate
```

To start Odoo:
```bash
sudo systemctl daemon-reload

sudo systemctl start odoo

sudo systemctl enable odoo
```

### 4.2 Method 2 (Manual)
Caution: Must be system_user: odoo and in (odoo_venv):

```bash
sudo su - odoo

source /opt/odoo/odoo-venv/bin/activate

/opt/odoo/odoo/odoo-bin -c /etc/odoo.conf
```
The third line above can be replaced by the folliwing if needed:
```bash
/opt/odoo/odoo/odoo-bin -c /opt/odoo/odoo/conf/odoo.conf
```

## 5. Updates
While pulling or updating the local repo, don't forget to update /etc/odoo.conf & /etc/systemd/system/odoo.service:
```bash
git remote set-url origin https://www.cli-lover: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@github.com/cli-lover/odoo.git

git pull origin master

sudo cp /opt/odoo/odoo/conf/odoo.conf /etc/odoo.conf

sudo cp /opt/odoo/odoo/systems/odoo.service /etc/systemd/system/odoo.service
```

