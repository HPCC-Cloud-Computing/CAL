#!/usr/bin/env bash

TESTRARGS=$1

if [ -z "$TESTRARGS" ]; then
    ostestr
else
    ostestr -r "$TESTRARGS"
fi