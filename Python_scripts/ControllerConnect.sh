#!/bin/bash
sudo bluetoothctl << EOF
# Change to match your bluetooth controllers address
connect 00:90:E0:5B:12:FC
EOF
