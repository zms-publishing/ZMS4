FROM ubuntu:16.04
RUN apt-get update

EXPOSE 8080
EXPOSE 5678

# Install Zope/ZEO Dependencies
RUN apt-get install -y python2.7
RUN apt-get install -y python-pip 
RUN apt-get install -y python-minimal 
RUN apt-get install -y python-dev 
RUN apt-get install -y python-setuptools 
RUN apt-get install -y python-virtualenv
RUN apt-get install -y make \
	gcc \ 
	g++ \
	git \
	curl \
	bash \
	zlib1g-dev\ 
	libbz2-dev \
	libffi-dev \
	libjpeg62-dev \
	libsasl2-dev \
	libxml2-dev \
	libxslt-dev \
	libxslt1-dev \
	libssl-dev \
	libldap2-dev \
	libreadline-dev \
	libsqlite3-dev
RUN apt-get install -y mariadb-server 
# Install slapd and ldap-utils without prompting for password
RUN echo "slapd slapd/internal/generated_adminpw password password" | debconf-set-selections && \
	echo "slapd slapd/internal/adminpw password password" | debconf-set-selections && \
	echo "slapd slapd/password2 password password" | debconf-set-selections && \
	echo "slapd slapd/password1 password password" | debconf-set-selections && \
	echo "slapd slapd/dump_database_destdir string /var/backups/slapd-VERSION" | debconf-set-selections && \
	echo "slapd slapd/domain string example.com" | debconf-set-selections && \
	echo "slapd shared/organization string Example Inc." | debconf-set-selections && \
	apt-get update && \
	apt-get install -y slapd ldap-utils && \
	rm -rf /var/lib/apt/lists/*

RUN python2 -m pip install pip==20.3

RUN adduser --disabled-password zope && usermod -aG sudo zope

USER zope
ENV VIRTUAL_ENV=/home/zope/venv
RUN virtualenv --python=python2  $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
WORKDIR /home/zope/venv
RUN pip install -r https://zopefoundation.github.io/Zope/releases/2.13.29/requirements.txt
RUN pip install --no-deps -e git+https://github.com/zms-publishing/ZMS4.git@fb_docker_pips#egg=ZMS
# RUN ./pip install Products.CMFCore==2.3.0
RUN pip install Pillow==6.2.2
RUN pip install python-ldap==3.3.1
RUN pip install Products.LDAPUserFolder==2.27
RUN pip install xhtml2pdf==0.2.4
RUN pip install Products.ZSQLMethods==2.13.5
RUN pip install Products.ZSQLiteDA==0.6.1
RUN pip install debugpy
RUN pip install pudb==2019.2

# # Create Zope Instance
RUN mkzopeinstance -d /home/zope/venv/instance/zms4 -u admin:admin

# COPY ./var venv/instance/zms4/var

# Finally Start Zope by Script
# ENTRYPOINT ["/bin/sh -c"]
# CMD ["/home/zope/venv/instance/zms4/bin/zopectl","fg"]
# CMD ["/home/zope/venv/instance/zms4/bin/runzope","-X","debug-mode=on"]