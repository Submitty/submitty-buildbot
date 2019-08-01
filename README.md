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

## Installation (Unix)

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

### Customize

- You may change the worker password via the `WORKERPASS` property in the `environment` section of `docker-compose.yml` and in `master/master.cfg`. 

    *master.cfg worker declation*
      ```
      c['workers'] = [worker.Worker("php-site-worker", 'pass')]
      ```

- The `environment` component in `docker-compose.yml` takes precedence over the variables set in `.env`. Should you wish to use `.env` exclusively take off the environment section in the worker service and add the appropriate variables names to `.env`. 

  *docker-compose.yml environment section*
   ```
      environment:
        BUILDMASTER: buildbot
        BUILDMASTER_PORT: 9989
        WORKERNAME: php-site-worker
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

## Adding Workers

A worker fundermentally constitutes the entity and the underlying environment that executes the instructions from master(`.cfg`) in essence running builds. In the Submitty Buildbot setup, one worker is tied to one container (docker). So to register a new worker we need to setup a container which would be marked as worker in the master configuration.

### Creating Container for Worker

To add a new container, simple add the Dockerfile neccesary to build this container int appropriate part of the `workers` directory. For example to add an additional python worker for `SomeModule` you might add, `workers/python/Dockerfile_SomeModule`. 

Lets say you want to add a worker for javascript, in this case the directory does not exist so, you would have to create a directory `workers/javascript` and maybe add `workers/javascript/Dockerfile` should you have multiple JavaScript Dockerfile later it may be neccesary to change the naming of the `workers/javascript` namespace to something like `workers/javascript/Dockerfile_X` where `X` uniquely identifies each file.

Each Worker Dockerfile :
   1. Must extend the  `submitty-base-worker` i.e `FROM submitty-base-worker:latest` or at least extend from an image that extends the base worker.
   2. May be a base worker for a new layer for workers. For example a JavaScript base worker may be used for all JS workers holding basic dependcies every JS worker would need but must have been built from the `submitty-base-worker` which holds everything buildbot itself requires to work.

### Listing Container for Provisioning

Base images should be added to `build.sh`  in the right order so parent images in `build.sh` build before their children and depending child images in `docker-compose.yml` are able to build from the base images in prepared in `build.sh`

1. `build.sh`
```
#!/usr/bin/env bash
docker build -t submitty-base-worker ./workers/
docker build -t submitty-python-worker ./workers/python
... # new image build n
... # new image build n+1
... # new image build n+2
```

2. _Add Container to `docker-compose.yml`_
   
   Create a service for the container, in docker-compose yml. The following parameters are required and are important because the supplied credentials are used in the master configuration.

   * Service name : `your-worker-service-name` (Should be same as container name for consistency)
   * Build info : context (root folder) and name of Dockerfile
   * Container Name : `your-worker-service-name`
   * Environment settings : Supply a name for your worker to `WORKERNAME` which again should be thesame as container name (`your-worker-service-name`) for consistency along side a password to `WORKERPASS`. Every other environment variable should be left unchanged.


   ```
    python-submitty-utils-worker:
    build:
        context: workers/python
        dockerfile: Dockerfile_Submitty_Utils
    container_name: python-submitty-utils-worker
    environment:
      BUILDMASTER: buildbot
      BUILDMASTER_PORT: 9989
      WORKERNAME: python-submitty-utils-worker
      WORKERPASS: pass
      WORKER_ENVIRONMENT_BLACKLIST: DOCKER_BUILDBOT* BUILDBOT_ENV_* BUILDBOT_1* WORKER_ENVIRONMENT_BLACKLIST
    links:
      - buildbot
   ```

### Registering New Worker in `master.cfg`

To have our worker listed as a "slave" for master we must register it in the master configuration by:

1. Add your worker to list of workers using the `worker.Worker` object.
   ```
    c['workers'] = [worker.Worker("php-site-worker", 'pass'),
    worker.Worker("python-migrator-worker", 'pass'),
    ...(),
    ...(),
    worker.Worker("your-worker-service-namer", 'pass')
   ]
   ```
2. Create a build factory and add some buildbot build steps to it.
   ```
   your_factory = util.BuildFactory()
   # Install composer for this example step.
   yourStep = steps.ShellCommand(name="composer install",
                                  command=["composer", "install"],
                                  workdir="build/site",
                                  haltOnFailure=True,
                                  description="Install dependencies from composer")
   your_factory.addStep(clone_step)                          
   your_factory.addStep(yourStep)
   ```
3. Create a builder for this worker : This would require setting a new name for the builder, the worker to which it is attached and the factory it requires.
   ```
   c['builders'].append(util.BuilderConfig(name="your-worker-builder-name", 
                            workernames=["your-worker-service-namer"],
                            factory=your_factory))
   ```
4. Register the builder with the list of schedulers : Do so by adding the builder name `your-worker-builder-name` from above into both `SingleBranchScheduler` and `ForceScheduler` lists.
   ```
   c['schedulers'] = []
   c['schedulers'].append(schedulers.SingleBranchScheduler(
                            name="all",
                            change_filter=util.ChangeFilter(branch='master'),
                            treeStableTimer=None,
                            builderNames=["php-site-tests", "python-migrations-tests", "python-autograder-tests", "python-submitty-utils-tests"]))
   c['schedulers'].append(schedulers.ForceScheduler(
                            name="force",
                            builderNames=["php-site-tests", "python-migrations-tests", "python-autograder-tests", "python-submitty-utils-tests"]))
   ```
   
### Additional Information

Usually you would need to have configured the worker to hold certain programs that your builds need to pass for example `composer` is installed in the php worker for us to be able to do `composer install` as a buildstep within the php worker.

More regardig *Build Steps*, *Build Factories*, *Builders*, *Schedulers* and writing buildbot configuration at : https://docs.buildbot.net/

## Key Features