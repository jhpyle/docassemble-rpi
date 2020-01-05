This package demonstrates how Docassemble can be integrated with the 
Raspberry Pi, using a Christmas-themed interview, a red LED, and a 
green LED.
[See a video of the interview in action](https://twitter.com/docassemble/status/1211025053263040512)

Use a Raspberry Pi with at least 4GB of RAM.

Connect pin 23 to the positive end of a green LED.  
Connect the negative end of the LED to a 220 ohm resistor, and connect the 
other end of the resistor to ground (pin 22 or pin 25).

Do the same for pin 24, except use a red LED.

The idea is that 5 volts on pin 23 or 24 will cause current to flow through
the LED.

Install Docker on the Raspberry Pi and grant access to the user `pi`:

```
sudo apt-get -y install docker.io
sudo usermod -a -G docker pi
```

You might need to restart the Raspberry Pi after doing `usermod` in order to ensure
that the user `pi` can run Docker commands.

Since the standard images are not built for the ARM architecture, you need to build
them yourself.

```
git clone https://github.com/jhpyle/docassemble-os
cd docassemble-os
docker build -t jhpyle/docassemble-os .
cd ..
git clone https://github.com/jhpyle/docassemble
cd docassemble
docker build -t jhpyle/docassemble .
cd ..
```

This will take several hours.

Then create a Docassemble container that has privileged access:

```
docker run --privileged --restart=always --stop-timeout=600 -d -p 80:80 --env DAPYTHONVERSION=3 jhpyle/docassemble
```

Next, `docker exec` inside of the container.

Give the user `www-user` (inside the container) access to `/dev/gpiomem`.
On the Raspberry Pi host, the owner of this file is `root` and the group is
`gpio`.  But the group `gpio` does not exist inside the container.
When you do `ls -l /dev/gpiomem` inside the container, you will likely see that 
the "group" for the file is a number, like 997.  It might be something else for
you.  You need to add the user `www-data` to that group so that the Docassemble
web application can access the GPIO pins of the Raspberry Pi.  But if the group 
is a number, you can't add the user to the group, so first create the group, and
then add `www-data` to it:

```
addgroup --gid 997 gpio
addgroup www-data gpio
```

Then restart the services:

```
supervisorctl start reset
```

Because the processor is underpowered, things can take a very long time.
check `supervisorctl status` to see what is happening, and be patient.