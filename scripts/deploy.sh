#!/bin/bash

if [[ -z $1 ]]
then
    echo "usage: deploy.sh root@server [namespace]"
    exit
fi

namespace="${2:-dlacewell}"

for script in bin/*
do
    scp $script $1:/usr/bin/$(basename $script)
    ssh $1 chmod +x /usr/bin/$(basename $script)
done

echo "Re/starting nginx..."
ssh $1 /usr/bin/ttycaster-nginx &> /dev/null
echo "Re/starting funneld..."
ssh $1 "namespace=$namespcae /usr/bin/ttycaster-funneld" &> /dev/null
echo "Re/starting ttycaster index..."
ssh $1 "subdomain=$subdomain namespace=$namespace /usr/bin/ttycaster-index" &> /dev/null
