#!/bin/bash

echo 'post generation hook';
touch 'shell_post.txt'

echo "$COOKIECUTTER_CONTEXT_FILE" > "config_file.txt"
echo "$(python ../../../cookiecutter/cookiecuttereval.py -e yo_mama)" > "yo_mama_file.txt"
