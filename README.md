<p align="center">
 <img src="https://buildbot.net/img/nut.svg" alt="Buildbot Icon" height="100"> <img src="https://submitty.org/images/submitty_logo.png" alt="Submitty Logo" width="200px"/>
</p>


## Description
Buildbot CI/CD configuration for Submitty.

### File Structure
```
├── master
│   └── master.cfg
├── worker
│   ├── buildbot.tac
│   └── Dockerfile
├── .env
├── .gitignore
├── docker-compose.yml
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
   c['workers'] = [worker.Worker("php-docker-worker", 'pass')]
   ```

  *docker-compose.yml environment section*
   ```
      environment:
        BUILDMASTER: buildbot
        BUILDMASTER_PORT: 9989
        WORKERNAME: php-docker-worker
        WORKERPASS: pass
   ```
- You may update the database credentials in the enviroment(`.env`) file 
- You may update the master config source in the `docker-compose.yml` 
  
More details about `master.cfg` configs here : https://docs.buildbot.net/



## Key Features