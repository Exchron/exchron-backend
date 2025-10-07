# Docker Deployment Guide

## Prerequisites

On your Ubuntu server, ensure Docker and Docker Compose are installed:

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo apt install docker-compose-plugin -y

# Add user to docker group (optional, to run without sudo)
sudo usermod -aG docker $USER
# Log out and back in for this to take effect
```

## Deployment Methods

### Method 1: Using Docker Compose (Recommended)

1. Copy your project files to the Ubuntu server
2. Navigate to the project directory
3. Build and run:

```bash
# Build and start the container
docker compose up --build -d

# View logs
docker compose logs -f

# Stop the container
docker compose down
```

### Method 2: Using Docker directly

```bash
# Build the image
docker build -t exchron-backend .

# Run the container
docker run -d \
  --name exchron-api \
  -p 8000:8000 \
  --restart unless-stopped \
  exchron-backend

# View logs
docker logs -f exchron-api

# Stop the container
docker stop exchron-api
docker rm exchron-api
```

### Method 3: With Nginx Reverse Proxy

Create an nginx configuration file `/etc/nginx/sites-available/exchron-api`:

```nginx
server {
    listen 80;
    server_name your-domain.com;  # Replace with your domain

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/exchron-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## Useful Commands

```bash
# Check container status
docker compose ps

# View resource usage
docker stats exchron-api

# Access container shell
docker compose exec exchron-backend bash

# Update deployment
docker compose pull
docker compose up --build -d

# Backup data (if volumes are used)
docker compose exec exchron-backend tar czf /tmp/backup.tar.gz /app/data
docker cp exchron-api:/tmp/backup.tar.gz ./backup.tar.gz
```

## Environment Variables

You can customize the deployment by setting environment variables in a `.env` file:

```env
# .env file
CORS_ORIGINS=http://your-frontend.com,https://your-frontend.com
API_PORT=8000
LOG_LEVEL=info
```

Then modify docker-compose.yml to use env_file:
```yaml
services:
  exchron-backend:
    env_file: .env
```

## SSL/HTTPS Setup with Let's Encrypt

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx -y

# Get SSL certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal is usually set up automatically
sudo crontab -l | grep certbot
```

## Monitoring and Logs

```bash
# Real-time logs
docker compose logs -f

# Log rotation (add to crontab)
echo "0 2 * * * docker system prune -f" | sudo crontab -

# Health check
curl http://localhost:8000/health
```

## Troubleshooting

1. **Container won't start**: Check logs with `docker compose logs`
2. **Permission issues**: Ensure proper file ownership
3. **Port conflicts**: Change port mapping in docker-compose.yml
4. **Memory issues**: Add resource limits in docker-compose.yml
5. **Model loading fails**: Check if model files are properly copied

## Security Considerations

1. Run containers as non-root user (already configured)
2. Use specific version tags instead of `latest`
3. Regularly update base images
4. Use secrets for sensitive data
5. Enable firewall and limit exposed ports
6. Use HTTPS in production