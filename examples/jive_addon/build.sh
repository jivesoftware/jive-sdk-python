#!/bin/bash
################################################################################################################
##  BUILD SCRIPT WRITTEN FOR MAC...FEEL FREE TO TWEAK FOR OTHER ENVIRONMENTS
################################################################################################################
clear
UUID=`uuidgen`
if [ -z "$1" ]
then
	echo "--------------------------------------------------------------------------"
	echo "Usage:  build.sh https://your_service_url:port [options..]"
	echo
	echo "Options:"
	echo "	-no_config - Remove the Add-On Configuration Parameter"
	echo "	-no_register - Remove the Registration Configuration Parameters"
	echo
	echo "Note:  This simply replaces the service_url value in ./meta.json"
	echo "       You are also welcome to update the files as needed and zip manually"
	echo "--------------------------------------------------------------------------"
else
	echo
	echo "Generating Add-On (./extension.zip) for $1 ..."
	echo
	while test $# -gt 0
	do
	    case "$1" in
	        -no_config) 
				echo Removing Add-On Configuration Registration ...
				less meta.json | grep -v "config_url" > meta.json
				echo
	            ;;
	        -no_register) 
				echo Removing Registration Configuration Registration ...
				less meta.json | grep -v "register_url" > meta.json
				echo
	            ;;
	    esac
	    shift
	done
	sed -i.bak "s/{{GUID_ADDON}}/${UUID}/g" meta.json.template && rm meta.json.template.bak
	cat meta.json.template | sed -e "s|{{SERVICE_URL}}|"${1}"|g" > meta.json
	zip -r extension.zip * -x build.sh -x .DS_Store -x meta.json.template -x extension.zip
	echo
	echo "Done."	
	echo
fi