# Local Docker Setup Guide

This guide will walk you through setting up and running the Exoplanet Classification API locally using Docker.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Docker Desktop** (Windows/Mac) or **Docker Engine** (Linux)
  - Download from: https://www.docker.com/products/docker-desktop/
  - Minimum version: Docker 20.10+ and Docker Compose 1.29+
- **Git** (to clone the repository if needed)

### Verify Docker Installation

Open your terminal/command prompt and run:

```cmd
docker --version
docker-compose --version
```

You should see version information for both commands.

## Quick Start (Recommended)

### Option 1: Using Docker Compose (Recommended)

1. **Navigate to the project directory:**
   ```cmd
   cd C:\Users\navid\Desktop\Figma\exchron-backend
   ```

2. **Build and start the container:**
   ```cmd
   docker-compose up --build
   ```

3. **Access the API:**
   - API Documentation: http://localhost:8000/docs
   - API Status: http://localhost:8000/health
   - Welcome Message: http://localhost:8000/

4. **Stop the container:**
   ```cmd
   docker-compose down
   ```

### Option 2: Using Docker Commands

1. **Navigate to the project directory:**
   ```cmd
   cd C:\Users\navid\Desktop\Figma\exchron-backend
   ```

2. **Build the Docker image:**
   ```cmd
   docker build -t exchron-api .
   ```

3. **Run the container:**
   ```cmd
   docker run -d -p 8000:8000 --name exchron-container exchron-api
   ```

4. **View logs:**
   ```cmd
   docker logs exchron-container
   ```

5. **Stop and remove the container:**
   ```cmd
   docker stop exchron-container
   docker rm exchron-container
   ```

## Detailed Setup Instructions

### Step 1: Verify Project Structure

Ensure your project directory contains these essential files:
```
exchron-backend/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── app/
│   ├── main.py
│   └── ...
├── data/
│   └── ...
├── models/
│   └── ...
└── README.md
```

### Step 2: Environment Configuration

The Docker setup uses the following default configuration:
- **Port**: 8000 (mapped to host port 8000)
- **Environment**: Production-ready with health checks
- **User**: Non-root user for security
- **Working Directory**: `/app`

### Step 3: Build and Run Options

#### Development Mode (with live reload)
For development with automatic code reloading:

```cmd
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build
```

*Note: You'll need to create `docker-compose.dev.yml` for this to work.*

#### Production Mode (default)
For production deployment:

```cmd
docker-compose up -d --build
```

The `-d` flag runs containers in detached mode (background).

## Configuration Options

### Port Mapping

To run on a different port, modify the port mapping:

```cmd
# Run on port 3001 instead of 8000
docker run -d -p 3001:8000 --name exchron-container exchron-api
```

Or update `docker-compose.yml`:
```yaml
ports:
  - "3001:8000"  # host:container
```

### Volume Mounts (Optional)

To persist data or enable live development, uncomment volume mounts in `docker-compose.yml`:

```yaml
volumes:
  - ./data:/app/data:ro          # Read-only data mount
  - ./models:/app/models:ro      # Read-only models mount
  - ./logs:/app/logs             # Persistent logs
```

### Resource Limits (Optional)

For production environments, uncomment resource limits in `docker-compose.yml`:

```yaml
deploy:
  resources:
    limits:
      cpus: '2.0'
      memory: 4G
    reservations:
      cpus: '1.0'
      memory: 2G
```

## Testing the Docker Setup

### 1. Health Check

Verify the API is running:
```cmd
curl http://localhost:8000/health
```

Expected response:
```json
{"status": "healthy", "timestamp": "2025-10-08T...", "version": "2.0"}
```

### 2. API Documentation

Visit http://localhost:8000/docs to access the interactive Swagger UI.

### 3. Test Predictions

#### Deep Learning Model:
```cmd
curl -X POST "http://localhost:8000/api/dl/predict" ^
     -H "Content-Type: application/json" ^
     -d "{\"model\": \"cnn\", \"kepid\": \"123456\", \"predict\": true}"
```

#### Machine Learning Model:
```cmd
curl -X POST "http://localhost:8000/api/ml/predict" ^
     -H "Content-Type: application/json" ^
     -d "{\"model\": \"gb\", \"datasource\": \"pre-loaded\", \"data\": \"kepler\", \"predict\": true}"
```

## Docker Management Commands

### View Running Containers
```cmd
docker ps
```

### View All Containers
```cmd
docker ps -a
```

### View Container Logs
```cmd
# Using docker-compose
docker-compose logs -f

# Using docker command
docker logs -f exchron-container
```

### Enter Container Shell (for debugging)
```cmd
# Using docker-compose
docker-compose exec exchron-backend bash

# Using docker command
docker exec -it exchron-container bash
```

### Clean Up

#### Remove Containers and Images
```cmd
# Stop and remove containers
docker-compose down

# Remove images
docker rmi exchron-api

# Remove all unused containers, images, and networks
docker system prune -f
```

#### Complete Cleanup
```cmd
# Remove everything (use with caution)
docker system prune -a -f --volumes
```

## Troubleshooting

### Common Issues

#### 1. Port Already in Use
```
Error: bind: address already in use
```

**Solution:** Change the port mapping or stop the service using port 8000:
```cmd
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F

# Or use a different port
docker run -p 8001:8000 exchron-api
```

#### 2. Build Failures
```
Error: failed to build
```

**Solutions:**
- Check Docker is running: `docker info`
- Verify Dockerfile syntax
- Ensure all required files exist
- Clear Docker cache: `docker builder prune`

#### 3. Container Exits Immediately
```cmd
# Check exit reason
docker logs exchron-container

# Common causes:
# - Missing dependencies in requirements.txt
# - Python import errors
# - Missing model files
```

#### 4. Health Check Failures

Check the health status:
```cmd
docker inspect --format='{{json .State.Health}}' exchron-container
```

### Performance Optimization

#### 1. Multi-stage Builds
The current Dockerfile uses a single stage. For production, consider multi-stage builds to reduce image size.

#### 2. Layer Caching
The Dockerfile is optimized for layer caching by copying `requirements.txt` first.

#### 3. Memory Usage
Monitor memory usage:
```cmd
docker stats exchron-container
```

## Security Considerations

1. **Non-root User**: The container runs as a non-root user (`appuser`)
2. **Read-only Mounts**: Data and model volumes should be mounted as read-only
3. **Network Security**: Only expose necessary ports
4. **Image Scanning**: Regularly scan images for vulnerabilities

## Integration with CI/CD

### Docker Hub Deployment
```cmd
# Tag image
docker tag exchron-api username/exchron-api:latest

# Push to Docker Hub
docker push username/exchron-api:latest
```

### Production Deployment
```cmd
# Pull and run production image
docker run -d -p 8000:8000 --restart unless-stopped username/exchron-api:latest
```

## Next Steps

After successfully running the API locally with Docker:

1. **Frontend Integration**: Connect your frontend application to `http://localhost:8000`
2. **API Testing**: Use the interactive docs at `http://localhost:8000/docs`
3. **Model Validation**: Test with real data using the provided endpoints
4. **Monitoring**: Set up logging and monitoring for production deployment

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [FastAPI with Docker](https://fastapi.tiangolo.com/deployment/docker/)
- [Python Docker Best Practices](https://pythonspeed.com/docker/)

---

**Need help?** Check the main [README.md](README.md) for API usage examples and troubleshooting tips.