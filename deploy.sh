#!/bin/bash

# Exchron Backend Deployment Script
# Usage: ./deploy.sh [build|start|stop|restart|logs|status]

set -e

PROJECT_NAME="exchron-backend"
CONTAINER_NAME="exchron-api"

case "$1" in
    "build")
        echo "Building $PROJECT_NAME..."
        docker compose build --no-cache
        echo "Build completed!"
        ;;
    "start")
        echo "Starting $PROJECT_NAME..."
        docker compose up -d
        echo "Started! API available at http://localhost:8000"
        echo "Health check: curl http://localhost:8000/health"
        ;;
    "stop")
        echo "Stopping $PROJECT_NAME..."
        docker compose down
        echo "Stopped!"
        ;;
    "restart")
        echo "Restarting $PROJECT_NAME..."
        docker compose down
        docker compose up -d
        echo "Restarted! API available at http://localhost:8000"
        ;;
    "logs")
        echo "Showing logs for $PROJECT_NAME..."
        docker compose logs -f
        ;;
    "status")
        echo "Status of $PROJECT_NAME:"
        docker compose ps
        echo ""
        echo "Health check:"
        curl -s http://localhost:8000/health | python3 -m json.tool || echo "API not responding"
        ;;
    "update")
        echo "Updating $PROJECT_NAME..."
        docker compose down
        docker compose build --no-cache
        docker compose up -d
        echo "Updated and restarted!"
        ;;
    "clean")
        echo "Cleaning up Docker resources..."
        docker compose down
        docker system prune -f
        echo "Cleanup completed!"
        ;;
    *)
        echo "Exchron Backend Deployment Script"
        echo ""
        echo "Usage: $0 [command]"
        echo ""
        echo "Commands:"
        echo "  build    - Build the Docker image"
        echo "  start    - Start the application"
        echo "  stop     - Stop the application"
        echo "  restart  - Restart the application"
        echo "  logs     - Show application logs"
        echo "  status   - Show application status and health"
        echo "  update   - Update and restart the application"
        echo "  clean    - Clean up Docker resources"
        echo ""
        echo "Examples:"
        echo "  $0 build"
        echo "  $0 start"
        echo "  $0 logs"
        exit 1
        ;;
esac