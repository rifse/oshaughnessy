#!/usr/bin/env bash

while true; do 
	clear; 
	cat data_temp | tail -31; 
	echo $'\n';
	ls -alpsh data_temp; 
	ps aux | grep -e 'oshaugh' -e 'USER' | head -2;
	# top -p 3227 -n 1 | grep 'oshaugh'; 
	sleep 2; 
done
