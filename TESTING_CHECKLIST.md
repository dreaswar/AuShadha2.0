# AuShadha 2.0 Testing Checklist

**Date Created:** November 5, 2025
**Testing Phase:** Initial HTMX Implementation
**Status:** Ready for Testing

---

## Prerequisites

### 1. Environment Setup
- [ ] Python 3.11+ installed
- [ ] PostgreSQL server running
- [ ] Database `aushadha2` created
- [ ] Database user `aushadha` created with password
- [ ] Virtual environment activated

### 2. Install Dependencies
```bash
cd /home/user/AuShadha2.0
python3 -m venv venv
source venv/bin/activate
pip install -r requirements/development.txt
```

### 3. Environment Configuration
- [ ] Copy `.env.example` to `.env`
- [ ] Update `.env` with actual database credentials
- [ ] Verify `DJANGO_SECRET_KEY` is set
- [ ] Verify `DJANGO_DEBUG=True` for development

### 4. Database Migration
```bash
cd src/AuShadha
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

---

## Phase 1: Basic Application Testing

### Test 1: Application Starts
```bash
cd src/AuShadha
python manage.py check
python manage.py runserver
```

**Expected Results:**
- ✅ No errors in `python manage.py check`
- ✅ Server starts on `http://127.0.0.1:8000`
- ✅ No import errors
- ✅ Logging messages appear in console

**Known Issues to Fix:**
- May need to create default clinic if none exists
- May need to fix imports in other modules

---

### Test 2: URL Resolution
Visit these URLs and verify they resolve:

| URL | Expected | Status |
|-----|----------|--------|
| `http://127.0.0.1:8000/` | Redirect to `/AuShadha/patients/` | ⏳ |
| `http://127.0.0.1:8000/AuShadha/patients/` | Patient home page | ⏳ |
| `http://127.0.0.1:8000/admin/` | Django admin login | ⏳ |
| `http://127.0.0.1:8000/AuShadha/authenticate/login/` | Login page | ⏳ |

**Check:**
- [ ] No 404 errors
- [ ] No 500 errors
- [ ] Templates load correctly
- [ ] Static files (CSS/JS) load from CDN

---

### Test 3: HTMX and Alpine.js Loading
Open browser developer tools (F12) and check:

**Console Checks:**
- [ ] No JavaScript errors
- [ ] `htmx` object exists (type `htmx` in console)
- [ ] `Alpine` object exists (type `Alpine` in console)
- [ ] Tailwind CSS classes are applied

**Network Tab:**
- [ ] HTMX loads from CDN (htmx.org)
- [ ] Alpine.js loads from CDN (unpkg.com)
- [ ] Tailwind CSS loads from CDN

---

## Phase 2: Patient Module Testing

### Test 4: Patient Home Page
Visit: `http://127.0.0.1:8000/AuShadha/patients/`

**Visual Checks:**
- [ ] Navigation header appears
- [ ] "Add New Patient" button visible
- [ ] Search bar visible
- [ ] Filters dropdown works (Alpine.js)
- [ ] User menu dropdown works (Alpine.js)
- [ ] Page is responsive (resize browser)

**HTMX Checks:**
- [ ] Patient list loads via HTMX automatically
- [ ] Loading spinner appears during load
- [ ] Network tab shows XHR request to `/AuShadha/patients/list/`

---

### Test 5: Patient List (HTMX Partial)
The patient list should load automatically via HTMX.

**If No Patients Exist:**
- [ ] "No patients found" message appears
- [ ] "Add Patient" button appears in empty state
- [ ] No errors in console

**If Patients Exist:**
- [ ] Patient table displays correctly
- [ ] Patient avatars show initials
- [ ] Hospital ID, name, age, sex, clinic display
- [ ] Action menu (3 dots) works (Alpine.js)
- [ ] Hovering over rows highlights them

---

### Test 6: Add Patient (Modal + HTMX)
Click "Add New Patient" button:

**Modal Behavior (Alpine.js):**
- [ ] Modal appears with smooth animation
- [ ] Background overlay appears
- [ ] Click outside modal closes it
- [ ] X button closes modal

**Form Loading (HTMX):**
- [ ] Form loads inside modal via HTMX
- [ ] "Loading form..." appears briefly
- [ ] Form fields appear:
  - Hospital ID
  - First Name
  - Middle Name
  - Last Name
  - Age
  - Sex (dropdown)

**Client-Side Validation (Alpine.js):**
- [ ] Try submitting empty form - errors appear
- [ ] Fill Hospital ID - error clears
- [ ] Fill First Name - error clears
- [ ] Enter age > 150 - error appears
- [ ] Enter negative age - error appears

**Form Submission (HTMX):**
- [ ] Fill valid data and submit
- [ ] "Saving..." appears on submit button
- [ ] Form submits via HTMX (no page reload)
- [ ] Success message appears
- [ ] Modal closes automatically
- [ ] Patient list refreshes with new patient
- [ ] New patient appears in list

**Test Data:**
```
Hospital ID: P2025001
First Name: John
Middle Name: M
Last Name: Doe
Age: 35
Sex: Male
```

---

### Test 7: Search Functionality (HTMX)
In the search bar:

**Test Searches:**
- [ ] Type "John" - results filter via HTMX
- [ ] Type Hospital ID - results filter
- [ ] Search has 500ms delay (debounce)
- [ ] No page reload during search
- [ ] Loading spinner appears during search
- [ ] Clear search - all patients show

**Check Network Tab:**
- [ ] XHR requests to `/AuShadha/patients/list/?search=...`
- [ ] Only partial HTML returned (not full page)

---

### Test 8: Pagination (HTMX)
If you have 20+ patients:

- [ ] Pagination controls appear
- [ ] "Previous" and "Next" buttons work
- [ ] Clicking page number loads via HTMX
- [ ] No page reload
- [ ] URL doesn't change
- [ ] Patient count shows correctly

---

### Test 9: Patient Actions Menu (Alpine.js)
Click the 3-dot menu on any patient:

- [ ] Dropdown appears (Alpine.js)
- [ ] Click outside - dropdown closes
- [ ] Options visible:
  - View Details
  - Edit
  - View History
  - New Visit
  - Delete (red)

**Test View Details (HTMX):**
- [ ] Click "View Details"
- [ ] Patient detail modal/page loads
- [ ] Shows patient information
- [ ] Tabs work (Alpine.js)

---

### Test 10: Patient Detail View (HTMX)
Navigate to patient detail:

**Layout:**
- [ ] Patient avatar with initials
- [ ] Patient name and Hospital ID
- [ ] "Edit" and "New Visit" buttons
- [ ] Personal Information section
- [ ] Clinical Information section

**Tabs (Alpine.js):**
- [ ] Click "Overview" tab - shows overview
- [ ] Click "Demographics" tab - shows coming soon
- [ ] Click "History" tab - shows coming soon
- [ ] Click "Visits" tab - shows coming soon
- [ ] Tab switching is smooth (no page reload)

**Quick Actions:**
- [ ] All 4 quick action buttons visible
- [ ] Hover effects work
- [ ] Shows "Coming Soon" labels

---

### Test 11: Edit Patient (HTMX)
Click "Edit" on a patient:

- [ ] Edit form loads via HTMX
- [ ] Form pre-filled with patient data
- [ ] Can modify fields
- [ ] Save button works
- [ ] Updates patient without page reload
- [ ] Success message appears
- [ ] Patient list updates with changes

---

### Test 12: Delete Patient (HTMX)
Click "Delete" on a patient:

- [ ] Confirmation dialog appears
- [ ] Cancel - no deletion
- [ ] Confirm - patient deleted via HTMX
- [ ] Row fades out and disappears
- [ ] No page reload
- [ ] Success message appears

**Note:** Delete requires superuser privileges

---

## Phase 3: Error Handling

### Test 13: Network Errors
Simulate network failure:

**Steps:**
1. Open DevTools Network tab
2. Set throttling to "Offline"
3. Try to load patient list

**Expected:**
- [ ] Error message appears
- [ ] HTMX logs error in console
- [ ] Application doesn't crash
- [ ] User sees friendly error message

---

### Test 14: Invalid Data
Try to add patient with:

**Duplicate Hospital ID:**
- [ ] Server returns validation error
- [ ] Error message displays in form
- [ ] Form doesn't close
- [ ] User can correct and resubmit

**Missing Required Fields:**
- [ ] Client-side validation catches it
- [ ] Errors show under each field
- [ ] Submit button disabled until valid

---

### Test 15: Browser Compatibility
Test in different browsers:

| Browser | Version | Status |
|---------|---------|--------|
| Chrome | Latest | ⏳ |
| Firefox | Latest | ⏳ |
| Safari | Latest | ⏳ |
| Edge | Latest | ⏳ |

**Check:**
- [ ] All features work
- [ ] No console errors
- [ ] Styling consistent
- [ ] Animations smooth

---

### Test 16: Mobile Responsiveness
Test on mobile devices or resize browser:

**Viewport Sizes:**
- [ ] Mobile (375px) - layout adapts
- [ ] Tablet (768px) - layout adapts
- [ ] Desktop (1024px+) - full layout

**Mobile-Specific:**
- [ ] Navigation menu collapses
- [ ] Search bar full width
- [ ] Tables scroll horizontally
- [ ] Buttons stack vertically
- [ ] Touch interactions work

---

## Phase 4: Performance Testing

### Test 17: Page Load Speed
Measure performance:

**Tools:**
- Chrome DevTools Lighthouse
- Network tab timing

**Targets:**
- [ ] Initial page load < 2 seconds
- [ ] HTMX partial load < 500ms
- [ ] Total JavaScript < 200KB
- [ ] No layout shifts (CLS)

---

### Test 18: Database Performance
With 100+ patients:

- [ ] List loads quickly
- [ ] Search is fast
- [ ] Pagination works smoothly
- [ ] No N+1 query problems

**Check Queries:**
```bash
# Enable query logging in settings
DEBUG = True
LOGGING['loggers']['django.db.backends'] = {
    'level': 'DEBUG'
}
```

---

## Phase 5: Security Testing

### Test 19: Authentication
- [ ] Unauthenticated users redirected to login
- [ ] Login works correctly
- [ ] Logout works correctly
- [ ] Session persists correctly

### Test 20: Authorization
- [ ] Regular users can't delete patients
- [ ] Superuser can delete patients
- [ ] Permissions enforced on all actions

### Test 21: CSRF Protection
- [ ] Forms include CSRF token
- [ ] POST requests validate CSRF
- [ ] HTMX includes CSRF in headers

### Test 22: XSS Prevention
Try entering script tags in patient name:
```
<script>alert('XSS')</script>
```

- [ ] Script doesn't execute
- [ ] Content is escaped in display
- [ ] No security warnings

---

## Known Issues to Fix

### Critical
- [ ] Create default clinic if none exists (FK constraint)
- [ ] Fix any import errors in other modules
- [ ] Ensure all URLs resolve correctly

### Medium
- [ ] Add proper form validation messages
- [ ] Improve error handling for AJAX failures
- [ ] Add loading states for all actions

### Low
- [ ] Add keyboard shortcuts
- [ ] Add accessibility labels
- [ ] Improve mobile menu

---

## Success Criteria

**Minimum Requirements:**
- ✅ Application starts without errors
- ✅ Patient list loads via HTMX
- ✅ Can add patient with form validation
- ✅ Search works without page reload
- ✅ No JavaScript errors in console
- ✅ Responsive on mobile devices

**Ideal State:**
- ✅ All CRUD operations work
- ✅ All animations smooth
- ✅ Page load < 2 seconds
- ✅ No security vulnerabilities
- ✅ Works in all modern browsers
- ✅ 100% keyboard accessible

---

## Test Results

Record your test results here:

**Date Tested:** ___________
**Tested By:** ___________
**Environment:** Development / Staging / Production

**Overall Status:**
- [ ] All tests passing
- [ ] Some tests failing (see notes below)
- [ ] Major issues found

**Notes:**
```
[Add any issues, bugs, or observations here]
```

---

## Next Steps After Testing

1. **If All Tests Pass:**
   - ✅ Commit any bug fixes
   - ✅ Move to Phase 2 (Add missing patient features)
   - ✅ Start demographics module migration

2. **If Tests Fail:**
   - 🔧 Fix critical bugs first
   - 🔧 Re-test failed areas
   - 🔧 Document workarounds

3. **Performance Issues:**
   - 🚀 Optimize database queries
   - 🚀 Add caching where needed
   - 🚀 Minimize JavaScript

---

**End of Testing Checklist**

*This document will be updated as new features are added.*
