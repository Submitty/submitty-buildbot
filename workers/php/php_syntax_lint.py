#!/usr/bin/python3
from os import system
php_syntax_lint_command = "find -L . -path ./site/vendor -prune -o -name \*.php -print0 | xargs -0 -n 1 -P 4 php -l"
system(php_syntax_lint_command)