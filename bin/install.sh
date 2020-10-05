#!/usr/bin/bash
curl -L https://bootstrap.saltstack.com -o /opt/replayd/bin/bootstrap_salt.sh
sh /opt/replayd/bin/bootstrap_salt.sh

mkdir -p /srv/salt
cp /opt/replayd/conf/top.sls /srv/salt/top.sls
cp /opt/replayd/conf/replayd.sls /srv/salt/replayd.sls

salt-call --local state.apply
