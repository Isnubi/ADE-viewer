# Introduction

This is a project to get quicker the current and the next classes of my school calendar.

## How to use

1. Create a docker compose file with the following content:

```yaml
services:
  app:
    image: ghcr.io/isnubi/ade-viewer:latest
    ports:
      - 5000:5000
    environment:
      - ADE_URL=https://ade.example.com
      - TZ=Europe/Paris
      - TIME_DELTA=0
    volumes:
      - /etc/localtime:/etc/localtime
    restart: unless-stopped
```

2. Run the following command:

```bash
docker-compose up -d
```

3. Open your browser and go to `http://localhost:5000`

## Configuration

- `ADE_URL`: The URL of your ics ADE export
- `TZ`: The timezone of your calendar
- `TIME_DELTA`: The number of hours you want to add to the current timezone

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

