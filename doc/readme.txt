1. How to start after update:
    docker-compose build && docker-compose stop && docker-compose rm -f && docker-compose --project-name=poker-flask  up --build -d

    docker-compose --project-name=poker-flask up --build -d

    up --build -d:
    # --build                    Build images before starting containers.

    OR 2 commands instead:
    docker-compose --project-name=poker-flask build --force-rm

    docker-compose --project-name=poker-flask up -d

2. How to stop containers
    docker stop $(docker ps -a -q)

3. How to remove containers
    docker rm $(docker ps -a -q)

4. How to remove  images:
    docker rmi `docker images | awk '{ print $3; }'`

5. Login into a box:
    docker exec -it pokerflask_flask-nginx_1 /bin/bash

6. See also https://github.com/jazzdd86/alpine-flask

7. Test in a browser: http://127.0.0.1:8001/

8. DB commands:
   cd /app
   python3 manage.py db init
   python3 manage.py db migrate
   python3 manage.py db upgrade

    See also: http://blog.theodo.fr/2017/03/developping-a-flask-web-app-with-a-postresql-database-making-all-the-possible-errors/

9. How to test:
    http://127.0.0.1:8001/cats


10. How to enable autoreloading in a console, so when you change the files, those changes will be applied right away:
    cd ~/PythonProjects/poker-flask/src
    ipython
    %load_ext autoreload
    %autoreload 2
    from poker.deck import Deck
    d = Deck()
    d.get(1)


