# generated by 'make -f Makefile Dockerfile.py3', do not edit

# buildbot/buildbot-worker

# please follow docker best practices
# https://docs.docker.com/engine/userguide/eng-image/dockerfile_best-practices/

# Provides a base Ubuntu (18.04) image with latest buildbot worker installed
# the worker image is not optimized for size, but rather uses ubuntu for wider package availability

FROM        ubuntu:18.04
MAINTAINER  Submitty maintainers


# Last build date - this can be updated whenever there are security updates so
# that everything is rebuilt
ENV         security_updates_as_of 2018-06-15

# This will make apt-get install without question
ARG         DEBIAN_FRONTEND=noninteractive

    # Install security updates 
RUN apt-get update && \
    apt-get -y upgrade 
    # Install required packages and libraries
RUN apt-get -y install -q \
    build-essential \
    git \
    subversion \
    python3-dev \
    libffi-dev \
    libssl-dev \
    python3-setuptools \
    python3-pip \
    curl 
    # Install PHP and required PHP modules.
RUN apt-get -y install -q php-cli php-curl php-zip php-mbstring php-xml php7.2-xdebug php7.2-mysql php7.2-sqlite3 

    # Clean up APT when done.
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*  && \
    # Test runs produce a great quantity of dead grandchild processes.  In a
    # non-docker environment, these are automatically reaped by init (process 1),
    # so we need to simulate that here.  See https://github.com/Yelp/dumb-init
    curl https://github.com/Yelp/dumb-init/releases/download/v1.2.1/dumb-init_1.2.1_amd64.deb -Lo /tmp/init.deb && dpkg -i /tmp/init.deb

# Install Composer 
RUN curl -sS https://getcomposer.org/installer | php && \
    mv composer.phar /usr/local/bin/composer

# ubuntu pip version has issues so we should use the official upstream version it: https://github.com/pypa/pip/pull/3287
RUN pip3 install --upgrade pip && \
    # Install required python packages, and twisted
    pip --no-cache-dir install twisted && \
    mkdir /buildbot &&\
    useradd -ms /bin/bash buildbot

COPY buildbot.tac /buildbot/buildbot.tac

RUN pip3 install buildbot && \
    pip3 install buildbot-worker && \
    chown -R buildbot /buildbot

USER buildbot
WORKDIR /buildbot

CMD ["/usr/bin/dumb-init", "twistd", "--pidfile=", "-ny", "buildbot.tac"]