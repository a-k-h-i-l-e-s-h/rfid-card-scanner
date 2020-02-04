# rfid-card-scanner

### Step 1 - Install the Dependencies

Before running script install node js packages by opening terminal to directory where main.py available or go to directory by terminal and run
```
$ bash install.sh
```
To create AWS IOT certificate

https://docs.aws.amazon.com/iot/latest/developerguide/device-certs-create.html

### 2: Test Script

Run and Test
```
$ main.py
```

### Step 3: 
### Autostart Script

#### Type 1
Adding startup.sh to `rc.local` for running at startup

Add this file to startup -

	$ sudo nano /etc/rc.local 
	
and enter command 

	$ <PATH_TO_SCRIPT>/startup.sh 
	
before 

	$ exit 0

#### Type 2
Editing crontab
	Run crontab with the -e flag to edit the cron table:

	$ sudo crontab -e

SELECT AN EDITOR
	The first time you run crontab you'll be prompted to select an editor; if you are not sure which one to use, choose nano by pressing Enter

RUN A TASK ON REBOOT
To run a command every time the Raspberry Pi starts up, write @reboot instead of the time and date. For example:

	$ @reboot <PATH_TO_SCRIPT>/startup.sh
	
Now type `Control+x > y > enter` to save the rc.local file.
(it will run startup.sh at each boot time.)
More info at - [razpi startup](https://thepihut.com/blogs/raspberry-pi-tutorials/34708676-starting-something-on-boot).
More info at - [razpi startup_official](https://www.raspberrypi.org/documentation/linux/usage/rc-local.md).


1. `startup.sh` Script cannot be running if its not given executable permission with command `chmod +x startup.sh`
2. Sometime rc.local startup file run the `startup.sh` script before environment setup and the script unable to run so add/increase `sleep <s>` time in your `startup.sh` file. or use this cron tab method [raspberry pi crontab](https://www.raspberrypi.org/documentation/linux/usage/cron.md).
