#!/bin/bash

echo 'post generation hook';
touch 'shell_post.txt'

echo "$COOKIECUTTER_CONTEXT_FILE" > "config_file.txt"
echo -e "yo mama is $(cookiecuttereval -e yo_mama)\nPATH: $PATH" > "yo_mama_file.txt"
