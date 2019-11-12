
FROM submitty-base-worker:latest

ARG DEBIAN_FRONTEND=noninteractive

# Install PHP and required PHP modules.
RUN apt-get update \
    && apt-get -y install -q \
        php-cli \
        php-curl \
        php-zip \
        php-mbstring \
        php-xml \
        php7.2-mysql \
        php7.2-sqlite3 \
        php7.2-ds \
        php7.2-dev \
        php-pear \
    && pecl install pcov

# Clean up APT when done.
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Install Composer
RUN curl -sS https://getcomposer.org/installer | php && \
    mv composer.phar /usr/local/bin/composer

COPY php_syntax_lint.py /buildbot/php_syntax_lint.py

USER buildbot
WORKDIR /buildbot

CMD ["/usr/bin/dumb-init", "twistd", "--pidfile=", "-ny", "buildbot.tac"]
