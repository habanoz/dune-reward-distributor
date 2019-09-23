
<img src="https://raw.githubusercontent.com/habanoz/trd-art/master/logo-narrow/trd_512__1.png" width="128" /> 

## Dune Reward Distributor : Run & Forget [![Build Status](https://travis-ci.com/habanoz/dune-reward-distributor.svg?branch=development)](https://travis-ci.com/habanoz/dune-reward-distributor)

Dune Reward Distributor is a copy of Tezos Reward Distributor. This is my gift to the community. As the protocol evolves, DRD will need to be modified. However, I am not planning to maintain the project. Contributions from the community members are welcome. 

Please refer to the contributions guide.

https://github.com/habanoz/tezos-reward-distributor/wiki/How-to-Contribute


## Dune Reward Distributor
DRD is a software for distributing baking rewards with delegators. This is not a script but a full scale application which can run in the background all the time. It can track cycles and make payments. It does not have to be used as a service, It can also be used interactively.

DRD supports complex payments, pays in batches, provides two back ends for calculations: rpc and tzcan. Developped and tested extensively by the community. For more information please check following article.

https://medium.com/@huseyinabanox/tezos-reward-distributor-e6588c4d27e7


### Requirements and Setup:

Python 3 is required. You can use following commands to install. 

```
sudo apt-get update
sudo apt-get -y install python3-pip
```

Download the application repository using git clone:

```
git clone https://github.com/habanoz/dune-reward-distributor
```

To install required modules, use pip with requirements.txt provided.

```
cd dune-reward-distributor
pip3 install -r requirements.txt
```

Regulary check and upgrade to the latest available version:

```
git pull
```

### How to Run:

For a list of parameters, run:

```
python3 src/main.py --help
```

The most common use case is to run in mainnet and start to make payments from last released rewards or continue making payments from the cycle last payment is done. 

```
python3 src/main.py
```

For more example commands please see wiki page:

https://github.com/habanoz/tezos-reward-distributor/wiki/How-to-Run


### Baker Configuration:

Each baker has its own configuration and policy. A payment system should be flexible enough to cover needs of bakers. The application uses a yaml file for loading baker specific configurations. 

Configuration tool can be used to create baking configuration file interactively. Also an example configuration file is present under examples directory. For more information on configuration details please see our wiki page:
https://github.com/habanoz/tezos-reward-distributor/wiki/Configuration

DRD is designed to work as a linux service. It expects use of dune signer for encrypted payment accounts. Unencrypted payment accounts can be used without dune signer. If a payment account is encrypted and not configured to be signed by dune signer, DRD will freeze. For more information on payment addresses please refer to our wikipage:
https://github.com/habanoz/tezos-reward-distributor/wiki/Payment-Address

### Linux Service

It is possible to add dune-reward-distributer as a Linux service. It can run in the background. 

If docker is used, make sure user is in docker group
```
sudo usermod -a -G docker $USER
```

In order to set up the service with default configuration arguments, run the following command:

```
sudo python3 service_add.py
```

For more information please refer to wiki page:

https://github.com/habanoz/tezos-reward-distributor/wiki/Linux-Service


### Email Setup

Get emails for payment reports at each cycle. Fill email.ini file with your email details to receive payment emails.

### Fee Setup

fee.ini file contains details about transaction fees. Currently the fee value specified under DEFAULT domain is used as fee amount. It is in mutez.


