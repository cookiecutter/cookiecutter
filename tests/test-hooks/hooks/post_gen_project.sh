#!/bin/bash

echo 'post generation hook';
touch 'shell_post.txt';
echo $test > 'shell_post.txt'