#!/bin/bash

SOURCE=$1

cd grammars/$SOURCE
ace -G $SOURCE.dat -g ace/config.tdl