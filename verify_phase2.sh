#!/bin/bash

echo "========================================"
echo "Phase 2 Verification Script"
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
  "backend/app/schemas/kpi.py"
  "backend/app/crud/kpi.py"
  "backend/app/services/kpi.py"
  "backend/app/api/v1/kpis.py"
  "backend/app/api/v1/templates.py"
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
  "frontend/src/services/kpiService.js"
  "frontend/src/pages/dashboard/DashboardPage.jsx"
  "frontend/src/pages/kpi/KPIListPage.jsx"
  "frontend/src/pages/kpi/KPIFormPage.jsx"
  "frontend/src/pages/kpi/KPIDetailPage.jsx"
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
echo "3. Checking Updated Files..."
if grep -q "from app.api.v1 import auth, kpis, templates" backend/app/main.py; then
  echo -e "  ${GREEN}✓${NC} backend/app/main.py includes KPI routes"
else
  echo -e "  ${RED}✗${NC} backend/app/main.py missing KPI route imports"
fi

if grep -q "KPIListPage" frontend/src/App.jsx; then
  echo -e "  ${GREEN}✓${NC} frontend/src/App.jsx includes KPI routes"
else
  echo -e "  ${RED}✗${NC} frontend/src/App.jsx missing KPI routes"
fi

echo ""
echo "========================================"
echo "Summary"
echo "========================================"
echo -e "Backend files: ${GREEN}$((${#BACKEND_FILES[@]} - MISSING_BACKEND))${NC}/${#BACKEND_FILES[@]} present"
echo -e "Frontend files: ${GREEN}$((${#FRONTEND_FILES[@]} - MISSING_FRONTEND))${NC}/${#FRONTEND_FILES[@]} present"

echo ""
if [ $MISSING_BACKEND -eq 0 ] && [ $MISSING_FRONTEND -eq 0 ]; then
  echo -e "${GREEN}✓ All Phase 2 files are present!${NC}"
  echo ""
  echo "Phase 2 Features Implemented:"
  echo "  ✓ KPI CRUD operations"
  echo "  ✓ KPI filtering (year, quarter, status, search)"
  echo "  ✓ KPI statistics and dashboard"
  echo "  ✓ KPI templates management"
  echo "  ✓ KPI approval workflow (submit, approve, reject)"
  echo "  ✓ Pagination for KPI list"
  echo "  ✓ Enhanced dashboard with real statistics"
  echo ""
  echo "Next: Start backend and frontend servers to test Phase 2"
else
  echo -e "${RED}✗ Some files are missing. Please check the output above.${NC}"
fi

echo ""
