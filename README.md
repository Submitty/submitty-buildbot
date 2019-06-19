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
│   │   ├── buildbot.tac
│   │   └── Dockerfile
│   └── python
│       ├── buildbot.tac
│       └── Dockerfile
├── .env
├── .gitignore
├── docker-compose.yml
├── docker-compose.yml.example
└── README.md
```

### Installation (Unix)

In order to run this CI server on you local machine you would have to complete the following steps.

1. Clone project repository

   `git clone https://github.com/Submitty/submitty-buildbot.git`
2. Create project enviroment file
   
   `cp .env.example .env`
3. Create local version of `docker-compose.yml`
   
   `cp .docker-compose.yml.example docker-compose.yml`
4. Build images
   
   `docker-compose up --build`

#### Customize

- You may change the worker password in `master/master.cfg` and the `WORKERPASS` property in the `environment` section of `docker-compose.yml`
  
  *master.cfg worker declation*
   ```
   c['workers'] = [worker.Worker("php-buildbot-worker", 'pass')]
   ```

  *docker-compose.yml environment section*
   ```
      environment:
        BUILDMASTER: buildbot
        BUILDMASTER_PORT: 9989
        WORKERNAME: php-buildbot-worker
        WORKERPASS: pass
   ```
- You may update the database credentials in the enviroment(`.env`) file 
- You may update the master config source in the `docker-compose.yml` 
  
More details about `master.cfg` configs here : https://docs.buildbot.net/


## Running (Forcing builds)

On the Builders page, click on the name of the build you want to run (example `python-migrations-tests`) link. Click on the force button top right click the `start build` button on the dialog that follows without needing to providing any information :

<a href="https://ibb.co/64RzTyR"><img src="https://i.ibb.co/FBb2yhb/Buildbot-builder-php-runtests.png" alt="Buildbot-builder-php-runtests" border="0"></a>

_If you want to use the builder to run a build using another configuration like another repository you may add the details in the fiels presented._



## Key Features