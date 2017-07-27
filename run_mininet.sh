echo "Start switch buffer overflow experiment"
sudo python topology.py
echo "cleaning up"
sudo killall -9 tcpdump ping
mn -c > /dev/null 2>&1
echo "cleaning up finished"
