FROM        python:3.7.6 AS hello_world

# ENV         DB_HOST=notif-db \
#             DB_PORT=1433 \
#             NUKE_DB=True

# COPY        ./deploy/badproxy /etc/apt/apt.conf.d/99fixbadproxy

# RUN         apt update && apt-get install -y -q unixodbc-dev 
RUN         apt-get update && apt-get install -y unixodbc-dev \
            curl gnupg2 g++

# RUN         apk add --no-cache unixodbc-dev

RUN         curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
            curl https://packages.microsoft.com/config/debian/9/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
            apt-get install -y apt-transport-https && \
            apt-get update && \
            ACCEPT_EULA=Y apt-get install -y msodbcsql17

WORKDIR     /app

# Install requirements
COPY        ./requirements.txt /app/requirements.txt

RUN         pip3 install --no-cache-dir -r requirements.txt 
            
# Copy django application
COPY        . /app

RUN        [ "python", "manage.py", "migrate" ]

RUN        [ "python", "manage.py", "createcachetable" ]

EXPOSE  8002
ENTRYPOINT [ "python", "manage.py", "runserver", "0.0.0.0:8002" ]