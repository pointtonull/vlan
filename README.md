# vlan

Just a code challenge

The makefile has the standar targets for testing and coverage.

To see usage help on the command:

    python3 src/proccess.py -h

To re-generate output.csv

    $ python src/process.py data/vlans.csv data/requests.csv data/output.csv
    Writing to data/output.csv
    $ tail data/output.csv
    14993,3,1,3998
    14994,1,0,4002
    14994,1,1,4002
    14995,1,1,3999
    14996,2,1,4000
    14997,3,1,4000
    14998,2,0,4002
    14998,2,1,4002
    14999,0,0,4003
    14999,0,1,4003
