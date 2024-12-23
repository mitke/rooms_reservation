#!/bin/bash

systemctl restart roomRez.socket
systemctl restart roomRez.service
systemctl restart nginx

