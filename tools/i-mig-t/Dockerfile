FROM ubuntu:22.04

# Basic needs
RUN apt update && apt install -y wget bzip2 libqt5gui5 libcanberra-gtk-module libcanberra-gtk3-module libnss3 libdbus-glib-1-2 openjdk-19-jdk curl jq

#ENV DISPLAY=$DISPLAY

# Burp installation
RUN wget -O burpsuite_community_linux_v2023_7_1.sh 'https://portswigger-cdn.net/burp/releases/download?product=community&version=2023.7.1&type=Linux' &&\
	chmod +x burpsuite_community_linux_v2023_7_1.sh &&\
	(echo -ne '\n'; echo '/opt/BurpSuiteCommunity/'; echo 'n') | ./burpsuite_community_linux_v2023_7_1.sh -c

# Driver for firefox and selenium
RUN wget -O geckodriver-v0.33.0-linux64.tar.gz 'https://github.com/mozilla/geckodriver/releases/download/v0.33.0/geckodriver-v0.33.0-linux64.tar.gz' &&\
	tar xvf geckodriver-v0.33.0-linux64.tar.gz &&\
	chmod +x geckodriver &&\
	mv geckodriver /root/

# Firefox installation
RUN wget -O firefox.tar.bz2 'https://download-installer.cdn.mozilla.net/pub/firefox/releases/115.0.3/linux-x86_64/en-US/firefox-115.0.3.tar.bz2' &&\
	tar xvf firefox.tar.bz2 -C /opt/ &&\
	ln -s /opt/firefox/firefox /usr/bin/firefox

# Set environment variable to run Firefox in headless mode
ENV MOZ_HEADLESS=1

# Copy burp config
COPY ./config/burp/project-options.json /opt/BurpSuiteCommunity/
COPY ./config/burp/user-options.json /opt/BurpSuiteCommunity/

# Preconfigure BurpSuite
# TO ENABLE DEBUGGER, COMMENT THIS
#RUN yes | /opt/BurpSuiteCommunity/BurpSuiteCommunity --user-config-file=user-options.json --config-file=project-options.json

# magic to avoid Docker caching the file even if they change
ADD "https://www.random.org/cgi-bin/randbyte?nbytes=10&format=h" skipcache

# Copy mig-t plugin into root
COPY ./mig-t-beta-jar-with-dependencies.jar /root/

# Copy mig-t configuration into home
COPY ./config/mig-t/config.json /

# Start configuration in headless mode
# To disable headless mode remove -Djava.awt.headless=true
CMD ["sh", "-c", "echo 'y' | java -Djava.awt.headless=true -jar \
/opt/BurpSuiteCommunity/burpsuite_community.jar \
--user-config-file=/opt/BurpSuiteCommunity/user-options.json \
--config-file=/opt/BurpSuiteCommunity/project-options.json"]