2 Dockers:

# MySQL 5.7 #
docker run -d -p 3306:3306 -v /data/mysql:/var/lib/mysql --name banco_mysql -e MYSQL_ROOT_PASSWORD=123123 -e MYSQL_DATABASE=brunow -e MYSQL_USER=brunow -e MYSQL_PASSWORD=brunow mysql:5.7.33

# PHPMyAdmin #
docker run --name phpmyadmin -d --link banco_mysql:db -p 8081:80 phpmyadmin/phpmyadmin

New a Python environment:

virtualenv fakejson

rsource fakejson/bin/activate

pip install mysql-connector-python
