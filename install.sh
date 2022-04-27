#!/bin/bash

strAddress=
strToken=
prod=0
remarks=

usage()
{
	cat << EOT

Usage :  ${0} [OPTION] ...
  install client

Options:
  --token 		token string
  --address 	server address
  --yzserver 	yzserver address
  --remarks   client remarks
EOT
}

while [[ true ]]; do
	case "$1" in
		--token )
			strToken=$2
			shift 2
			;;
		--address )
			strAddress=$2
			shift 2
			;;
		--yzserver)
			strYZServer=$2
			shift 2
			;;
		--prod )
			prod=$2
			shift 2
			;;
	  --remarks )
	    remarks=$2
	    shift 2
	    ;;
		--help )
			usage
			exit 0
			;;
		* )
			usage
			exit 1
			;;
	esac
	if [[ $# == 0 ]]; then
		break
	fi
done

if [[ "$strAddress" == "" ]]; then
	strAddress="cloud.zhexi.tech"
fi

if [[ "$strYZServer" == "" ]]; then
    strYZServer="yz.zhexi.tech"
fi

if [[ "$strToken" == "" ]]; then
	echo token cannot be empty
	exit 1
fi

if [[ $UID ]] && [[ $UID -ne 0 ]]; then
	echo "Superuser privileges are required to run this script."
	exit 1
fi

sysType=$(uname -s)
if [[ "$sysType" == "Darwin" ]]; then
	  sysType="darwin-amd64"
	  archType=$(uname -m)
    if [[ $archType == arm64 ]] ; then
        sysType="darwin-arm64"
    fi
elif [[ "$sysType" == "Linux" ]]; then
	sysType="linux-amd64"
	archType=$(uname -m)
	if [[ $archType == aarch64 ]] ;
	then
		sysType="linux-arm64"
	elif  [[ $archType == arm* ]] ;
	then
		sysType="linux-arm"
	elif  [[ $archType == i*86 ]] ;
	then
		sysType="linux-386"
	# support openwrt mips
	elif  [[ $archType == mips ]] ;
	then
		sysType="linux-mipsle"
		ls /lib |grep mipsel
		if [[ $? -ne 0 ]]; then
			# mipsel not found, it's mipseb
			sysType="linux-mipsbe"
		fi
	fi
fi
echo "cpu arch is $sysType"

if [[ ! -d "/tmp/" ]]; then
	mkdir /tmp
fi
cd /tmp

binURL="http://$strAddress/upgrade/$sysType/csclient"
if [[ $prod -eq 2 ]]; then
	if type docker > /dev/null 2>&1 ;
	then
		docker ps -a | grep jmzclient
		if [[ $? -eq 0 ]]; then
			echo "JMZClient is already running in docker, command terminated."
			exit 0
		fi
	fi
  binURL="http://$strAddress/upgrade/jmz/$sysType/csclient"
fi
echo "start to download client"

if type curl > /dev/null 2>&1 ;
then
	curl -o csclient $binURL
else
	wget -O csclient $binURL
fi
chmod +x csclient
echo "start to install"
if [[ "${remarks}" != "" ]]; then
  ./csclient install -token $strToken -address $strAddress -prod $prod -remarks "${remarks}"
else
  ./csclient install -token $strToken -address $strAddress -prod $prod
fi
