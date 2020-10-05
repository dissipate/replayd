#!/bin/bash

# Run when replayd service is running
docker exec -i -t replayd_replayd_1 pytest
