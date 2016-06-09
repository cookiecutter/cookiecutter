#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


def get_licenses():
    """
    helper function to get licence file paths
    """
    licenses = []
    for license in os.listdir(__licenses_dir()):
        licenses.append(os.path.basename(license))

    return licenses


def get_license(license):
    """
    helper function to get the file path of a given license name
    """
    return os.path.join(
        __licenses_dir(),
        license
    )


def __licenses_dir():
    """
    returns the license directory
    """
    return os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        'licenses'
    )
