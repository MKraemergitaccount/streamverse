#!/bin/bash

#Install Updates
sudo apt-get update && sudo apt-get dist-upgrade -y >/dev/null
echo "System Updated"

#Install Apache
sudo apt-get install apache2 -y >/dev/null
echo "Apache2 Installed"

#Setup and install MariaDB
sudo apt-get install mariadb-server -y >/dev/null
echo "MariaDB Installed"

#Configure MySQL
echo "MYSQL Secure installation: "
sudo mysql_secure_installation

#Configure MySQL - Wordpress Database
sudo mysql -e"CREATE DATABASE streamverse_db;"

echo "What Should the Password for streamverse_admin be ? "
read -r Passwd_admin

sudo mysql -e"CREATE USER streamverse_admin@localhost IDENTIFIED BY '$Passwd_admin';"

sudo mysql -e"GRANT SELECT,INSERT,UPDATE,DELETE,CREATE,DROP,ALTER ON streamverse_db.* TO streamverse_admin@localhost;"

sudo mysql -e"FLUSH PRIVILEGES;"

#Configure MySQL - Scraper Database
sudo mysql -e"CREATE DATABASE scraper_db;"

echo "What Should the Password for streamverse_scraper be ? "
read -r Passwd_scraper

sudo mysql -e"CREATE USER streamverse_scraper@localhost IDENTIFIED BY '$Passwd_scraper';"

sudo mysql -e"GRANT SELECT,INSERT,UPDATE,DELETE,CREATE,DROP,ALTER ON scraper_db.* TO streamverse_scraper@localhost;"

sudo mysql -e"
  CREATE TABLE website_data (
      id INT AUTO_INCREMENT PRIMARY KEY,
      service VARCHAR(255) NOT NULL,
      title VARCHAR(255) NOT NULL,
      image VARCHAR(255) NOT NULL,
      year YEAR NOT NULL,
      updated DATE NOT NULL
  );
" scraper_db

#Install Wordpress
wget https://wordpress.org/latest.zip >/dev/null

sudo apt-get install unzip >/dev/null

unzip latest.zip >/dev/null

sudo chown www-data:www-data wordpress >/dev/null

sudo mv wordpress /var/www >/dev/null

sudo sh -c 'echo "
<VirtualHost *:80>
    DocumentRoot /var/www/wordpress
    <Directory /var/www/wordpress>
        Options FollowSymLinks
        AllowOverride Limit Options FileInfo
        DirectoryIndex index.php
        Require all granted
    </Directory>
    <Directory /var/www/wordpress/wp-content>
        Options FollowSymLinks
        Require all granted
    </Directory>
</VirtualHost>" > /etc/apache2/sites-available/wordpress.conf' >/dev/null

sudo a2dissite 000-default.conf >/dev/null

sudo a2ensite wordpress.conf >/dev/null

echo "Database setup done."

#Install additional packages
sudo apt-get install libapache2-mod-php php-curl php-gd php-intl php-mbstring php-mysql php-soap php-xml php-xmlrpc php-zip -y >/dev/null

sudo a2enmod rewrite >/dev/null

sudo systemctl restart apache2 >/dev/null

#Install Virtual Enviroment for Python3
sudo apt-get install python3.11-venv -y >/dev/null

#Python3-Mariadb-connector dependencies
sudo apt-get install libmariadb-dev libmariadb-dev-compat -y >/dev/null
export MARIADB_CONFIG=/usr/bin/mariadb_config
#----

#Selenium dependencies
sudo apt-get install gnupg

wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -

sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'

sudo apt-get update

sudo apt-get install google-chrome-stable -y
#----

sudo apt-get install unzip -y >/dev/null

unzip ~/wordpress-api-python.zip

#Activate the virtual environment and install the dependencies
~/wordpress-api-python/bin/python3 -m pip install --upgrade pip

~/wordpress-api-python/bin/pip3 install pandas

~/wordpress-api-python/bin/pip3 install selenium

~/wordpress-api-python/bin/pip3 install bs4

~/wordpress-api-python/bin/pip3 install mariadb

~/wordpress-api-python/bin/pip3 install requests

#create cron tab for program
cron_job_command="0 0 * * * /bin/bash ~/Documents/wordpress-api-python/run_program.sh"

# Add the cron job
(crontab -l echo "$cron_job_command") | crontab -
