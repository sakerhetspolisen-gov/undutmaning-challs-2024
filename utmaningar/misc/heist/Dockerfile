FROM fedora:latest

RUN yum update -y && \
    yum groupinstall -y "Development Tools" && \
    yum install -y tmux util-linux ncurses binutils psmisc procps strace python3-pip util-linux gcc-c++ make

# Install pip3 packages
RUN pip3 install --no-cache-dir alive-progress pyfiglet


# Add user
#RUN useradd -ms /bin/bash ctf

# Create a directory for the app
#RUN mkdir -p /home/ctf/app && chown -R ctf:ctf /home/ctf/app
#WORKDIR /home/ctf/app

# Install Node.js deps
COPY package.json ./
#RUN npm install

# Copy app
COPY web-terminal-server.js ./
COPY public /var/www/public

# Copy CTF/script
COPY tmux.conf /home/ctf/.tmux.conf
COPY timer.py /home/ctf/timer.py
COPY secret /home/ctf/secret

#Permissions
RUN chown -R ctf:ctf /home/ctf/
WORKDIR /code
# Exose Web
EXPOSE 3000

# Set entrypoint
#USER ctf
#CMD ["tmux", "capture-pane", "-b", "temp-capture-buffer", "-S -"]
#CMD ["tmux", "capture-pane", "-pS", "-3000", "-t2", ">", "/var/tmp/ctfrd"]
#CMD ["tmux", "attach"]
#CMD ["su", "-", "ctf", "-c", "/bin/bash"]
COPY ./entrypoint.sh .
ENTRYPOINT ["/entrypoint.sh"]
