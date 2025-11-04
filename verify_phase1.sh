#!/bin/bash

echo "========================================"
echo "Phase 1 Verification Script"
echo "========================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check backend files
echo "1. Checking Backend Files..."
BACKEND_FILES=(
  "backend/app/main.py"
  "backend/app/config.py"
  "backend/app/database.py"
  "backend/app/models/user.py"
  "backend/app/models/kpi.py"
  "backend/app/schemas/user.py"
  "backend/app/schemas/auth.py"
  "backend/app/crud/user.py"
  "backend/app/services/auth.py"
  "backend/app/api/deps.py"
  "backend/app/api/v1/auth.py"
  "backend/app/utils/security.py"
  "backend/scripts/create_admin.py"
  "backend/scripts/init_db.py"
  "backend/requirements.txt"
  "backend/.env.example"
)

MISSING_BACKEND=0
for file in "${BACKEND_FILES[@]}"; do
  if [ -f "$file" ]; then
    echo -e "  ${GREEN}✓${NC} $file"
  else
    echo -e "  ${RED}✗${NC} $file (MISSING)"
    MISSING_BACKEND=$((MISSING_BACKEND + 1))
  fi
done

echo ""
echo "2. Checking Frontend Files..."
FRONTEND_FILES=(
  "frontend/index.html"
  "frontend/src/main.jsx"
  "frontend/src/App.jsx"
  "frontend/src/index.css"
  "frontend/src/contexts/AuthContext.jsx"
  "frontend/src/hooks/useAuth.js"
  "frontend/src/services/api.js"
  "frontend/src/services/authService.js"
  "frontend/src/components/auth/ProtectedRoute.jsx"
  "frontend/src/components/layout/Header.jsx"
  "frontend/src/components/layout/Sidebar.jsx"
  "frontend/src/components/layout/MainLayout.jsx"
  "frontend/src/pages/auth/LoginPage.jsx"
  "frontend/src/pages/dashboard/DashboardPage.jsx"
  "frontend/package.json"
  "frontend/.env.example"
)

MISSING_FRONTEND=0
for file in "${FRONTEND_FILES[@]}"; do
  if [ -f "$file" ]; then
    echo -e "  ${GREEN}✓${NC} $file"
  else
    echo -e "  ${RED}✗${NC} $file (MISSING)"
    MISSING_FRONTEND=$((MISSING_FRONTEND + 1))
  fi
done

echo ""
echo "3. Checking Environment Files..."
if [ -f "backend/.env" ]; then
  echo -e "  ${GREEN}✓${NC} backend/.env exists"
else
  echo -e "  ${YELLOW}⚠${NC} backend/.env not found. Run: cp backend/.env.example backend/.env"
fi

if [ -f "frontend/.env" ]; then
  echo -e "  ${GREEN}✓${NC} frontend/.env exists"
else
  echo -e "  ${YELLOW}⚠${NC} frontend/.env not found. Run: cp frontend/.env.example frontend/.env"
fi

echo ""
echo "4. Checking Python Virtual Environment..."
if [ -d "backend/venv" ]; then
  echo -e "  ${GREEN}✓${NC} backend/venv exists"
else
  echo -e "  ${YELLOW}⚠${NC} backend/venv not found. Run: cd backend && python -m venv venv"
fi

echo ""
echo "5. Checking Node Modules..."
if [ -d "frontend/node_modules" ]; then
  echo -e "  ${GREEN}✓${NC} frontend/node_modules exists"
else
  echo -e "  ${YELLOW}⚠${NC} frontend/node_modules not found. Run: cd frontend && npm install"
fi

echo ""
echo "========================================"
echo "Summary"
echo "========================================"
echo -e "Backend files: ${GREEN}$((${#BACKEND_FILES[@]} - MISSING_BACKEND))${NC}/${#BACKEND_FILES[@]} present"
echo -e "Frontend files: ${GREEN}$((${#FRONTEND_FILES[@]} - MISSING_FRONTEND))${NC}/${#FRONTEND_FILES[@]} present"

echo ""
if [ $MISSING_BACKEND -eq 0 ] && [ $MISSING_FRONTEND -eq 0 ]; then
  echo -e "${GREEN}✓ All Phase 1 files are present!${NC}"
  echo ""
  echo "Next steps:"
  echo "1. Setup backend: cd backend && cp .env.example .env"
  echo "2. Edit backend/.env and set SECRET_KEY"
  echo "3. Setup frontend: cd frontend && cp .env.example .env"
  echo "4. Follow instructions in PHASE1_COMPLETE.md"
else
  echo -e "${RED}✗ Some files are missing. Please check the output above.${NC}"
fi

echo ""
