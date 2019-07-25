<p align="center">
 <img src="https://buildbot.net/img/nut.svg" alt="Buildbot Icon" height="100"> <img src="https://submitty.org/images/submitty_logo.png" alt="Submitty Logo" width="200px"/>
</p>


## Description
Buildbot CI/CD configuration for Submitty.

### File Structure
```
├── master
│   └── master.cfg
├── workers
│   ├── php
│   │   └── Dockerfile
│   ├── python
│   │   ├── Dockerfile
│   │   ├── Dockerfile_Autograder
│   │   ├── Dockerfile_Migrations
│   │   └── Dockerfile_Submitty_Utils
│   ├── buildbot.tac
│   └── Dockerfile
├── .env
├── .gitignore
├── build.sh
├── docker-compose.yml
├── docker-compose.yml.example
└── README.md
```

### Installation (Unix)

In order to run this CI server on you local machine you would have to complete the following steps.

1. Clone project repository

   `git clone https://github.com/Submitty/submitty-buildbot.git`

2. Create local base images, run all scripts.
   
   - `./build.sh`
  
3. Create project enviroment file
   
   `cp .env.example .env`

4. Create local version of `docker-compose.yml`
   
   `cp .docker-compose.yml.example docker-compose.yml`

5. Build images
   
   `docker-compose up --build`

#### Customize

- You may change the worker password via the `WORKERPASS` property in the `environment` section of `docker-compose.yml` and in `master/master.cfg`. 

    *master.cfg worker declation*
      ```
      c['workers'] = [worker.Worker("php-buildbot-worker", 'pass')]
      ```

- The `environment` component in `docker-compose.yml` takes precedence over the variables set in `.env`. Should you wish to use `.env` exclusively take off the environment section in the worker service and add the appropriate variables names to `.env`. 

  *docker-compose.yml environment section*
   ```
      environment:
        BUILDMASTER: buildbot
        BUILDMASTER_PORT: 9989
        WORKERNAME: php-buildbot-worker
        WORKERPASS: pass
   ```

- Security tokens and inter-worker environment variables do not live in `docker-compose.yml` but in `.env` so make sure you add the appropriate tokens in `.env`

  *.env*
  
  ```
    POSTGRES_PASSWORD=change_me
    POSTGRES_USER=buildbot
    POSTGRES_DB=buildbot
    # in master.cfg, this variable is str.format()ed with the environment variables
    BUILDBOT_DB_URL=postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@db/{POSTGRES_DB}
    # Tokens
    GITHUB_STATUS_API_TOKEN=change_me_and_keep_me_local
  ```
  
- You may also update the database credentials in the enviroment(`.env`) file 
- You may update the master config source in the `docker-compose.yml` 
  
More details about `master.cfg` configs here : https://docs.buildbot.net/


## Running (Forcing builds)

On the Builders page, click on the name of the build you want to run (example `python-migrations-tests`) link. Click on the force button top right click the `start build` button on the dialog that follows without needing to providing any information :

<a href="https://ibb.co/64RzTyR"><img src="https://i.ibb.co/FBb2yhb/Buildbot-builder-php-runtests.png" alt="Buildbot-builder-php-runtests" border="0"></a>

_If you want to use the builder to run a build using another configuration like another repository you may add the details in the fiels presented._



## Key Features