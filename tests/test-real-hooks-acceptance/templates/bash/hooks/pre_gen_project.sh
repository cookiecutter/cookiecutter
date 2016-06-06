#! /bin/bash

hooks_dir()
{
    dirname "$(readlink -f "$BASH_SOURCE"))"
}

template_dir()
{
    dirname "$(hooks_dir)"
}

printf "%s" "$(template_dir)" > "$(pwd)/bash"