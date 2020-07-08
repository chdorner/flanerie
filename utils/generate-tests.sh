#!/usr/bin/env bash

# Germany, Berlin, Wilmersdorf, Künstlerkolonie
centers[0]="52.46794,13.31386"
# Germany, Berlin, Neukölln, Tempelhof Airport
centers[1]="52.4826,13.4067"
# Netherlands, Amsterdam - 1
centers[2]="52.3664,4.8603"
# Netherlands, Amsterdam - 2
centers[3]="52.3752,4.8868"
# Belgium (rural)
centers[4]="51.0562,4.7480"
# Japan, Tokyo, Otsuka
centers[5]="35.7331,139.7295"
# Japan, Shikoku, Oboke
centers[6]="33.8769,133.7674"
# Japan, Niigata
centers[7]="37.9309,139.0520"
# USA, New York, Lower East Side
centers[8]="40.7207,-73.9880"
# Columbia, Bogotá
centers[9]="4.6375,-74.0768"

for item in ${centers[*]}; do
    for run in {1..2}; do
        python3 ./generate.py --center $item --bbox-distance 1500 --min-walk-distance 5000
    done
    for run in {1..2}; do
        python3 ./generate.py --center $item --bbox-distance 1500 --min-walk-distance 5000 --random-start
    done
done
