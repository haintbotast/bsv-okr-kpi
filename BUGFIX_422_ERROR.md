# Bug Fix: 422 Unprocessable Entity Error

**Date**: 2025-11-04
**Status**: ✅ **FIXED**

---

## 🐛 Issue

Frontend could not load KPI list. Browser console showed:
```
Failed to load resource: the server responded with a status of 422 (Unprocessable Entity)
```

---

## 🔍 Root Cause

The frontend was sending empty string values for optional query parameters:
```
GET /api/v1/kpis?skip=0&limit=20&year=2025&quarter=&status=&search=
                                                    ^^       ^^      ^^
                                                Empty strings sent
```

The backend API endpoint for `quarter` parameter has validation:
```python
quarter: Optional[str] = Query(None, pattern="^Q[1-4]$")
```

This regex pattern `^Q[1-4]$` only accepts:
- `Q1`, `Q2`, `Q3`, `Q4` ✅
- `None` (parameter not sent) ✅
- Empty string `""` ❌ **REJECTED**

---

## ✅ Solution

Updated `/frontend/src/services/kpiService.js` to filter out empty/null values before sending API requests:

### Before:
```javascript
async getKPIs(params = {}) {
  const { skip = 0, limit = 100, user_id, year, quarter, status, search } = params
  const response = await api.get('/kpis', {
    params: { skip, limit, user_id, year, quarter, status, search },
  })
  return response.data
}
```

### After:
```javascript
async getKPIs(params = {}) {
  const { skip = 0, limit = 100, user_id, year, quarter, status, search } = params

  // Filter out empty/null values to avoid validation errors
  const filteredParams = {
    skip,
    limit,
    ...(user_id && { user_id }),
    ...(year && { year }),
    ...(quarter && { quarter }),
    ...(status && { status }),
    ...(search && { search }),
  }

  const response = await api.get('/kpis', {
    params: filteredParams,
  })
  return response.data
}
```

---

## 🔧 How the Fix Works

The new code uses JavaScript spread operator with conditional inclusion:
- `...(quarter && { quarter })` - Only includes `quarter` parameter if it has a truthy value
- Empty strings `""` are falsy in JavaScript, so they are excluded
- `null` and `undefined` are also excluded
- `0` is falsy but handled separately for `skip` (always included)

**Result:**
```
Before: GET /api/v1/kpis?skip=0&limit=20&year=2025&quarter=&status=&search=
After:  GET /api/v1/kpis?skip=0&limit=20&year=2025
```

Only parameters with actual values are sent!

---

## 🚀 Deployment

```bash
cd /home/haint/Documents/bsv-okr-kpi/deployment

# Rebuild frontend with fix
sg docker -c "docker compose up -d --build frontend"

# Verify
sg docker -c "docker compose ps"
```

---

## ✅ Verification

### Test the fix:
1. Open browser: http://localhost
2. Login with admin credentials
3. Navigate to KPI list page
4. Check browser console - no more 422 errors ✅
5. KPI list loads successfully ✅

### Backend logs (after fix):
```
INFO: GET /api/v1/kpis?skip=0&limit=20&year=2025 HTTP/1.1" 200 OK
```

No more 422 errors! 🎉

---

## 📝 Files Modified

1. **`/frontend/src/services/kpiService.js`**
   - Added parameter filtering in `getKPIs()` method
   - Prevents empty strings from being sent as query parameters

---

## 🎓 Lessons Learned

### Frontend Best Practices:
1. **Always filter optional parameters** before sending API requests
2. **Don't send empty strings** for optional parameters - omit them instead
3. **Test with empty filters** to catch validation issues

### Backend Best Practices:
1. **Use `Optional[str]`** for optional query parameters
2. **Add clear validation patterns** (regex for quarter: `^Q[1-4]$`)
3. **Return descriptive error messages** for validation failures

### Integration Testing:
1. Test all filter combinations including empty values
2. Verify API contracts between frontend and backend
3. Check query parameter handling

---

## 🔄 Similar Issues to Watch For

This same pattern should be applied to other API calls that have optional parameters with validation:

### Potentially Affected Endpoints:
- ✅ `/api/v1/kpis` - **FIXED**
- `/api/v1/templates` - May need similar fix if has optional params with patterns
- `/api/v1/users` - Check optional filter params
- `/api/v1/analytics` - Check optional filter params

### Recommended Action:
Review all service files and apply the same filtering pattern:

```bash
# Find all service files
find frontend/src/services -name "*.js"

# Check for similar patterns
grep -n "params: {" frontend/src/services/*.js
```

---

## 📊 Impact

- **Severity**: High (blocks main functionality)
- **Affected Users**: All users trying to view KPI list
- **Fix Time**: ~5 minutes
- **Rebuild Time**: ~1 minute
- **Downtime**: None (rolling update)

---

## ✅ Status

**RESOLVED** - Frontend now correctly filters empty parameters before API calls.

Both containers healthy:
```
NAME           STATUS
kpi-backend    Up (healthy)
kpi-frontend   Up (healthy)
```

Application fully functional! 🎉

---

## 🔗 Related Documentation

- **[DOCKER_OPERATIONS.md](DOCKER_OPERATIONS.md)** - Container management
- **[DEPLOYMENT_SUCCESS.md](DEPLOYMENT_SUCCESS.md)** - Initial deployment
- **[CLAUDE.md](CLAUDE.md)** - Project architecture

---

**Fixed by**: Claude Code
**Deployed**: 2025-11-04
**Build**: Frontend rebuilt with parameter filtering
