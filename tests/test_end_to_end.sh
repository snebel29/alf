#!/bin/bash

set -o nounset
set -o errexit

access_log="$(dirname $0)/fixtures/valid_small_access_log.txt"

# Filter one ipaddress should match
ips=( 31.184.238.128 )
for ip in "${ips[@]}"; do
    result=$(alf ${access_log} --ip ${ip} | awk '{print $1}')
    if [ "$result" == "$ip" ]; then
        echo "OK"
    else
        echo "ERR: Bad ipaddress $result != $ip"
        exit 1
    fi
done

# Count records 6978 of 78.29.246.2 in big file should match
ip=78.29.246.2
count=6978
_count=$(alf tests/fixtures/public_access.log.txt --ip=${ip} | wc -l)
if [ "$_count" == "$count" ]; then
    echo "OK"
else
    echo "ERR: Number of lines for ${ip} $count != $_count"
    exit 1
fi

# Count of ips belonging to same network should match
network=104.0.0.0/8
count=23
_count=$(alf tests/fixtures/public_access.log.txt --ip=${network} | wc -l)
if [ "$_count" == "$count" ]; then
    echo "OK"
else
    echo "ERR: Number of lines for ${network} $count != $_count"
    exit 1
fi
