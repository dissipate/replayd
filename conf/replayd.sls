docker.packages:
  pkg.installed:
    - refresh: true
    - order: 1
    - pkgs:
      - apt-transport-https
      - ca-certificates
      - curl
      - software-properties-common

Run install_docker:
  cmd.run:
   - order: 2
   - name: /opt/replayd/bin/install_docker.sh

Get docker_compose:
  cmd.run:
    - order: 3
    - name: curl -L https://github.com/docker/compose/releases/download/1.27.4/docker-compose-Linux-x86_64 -o /usr/local/bin/docker-compose && chmod +x /usr/local/bin/docker-compose
    - creates: /usr/local/bin/docker-compose

/etc/systemd/system/docker-compose@replayd.service:
  file.managed:
    - order: 4
    - source:
      - '/opt/replayd/conf/docker-compose@replayd.service'

docker-compose@replayd.service:
  service.running:
    - order: 5
    - reload: True
