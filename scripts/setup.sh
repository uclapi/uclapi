apt-get update

apt-get -y install git curl libpq-dev libpq5 libpython3-dev \
    python3 python3-pip python3-virtualenv python-virtualenv \
    unzip virtualenv libaio1 build-essential libpcre3 \
    libpcre3-dev wget sed

# Oracle Version
ORACLE_VERSION=12_2
ORACLE_SO_VERSION=12.1

# Oracle Instant Client download links
ORACLE_INSTANTCLIENT_BASIC_URL=https://s3.eu-west-2.amazonaws.com/uclapi-static/instantclient-basic-linux.x64-12.2.0.1.0.zip
ORACLE_INSTANTCLIENT_SDK_URL=https://s3.eu-west-2.amazonaws.com/uclapi-static/instantclient-sdk-linux.x64-12.2.0.1.0.zip

mkdir /opt/oracle

rm -rf /opt/oracle/instantclient_$ORACLE_VERSION

wget -O instantclient.zip "$ORACLE_INSTANTCLIENT_BASIC_URL"
wget -O instantclientsdk.zip "$ORACLE_INSTANTCLIENT_SDK_URL"

unzip -d/opt/oracle instantclient.zip
unzip -d/opt/oracle instantclientsdk.zip

export ORACLE_HOME=/opt/oracle/instantclient_$ORACLE_VERSION

pushd $ORACLE_HOME

ln -s libclntsh.so.$ORACLE_SO_VERSION libclntsh.so
ln -s libocci.so.$ORACLE_SO_VERSION libocci.so
ln -s libclntshcore.so.$ORACLE_SO_VERSION libclntshcore.so

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$ORACLE_HOME
ldconfig

# Add ORACLE_HOME to /etc/environment
grep -q -F "ORACLE_HOME=/opt/oracle/instantclient_$ORACLE_VERSION" /etc/environment || echo "ORACLE_HOME=/opt/oracle/instantclient_$ORACLE_VERSION" >> /etc/environment

# Add ld path to /etc/ld.so.conf.d
echo "/opt/oracle/instantclient_$ORACLE_VERSION" > /etc/ld.so.conf.d/oracle.conf
ldconfig

popd