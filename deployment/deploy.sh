#!/bin/bash
# Quick deployment script that handles docker group permissions
# This script runs docker commands with the docker group activated

set -e

echo "🚀 KPI Management System - Deployment Script"
echo "=============================================="
echo ""

# Check if running from deployment directory
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Error: Please run this script from the deployment/ directory"
    echo "   cd /home/haint/Documents/bsv-okr-kpi/deployment/"
    exit 1
fi

# Check if .env symlink exists
if [ ! -L ".env" ]; then
    echo "⚠️  Warning: .env symlink not found"
    echo "   Creating symlink to ../backend/.env"
    ln -sf ../backend/.env .env
    echo "✅ Symlink created"
fi

echo "📋 Checking configuration..."
sg docker -c "docker compose config > /dev/null 2>&1" && echo "✅ Configuration valid" || {
    echo "❌ Configuration error"
    exit 1
}

echo ""
echo "🐳 Starting Docker containers..."
sg docker -c "docker compose up -d --build"

echo ""
echo "⏳ Waiting for services to be healthy..."
sleep 5

echo ""
echo "📊 Container status:"
sg docker -c "docker compose ps"

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📍 Access points:"
echo "   Frontend:  http://localhost"
echo "   Backend:   http://localhost:8000"
echo "   API Docs:  http://localhost:8000/docs"
echo ""
echo "📝 Next steps:"
echo "   1. Initialize database (first time only):"
echo "      ./deploy.sh init"
echo ""
echo "   2. Create admin user (first time only):"
echo "      ./deploy.sh admin"
echo ""
echo "   3. View logs:"
echo "      ./deploy.sh logs"
echo ""
}

# Handle subcommands
case "${1:-up}" in
    up|start)
        deploy
        ;;

    init)
        echo "🗄️  Initializing database..."
        sg docker -c "docker compose exec backend python scripts/init_db.py"
        echo "✅ Database initialized"
        ;;

    admin)
        echo "👤 Creating admin user..."
        echo ""
        read -p "Admin email [admin@company.com]: " email
        email=${email:-admin@company.com}

        read -p "Admin full name [System Administrator]: " fullname
        fullname=${fullname:-System Administrator}

        read -sp "Admin password: " password
        echo ""

        if [ -z "$password" ]; then
            echo "❌ Password cannot be empty"
            exit 1
        fi

        sg docker -c "docker compose exec backend python scripts/create_admin.py \
            --email \"$email\" \
            --password \"$password\" \
            --fullname \"$fullname\""
        echo "✅ Admin user created"
        ;;

    logs)
        echo "📜 Viewing logs (Ctrl+C to exit)..."
        sg docker -c "docker compose logs -f ${2:-}"
        ;;

    stop)
        echo "🛑 Stopping containers..."
        sg docker -c "docker compose down"
        echo "✅ Containers stopped"
        ;;

    restart)
        echo "🔄 Restarting containers..."
        sg docker -c "docker compose restart ${2:-}"
        echo "✅ Containers restarted"
        ;;

    ps|status)
        echo "📊 Container status:"
        sg docker -c "docker compose ps"
        ;;

    shell)
        service=${2:-backend}
        echo "🐚 Opening shell in $service container..."
        sg docker -c "docker compose exec $service bash"
        ;;

    backup)
        echo "💾 Creating backup..."
        sg docker -c "docker compose exec backend python scripts/backup.py"
        echo "✅ Backup created"
        ;;

    clean)
        echo "🧹 Cleaning up (removing containers and volumes)..."
        read -p "Are you sure? This will delete all data! (yes/no): " confirm
        if [ "$confirm" = "yes" ]; then
            sg docker -c "docker compose down -v"
            echo "✅ Cleanup complete"
        else
            echo "❌ Cleanup cancelled"
        fi
        ;;

    help|--help|-h)
        echo "KPI Management System - Deployment Script"
        echo ""
        echo "Usage: ./deploy.sh [command] [options]"
        echo ""
        echo "Commands:"
        echo "  up, start        Start/deploy the application (default)"
        echo "  init             Initialize database (first time only)"
        echo "  admin            Create admin user (first time only)"
        echo "  logs [service]   View logs (optional: backend/frontend)"
        echo "  stop             Stop all containers"
        echo "  restart [service] Restart containers (optional: specific service)"
        echo "  ps, status       Show container status"
        echo "  shell [service]  Open shell in container (default: backend)"
        echo "  backup           Create database backup"
        echo "  clean            Remove containers and volumes (DANGEROUS)"
        echo "  help             Show this help message"
        echo ""
        echo "Examples:"
        echo "  ./deploy.sh              # Deploy application"
        echo "  ./deploy.sh init         # Initialize database"
        echo "  ./deploy.sh admin        # Create admin user"
        echo "  ./deploy.sh logs         # View all logs"
        echo "  ./deploy.sh logs backend # View backend logs only"
        echo "  ./deploy.sh shell        # Shell into backend"
        echo "  ./deploy.sh stop         # Stop application"
        ;;

    *)
        echo "❌ Unknown command: $1"
        echo "Run './deploy.sh help' for usage information"
        exit 1
        ;;
esac
