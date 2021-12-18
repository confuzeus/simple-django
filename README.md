# Simple Django Project Template

This template contains everything you need to bootstrap a new Django project.

## Usage guide

1. Make a copy of *.env_sample* named as *.env*. Edit contents as required.
2. Build the *piptools* image and run `docker-compose --profile debug run piptools compile` to compile requirements.
3. Build everything with `docker-compose --profile debug build`.
4. Build static assets with `docker-compose --profile debug run node npm run build`.
5. Run the whole stack with `docker-compose --profile debug up`.