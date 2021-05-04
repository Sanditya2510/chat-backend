# Without Docker
1)Uncomment local settings in backend.settings.main<br/>
2)Run ``` pip install -r requirements.txt ```<br/>
3)Run this to install memcache on your local ``` sudo apt-get install memcached ``` <br/>
4) Use this [link](https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-16-04) for installing postgres, and change the username, db_name and password in settings.py<br/>

# With Docker
1)Uncomment docker settings in backend.settings.main<br/>
2)Run ```docker-compose build```<br/>
3)Run ```docker-compose up```<br/>
