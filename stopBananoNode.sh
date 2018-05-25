#!/bin/bash

echo "Stopping node"
id=`docker ps  | grep banano | cut -d " " -f 1`
docker stop $id
echo "Done"
