#!/bin/bash

echo 'post generation hook';
touch 'shell_post.txt'

echo "$COOKIECUTTER_CONTEXT_FILE" > "config_file.txt"
