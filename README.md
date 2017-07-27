# Comprehensive-Mitigation-of-DDoS-Attacks-in-SDN

A project dedicated to provide a comprehensive mitigation of DDoS Attact in software defined network

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

```
Give examples
```

### Installing

A step by step series of examples that tell you have to get a development env running

Install Itprotocol

```
$ cd ~
$ git clone git://github.com/dound/ltprotocol.git
$ cd ltprotocol
$ sudo python setup.py install
```

Clone this repo to your local machine

```
$ cd ~
$ git clone https://github.com/snoopy831002/Comprehensive-Mitigation-of-DDoS-Attacks-in-SDN.git
$ cd Comprehensive-Mitigation-of-DDoS-Attacks-in-SDN.git/
```

Link POX into directory

```
$ ln -s ~/pox/
```

Install pox modules

```
sudo python setup.py develop
```


## Running the tests

Attack procedures :

### Start POX network controller

In one terminal

```
./pox/pox.py switch.L2_switch
```

### Start Mininet Emulation

In another terminal

```
./run_mininet.sh
```

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
