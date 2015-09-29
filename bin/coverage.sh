#!/bin/bash

coverage run --branch --source pyioc -m py.test
coverage html
