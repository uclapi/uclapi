FROM postgres:11.1

# Set to a British English locale
RUN localedef -i en_GB -c -f UTF-8 -A /usr/share/locale/locale.alias en_GB.UTF-8
ENV LANG en_GB.utf8

# Copy in DDL for Shibboleth
COPY ./shibpostgres/shib.sql /docker-entrypoint-initdb.d/shib.sql
