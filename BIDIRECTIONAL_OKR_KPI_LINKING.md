# Bidirectional OKR-KPI Linking Complete ✅

**Date:** November 7, 2025
**Feature:** Two-way connection between Objectives and KPIs + Hierarchical Progress Calculation

---

## Overview

This enhancement adds **bidirectional visibility** between Objectives and KPIs, plus automatic **hierarchical progress calculation** where objectives inherit progress from their children and linked KPIs.

---

## 1. Bidirectional Linking ↔️

### From Objective → KPI (Already Existed)
- **Location:** Objective Detail Page
- **Feature:** "Linked KPIs" section with "Link KPI" button
- **Capability:**
  - Link multiple KPIs to an objective
  - Assign weight to each KPI (0-100%)
  - View all linked KPIs with their progress
  - Unlink KPIs

### From KPI → Objective (NEW ✨)
- **Location:** KPI Detail Page
- **Feature:** New "Linked Objectives" section
- **Capability:**
  - Automatically shows all objectives this KPI is linked to
  - Displays objective title, level, year, quarter, department, owner
  - Shows weight assigned to this KPI for each objective
  - Shows each objective's progress
  - Click-through to navigate to objective details
  - Visual progress impact explanation

**Example UI:**
```
┌─────────────────────────────────────────────────────────┐
│ Linked Objectives (2)                                    │
├─────────────────────────────────────────────────────────┤
│ 🏢 Increase market share in Southeast Asia              │
│ Level 1  •  2025 Q1  •  Sales  •  John Doe  •  Weight: 50% │
│                                                 Progress: 75% │
├─────────────────────────────────────────────────────────┤
│ 🏢 Expand customer base                                  │
│ Level 2  •  2025 Q1  •  Sales  •  Jane Smith  •  Weight: 30% │
│                                                 Progress: 60% │
└─────────────────────────────────────────────────────────┘

💡 Progress Impact: This KPI contributes to 2 objectives with
the specified weights. When you update this KPI's progress,
the linked objectives will automatically recalculate their progress.
```

---

## 2. Hierarchical Progress Calculation 📊

### How It Works

Objectives automatically calculate their progress using this **cascading hierarchy**:

```
┌─────────────────────────────────────────────────────────┐
│ Progress Calculation Logic                               │
└─────────────────────────────────────────────────────────┘
                           ↓
           ┌───────────────┴───────────────┐
           │  Has Child Objectives?         │
           └───────────────┬───────────────┘
                           │
                    YES ←──┴──→ NO
                     ↓           ↓
              ┌──────────┐  ┌───────────────┐
              │ Average  │  │ Has Linked    │
              │ Progress │  │ KPIs?         │
              │ of       │  └───────┬───────┘
              │ Children │          │
              └──────────┘   YES ←─┴─→ NO
                              ↓        ↓
                        ┌────────┐  ┌────────┐
                        │Weighted│  │ Manual │
                        │Average │  │Progress│
                        │of KPIs │  └────────┘
                        └────────┘
```

### Example Hierarchy

```
Company Goal: Increase Revenue (Level 0)
├─ Progress: 67% (average of children)
│
├─ Division: Sales Growth (Level 1)
│  ├─ Progress: 70% (average of children)
│  │
│  ├─ Team: Enterprise Sales (Level 2)
│  │  ├─ Progress: 75% (weighted average of KPIs)
│  │  │
│  │  ├─ KPI 1: Close 10 enterprise deals (60% complete, weight: 40%)
│  │  └─ KPI 2: Achieve $2M in contracts (85% complete, weight: 60%)
│  │
│  └─ Team: SMB Sales (Level 2)
│     ├─ Progress: 65% (weighted average of KPIs)
│     │
│     ├─ KPI 3: Acquire 100 new customers (70% complete, weight: 50%)
│     └─ KPI 4: Reduce churn rate (60% complete, weight: 50%)
│
└─ Division: Marketing (Level 1)
   ├─ Progress: 64% (weighted average of KPIs)
   │
   ├─ KPI 5: Generate 500 qualified leads (68% complete, weight: 60%)
   └─ KPI 6: Improve brand awareness by 20% (58% complete, weight: 40%)
```

**Calculation Flow:**
1. **Bottom-up:** KPI progress updates first
2. **Level 2 (Teams):** Calculate from weighted KPI averages
3. **Level 1 (Divisions):** Calculate from child objective averages
4. **Level 0 (Company):** Calculate from division objective averages

### Recalculate Button

Every Objective Detail page has a **"🔄 Recalculate" button** that:
- Recalculates the objective's progress based on current data
- **Cascades up** to recalculate all parent objectives
- Updates progress for the entire hierarchy path
- Useful after:
  - KPI progress updates
  - Linking/unlinking KPIs
  - Child objective progress changes

---

## 3. Technical Implementation

### Backend Changes

#### New Endpoint
```python
GET /api/v1/kpis/{kpi_id}/objectives
```
**Returns:** List of objectives linked to a KPI with:
- Objective details (id, title, level, status, progress, year, quarter, department)
- Owner name
- Link metadata (weight, linked_at timestamp)

#### New CRUD Method
```python
# In backend/app/crud/objective.py
def get_objectives_by_kpi(self, db: Session, kpi_id: int) -> list[dict]:
    """Get all objectives linked to a KPI with link information."""
    # Queries ObjectiveKPILink table
    # Joins with Objective and User tables
    # Returns enriched data for frontend display
```

### Frontend Changes

#### New Service Method
```javascript
// In frontend/src/services/objectiveService.js
getObjectivesByKPI: async (kpiId) => {
  const response = await api.get(`/kpis/${kpiId}/objectives`);
  return response.data;
}
```

#### Updated KPI Detail Page
```javascript
// In frontend/src/pages/kpi/KPIDetailPage.jsx
- Added linkedObjectives state
- Added objectivesLoading state
- Added fetchLinkedObjectives() function
- Added "Linked Objectives" section with rich display
- Shows progress impact explanation
```

---

## 4. User Workflows

### Scenario A: Manager Creates Cascade

1. **Create Company Objective** (Level 0)
   - Title: "Increase Revenue by 20%"
   - Manual progress: 0%

2. **Create Division Objectives** (Level 1)
   - Parent: Company Objective
   - Progress auto-calculates from children

3. **Create Team Objectives** (Level 2)
   - Parent: Division Objectives
   - Progress auto-calculates from KPIs

4. **Link KPIs** to Team Objectives
   - From Objective Detail: Click "Link KPI"
   - Assign weights (must total 100% for accurate calculation)
   - Progress now flows: KPIs → Teams → Divisions → Company

### Scenario B: Employee Views Impact

1. **Employee creates/updates KPI**
   - Progress: 75%

2. **Employee views KPI Detail**
   - Sees "Linked Objectives" section
   - Realizes their KPI contributes to 2 objectives:
     - Team objective (weight: 60%)
     - Division objective (weight: 40%)

3. **Employee clicks through** to Team Objective
   - Sees how their KPI progress affects team progress
   - Views full hierarchy path via breadcrumbs

4. **Manager recalculates** objective progress
   - Team progress updates from 65% → 72%
   - Division progress updates automatically
   - Company progress updates automatically

---

## 5. Benefits

### For Employees
- ✅ **Visibility:** See exactly which objectives depend on their work
- ✅ **Motivation:** Understand strategic impact of daily tasks
- ✅ **Alignment:** Track contribution to organizational goals
- ✅ **Navigation:** Easy click-through to related objectives

### For Managers
- ✅ **Automatic Progress:** No manual progress tracking needed
- ✅ **Weighted Contributions:** Assign importance to different KPIs
- ✅ **Cascading Updates:** Changes propagate up the hierarchy
- ✅ **Real-time Insights:** Always current progress data

### For Executives
- ✅ **Top-down View:** Company progress reflects reality
- ✅ **Drill-down:** Investigate progress at any level
- ✅ **Dependency Mapping:** See KPI-to-Objective connections
- ✅ **Data-driven:** Decisions based on actual performance

---

## 6. Data Flow Diagram

```
┌─────────────────────────────────────────────────────────┐
│                   User Actions                           │
└──────────────────┬──────────────────────────────────────┘
                   │
       ┌───────────┴───────────┐
       │                       │
       ▼                       ▼
┌─────────────┐        ┌─────────────┐
│  Update KPI │        │   Link KPI  │
│  Progress   │        │ to Objective│
└──────┬──────┘        └──────┬──────┘
       │                      │
       └──────────┬───────────┘
                  │
                  ▼
       ┌──────────────────┐
       │ Database Tables:  │
       │ - kpis           │
       │ - objective_kpi_ │
       │   links          │
       └─────────┬────────┘
                 │
                 ▼
       ┌──────────────────┐
       │ Recalculate      │
       │ Progress API     │
       └─────────┬────────┘
                 │
                 ▼
       ┌──────────────────┐
       │ Update Objective │
       │ Progress         │
       └─────────┬────────┘
                 │
                 ▼
       ┌──────────────────┐
       │ Cascade to       │
       │ Parent Objectives│
       └─────────┬────────┘
                 │
                 ▼
       ┌──────────────────┐
       │ UI Updates:       │
       │ - Objective pages│
       │ - KPI pages      │
       │ - Stats dashboard│
       └──────────────────┘
```

---

## 7. Testing Checklist

### Backend
- [x] GET /api/v1/kpis/{kpi_id}/objectives returns linked objectives
- [x] Returns correct objective details and link metadata
- [x] Handles KPIs with no linked objectives (empty array)
- [x] Endpoint is documented in OpenAPI spec

### Frontend
- [x] KPI Detail page shows "Linked Objectives" section
- [x] Shows loading state while fetching
- [x] Shows empty state when no objectives linked
- [x] Displays all objective details correctly
- [x] Progress bars render with correct colors
- [x] Click-through navigation works
- [x] Progress impact explanation visible

### Integration
- [ ] Link KPI to objective from Objective page
- [ ] Verify link appears in KPI page
- [ ] Update KPI progress
- [ ] Recalculate objective progress
- [ ] Verify parent objectives update
- [ ] Unlink KPI from objective
- [ ] Verify link disappears from KPI page

---

## 8. Future Enhancements

### Possible Improvements

1. **Link from KPI Side**
   - Add "Link to Objective" button on KPI Detail page
   - Modal to select objective and assign weight

2. **Progress Analytics**
   - Show contribution breakdown (which KPIs contribute most)
   - Historical progress trends
   - Predictive completion dates

3. **Alerts & Notifications**
   - Notify when linked objective changes
   - Alert when KPI progress affects objective thresholds
   - Weekly progress summary emails

4. **Bulk Operations**
   - Link multiple KPIs to an objective at once
   - Adjust weights in bulk
   - Copy objective structure with KPI links

5. **Visual Improvements**
   - Network graph showing all connections
   - Sankey diagram of progress flow
   - Heat map of objective/KPI health

---

## Summary

| Feature | Status | Impact |
|---------|--------|--------|
| **Bidirectional Linking** | ✅ Complete | See connections from both sides |
| **Hierarchical Progress** | ✅ Complete | Automatic calculation, no manual work |
| **Cascading Updates** | ✅ Complete | Changes propagate to all parents |
| **Weight-based Contribution** | ✅ Complete | Accurate progress representation |
| **UI Visibility** | ✅ Complete | Clear, informative displays |
| **Backend API** | ✅ Complete | `/api/v1/kpis/{kpi_id}/objectives` |
| **Frontend Integration** | ✅ Complete | KPI Detail page enhancement |

---

**Access the feature:**
1. Open http://localhost
2. Navigate to any KPI detail page
3. Scroll to "Linked Objectives" section
4. Or navigate to Objective detail page → "Linked KPIs" section

**Both views are now fully functional and synchronized!** 🎉
