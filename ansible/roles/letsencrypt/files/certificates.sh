#!/bin/bash

certbot certonly -n \
  -m me@example.com \
  --agree-tos \
  --dns-cloudflare \
  --dns-cloudflare-credentials /root/cloudflare.ini \
  -d example.com
