# Phase C: OKR Objectives & Hierarchical Structure 🎯

**Status**: 📋 **PLANNING**
**Priority**: ⭐ **HIGH** - Core feature to complete the OKR system
**Estimated Duration**: 12-15 hours (2-3 days)

---

## 🎯 Overview

Currently, the system only has **KPIs (Key Results)**. This phase adds **Objectives** to create a complete OKR framework with hierarchical goal alignment from company-level down to individual KPIs.

### Current State
```
❌ No objectives layer
✅ KPIs exist (individual key results)
❌ No hierarchical structure
❌ No alignment visualization
```

### Target State
```
✅ Company Goals (Top level)
  └─ Division/Unit Objectives
      └─ Team Objectives
          └─ Individual KPIs (Key Results)

✅ Tree visualization showing hierarchy
✅ Gantt chart for timeline view
✅ Alignment tracking (goals → objectives → KPIs)
```

---

## 🏗️ Architecture Design

### 1. Database Schema

#### New Table: `objectives`

```sql
CREATE TABLE objectives (
    id INTEGER PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,

    -- Hierarchy
    parent_id INTEGER REFERENCES objectives(id),  -- NULL for top-level (company goals)
    level VARCHAR(20) NOT NULL,  -- 'company', 'division', 'team', 'individual'

    -- Ownership
    owner_id INTEGER REFERENCES users(id),
    department VARCHAR(100),

    -- Time period
    year INTEGER NOT NULL,
    quarter VARCHAR(10),  -- NULL for annual objectives
    start_date DATE,
    end_date DATE,

    -- Progress
    status VARCHAR(20) DEFAULT 'active',  -- active, completed, abandoned, on_hold
    progress_percentage FLOAT DEFAULT 0.0,

    -- Metadata
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER REFERENCES users(id),

    INDEX idx_parent (parent_id),
    INDEX idx_owner (owner_id),
    INDEX idx_year_quarter (year, quarter),
    INDEX idx_level (level)
);
```

#### New Table: `objective_kpi_links`

```sql
CREATE TABLE objective_kpi_links (
    id INTEGER PRIMARY KEY,
    objective_id INTEGER REFERENCES objectives(id) ON DELETE CASCADE,
    kpi_id INTEGER REFERENCES kpis(id) ON DELETE CASCADE,
    weight FLOAT DEFAULT 1.0,  -- How much this KPI contributes to objective (0-1)
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    UNIQUE (objective_id, kpi_id),
    INDEX idx_objective (objective_id),
    INDEX idx_kpi (kpi_id)
);
```

#### Modified Table: `kpis`

```sql
-- Add to existing kpis table:
ALTER TABLE kpis ADD COLUMN objective_id INTEGER REFERENCES objectives(id);
-- Note: Keep backward compatibility - objective_id can be NULL for standalone KPIs
```

### 2. Hierarchical Structure Rules

```
Level 0: Company Goals (parent_id = NULL, level = 'company')
  ├─ Level 1: Division/Unit Objectives (level = 'division')
  │   ├─ Level 2: Team Objectives (level = 'team')
  │   │   └─ Level 3: Individual Objectives (level = 'individual')
  │   │       └─ KPIs (Key Results)
```

**Rules**:
- Company goals can have multiple division objectives
- Division objectives can have multiple team objectives
- Team objectives can have multiple individual objectives
- Individual objectives link to KPIs
- KPIs can belong to one or more objectives (via objective_kpi_links)
- Progress rolls up: Objective progress = average of child objectives/KPIs

---

## 📊 Core Features

### Feature 1: Objective Management

#### Backend API Endpoints
```python
# Objectives CRUD
POST   /api/v1/objectives              # Create objective
GET    /api/v1/objectives              # List objectives (with filters)
GET    /api/v1/objectives/{id}         # Get objective details
PUT    /api/v1/objectives/{id}         # Update objective
DELETE /api/v1/objectives/{id}         # Delete objective

# Hierarchy operations
GET    /api/v1/objectives/{id}/children        # Get child objectives
GET    /api/v1/objectives/{id}/ancestors       # Get parent chain
GET    /api/v1/objectives/{id}/tree            # Get full subtree
POST   /api/v1/objectives/{id}/move            # Move to different parent

# KPI linking
POST   /api/v1/objectives/{id}/kpis            # Link KPI to objective
DELETE /api/v1/objectives/{id}/kpis/{kpi_id}   # Unlink KPI
GET    /api/v1/objectives/{id}/kpis            # Get linked KPIs

# Progress calculation
GET    /api/v1/objectives/{id}/progress        # Calculate progress
POST   /api/v1/objectives/{id}/recalculate     # Manually trigger recalculation
```

#### Frontend Pages
1. **Objectives List Page** (`/objectives`)
   - Filterable list (year, quarter, level, department, owner)
   - Search by title/description
   - Quick stats: total, active, completed
   - Create new objective button

2. **Objective Detail Page** (`/objectives/{id}`)
   - Full objective information
   - Parent objective (breadcrumb trail)
   - Child objectives list
   - Linked KPIs list
   - Progress visualization
   - Edit/delete actions
   - Activity timeline

3. **Objective Form** (`/objectives/new`, `/objectives/{id}/edit`)
   - Title, description
   - Level selection (auto-suggested based on user role)
   - Parent objective selector (hierarchical dropdown)
   - Owner assignment
   - Time period (year, quarter, start/end dates)
   - KPI selection and linking
   - Weight assignment for KPIs

---

### Feature 2: Hierarchy Visualization

#### Tree View Component
```
📊 Company Goals (FY 2025)
├─ 💼 Increase Revenue by 30%
│  ├─ 📈 Sales Division: Acquire 50 new customers
│  │  ├─ 👥 Team A: 20 customers in Q1-Q2
│  │  │  └─ 🎯 John's KPI: 5 customers/month
│  │  └─ 👥 Team B: 30 customers in Q3-Q4
│  └─ 🔧 Product Division: Launch 3 new features
│     └─ 👥 Dev Team: Feature X by Q2
│        └─ 🎯 Jane's KPI: Complete 10 tickets/week
└─ 🎓 Improve Customer Satisfaction to 4.5/5
   └─ 💬 Support Division: Reduce response time
      └─ 🎯 Support KPI: <2hr avg response
```

**Features**:
- Expandable/collapsible nodes
- Color-coded by status (active, completed, at-risk)
- Progress bars on each node
- Click to view details
- Drag-and-drop to reorganize (admin only)
- Filter by department/time period

#### Gantt Chart Component
```
Timeline visualization showing:
- Horizontal bars for each objective/KPI
- Start/end dates
- Dependencies
- Milestones
- Current date indicator
- Progress overlay
```

**Libraries to use**:
- `react-d3-tree` or `react-organizational-chart` for tree view
- `react-gantt-timeline` or `frappe-gantt` for Gantt chart
- `recharts` or `visx` for custom visualizations

---

### Feature 3: Alignment & Cascading

#### Alignment Dashboard
Shows how individual work aligns with company goals:

```
You (Employee) → Team → Division → Company
--------------------------------------------------
Your KPIs:
  └─ Individual Objective: "Complete feature X"
      └─ Team Objective: "Launch product Y"
          └─ Division Objective: "Revenue growth"
              └─ Company Goal: "Increase revenue 30%"

Contribution: Your work contributes 12% to Division objective
```

**Features**:
- Visual alignment path
- Contribution percentage calculation
- Misaligned objectives warning
- Orphaned KPIs detection (KPIs not linked to objectives)

#### Cascading Goals Workflow
```
1. Admin creates company goals (Q4 planning)
2. Division managers create division objectives aligned to company goals
3. Team leads create team objectives aligned to division objectives
4. Employees create individual objectives and KPIs aligned to team objectives
5. System validates alignment and calculates contribution
```

---

### Feature 4: Progress Rollup

#### Automatic Progress Calculation
```python
def calculate_objective_progress(objective_id):
    # Get all child objectives
    children = get_child_objectives(objective_id)

    # Get all linked KPIs
    kpis = get_linked_kpis(objective_id)

    if children:
        # Average of child objectives
        progress = sum(child.progress for child in children) / len(children)
    elif kpis:
        # Weighted average of KPIs
        total_weight = sum(link.weight for link in kpis)
        progress = sum(kpi.progress * link.weight for kpi, link in kpis) / total_weight
    else:
        # Manual progress
        progress = objective.manual_progress or 0

    return progress
```

#### Progress Update Triggers
- When KPI progress updated → recalculate linked objectives
- When child objective updated → recalculate parent
- Batch recalculation job (nightly)

---

## 🎨 UI/UX Design

### Navigation Updates
Add new menu item:
```
📊 Dashboard
📋 KPIs
🎯 Objectives  ← NEW
   ├─ My Objectives
   ├─ Company Goals
   ├─ Tree View
   └─ Gantt Chart
📊 Reports
```

### Dashboard Updates
Add "Objectives Overview" section:
- Total objectives by level
- Progress toward company goals
- Alignment score
- At-risk objectives

---

## 🔧 Implementation Plan

### Phase C.1: Database & Backend (5-6 hours)

**Tasks**:
1. ✅ Create database migration for `objectives` table (30 min)
2. ✅ Create migration for `objective_kpi_links` table (30 min)
3. ✅ Add `objective_id` to KPIs table (30 min)
4. ✅ Create SQLAlchemy models (1 hour)
   - `Objective` model with relationships
   - `ObjectiveKPILink` model
5. ✅ Create Pydantic schemas (1 hour)
   - `ObjectiveCreate`, `ObjectiveUpdate`, `ObjectiveResponse`
   - `ObjectiveTree` (for tree view)
   - `ObjectiveGantt` (for Gantt chart)
6. ✅ Implement CRUD operations (1 hour)
   - Basic CRUD in `crud/objective.py`
   - Hierarchy operations (get_children, get_ancestors, get_tree)
7. ✅ Implement API endpoints (1.5 hours)
   - All endpoints listed above
   - Permission checks (RBAC)
8. ✅ Implement progress calculation (1 hour)
   - Recursive rollup algorithm
   - Background job for batch updates

### Phase C.2: Frontend - Basic UI (3-4 hours)

**Tasks**:
1. ✅ Create Objective service (`services/objectiveService.js`) (30 min)
2. ✅ Create Objectives List Page (1 hour)
3. ✅ Create Objective Form Page (1 hour)
4. ✅ Create Objective Detail Page (1 hour)
5. ✅ Add navigation menu items (30 min)

### Phase C.3: Frontend - Visualization (4-5 hours)

**Tasks**:
1. ✅ Install visualization libraries (30 min)
   ```bash
   npm install react-d3-tree frappe-gantt recharts
   ```
2. ✅ Create Tree View Component (2 hours)
   - Hierarchical tree rendering
   - Interactive nodes
   - Filtering and search
3. ✅ Create Gantt Chart Component (2 hours)
   - Timeline visualization
   - Progress overlay
   - Date range selection
4. ✅ Create Alignment View Component (1 hour)
   - Alignment path visualization
   - Contribution metrics

### Phase C.4: Integration & Testing (2-3 hours)

**Tasks**:
1. ✅ Link KPIs to objectives (1 hour)
   - Update KPI forms to allow objective selection
   - Add "Link to Objective" button on KPI detail page
2. ✅ Update Dashboard with objective stats (30 min)
3. ✅ Testing (1.5 hours)
   - Test CRUD operations
   - Test hierarchy operations
   - Test progress calculations
   - Test visualizations
   - Test permissions

---

## 📋 User Stories

### As an Admin
- I can create company-level goals for the year
- I can view the entire organization's objective hierarchy
- I can see which objectives are at risk
- I can reorganize the structure via drag-and-drop

### As a Manager
- I can create division/team objectives aligned to company goals
- I can see my team's objectives and their progress
- I can view a Gantt chart of my division's objectives
- I can approve/reject child objectives

### As an Employee
- I can create individual objectives aligned to team objectives
- I can link my KPIs to my objectives
- I can see how my work contributes to company goals
- I can view my alignment path

---

## 🧪 Testing Checklist

### Backend Tests
- [ ] Objective CRUD operations
- [ ] Hierarchy queries (children, ancestors, tree)
- [ ] Progress calculation (single, rollup)
- [ ] KPI linking
- [ ] Move operations (change parent)
- [ ] Permission checks
- [ ] Circular reference prevention

### Frontend Tests
- [ ] Objective list with filters
- [ ] Objective creation form
- [ ] Objective editing
- [ ] Tree view rendering
- [ ] Gantt chart rendering
- [ ] Alignment visualization
- [ ] KPI linking UI

---

## 📈 Success Metrics

**After Phase C completion:**
- ✅ Complete OKR framework (O + KR)
- ✅ 4-level hierarchy support
- ✅ Visual tree and Gantt views
- ✅ Automatic progress rollup
- ✅ Alignment tracking
- ✅ 100% backward compatible (existing KPIs still work)

---

## 🚀 Future Enhancements (Post Phase C)

1. **OKR Templates** - Predefined objective templates
2. **OKR Grading** - Score objectives (0.0 - 1.0 scale, Google style)
3. **Check-ins** - Weekly/monthly progress updates
4. **What-if Scenarios** - Simulate objective changes
5. **AI Suggestions** - Recommend alignment improvements
6. **Export** - Export tree view to PDF/PNG
7. **Real-time Collaboration** - WebSocket updates

---

## 📝 Notes

- Keep backward compatibility: Existing KPIs without objectives should still work
- Progress calculation should be fast (use caching, background jobs)
- Tree view should handle large hierarchies (100+ objectives)
- Gantt chart should support zoom levels (year/quarter/month)
- Mobile responsiveness for all new pages

---

**Ready to start implementation?** We can begin with Phase C.1 (Database & Backend) and work our way up!
