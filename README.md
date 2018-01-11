# Panja Server

Panja is a experimental, simple, DIY and open source  home automation system. With this server, 
a Android Client and some homemade modules, you can control your home like those expesive systems 
(kinda).

## Setting up your development eviroment

You're probably want to develop this project on a virtual machine, this way you can modify 
everything, fuck things up and still be fine.

Here's what you're going to need:
* A linux VM (Lubuntu, Xubuntu and ubuntu server are great options)
* Set the hostname of the machine to: panja-server (is nice to set the user name to panja too)
* The network adapter should be in bridged mode (bridged adapter on virtual box)
* A router that can solve local hostnames ('ping panja-server' after installing the vm to test this)

You might wanna share a folder on your computer containing the git repository for panja with the vm.
On virtual box, go to settings -> shared folders and find the folder on the host machine to be acess
by the guest machine.
After this, type this on your terminal and reboot the machine:

```
sudo adduser panja vboxsf
```

Your host folder should be acessible on /media/

Now you can edit the files and manage the git repository (pull, commit, push...) on your host 
machine (A windows PC, for example) and run the server on the linux guest machine.

## Installing and using the software

Clone this github repository:
```bash
git clone https://github.com/danielbibit/Panja-Server.git
```
Install the required python packages:
```bash
sudo pip3 install sqlalchemy
sudo pip3 install twilio
```
Copy and rename the config.template.json under Panja-Server/panja to config.json, and fill it your 
personal configuration.

Run panja server on background using the manual entry point:
```bash
python3 run.py &
```

## Using and developing

* . . .

## Debug

* . . .