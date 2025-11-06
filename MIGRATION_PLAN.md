# AuShadha 2.0 - Dojo to HTMX + Alpine.js Migration Plan

**Date**: November 6, 2025
**Status**: In Progress - Phase 1 Complete
**Target Completion**: Iterative, based on priority

## Overview

This document outlines the strategic plan for migrating AuShadha 2.0's frontend from the Dojo Toolkit to a modern stack using HTMX and Alpine.js. This migration will:

- Reduce frontend complexity
- Improve performance and load times
- Modernize the codebase for easier maintenance
- Provide a cleaner, more maintainable architecture
- Enable future scalability with Vue.js for complex components

## Technology Stack

### Current Stack (Legacy)
- **Frontend Framework**: Dojo Toolkit 1.x
- **Widget Library**: Dijit
- **Extensions**: Dojox
- **CSS**: Dojo themes (Claro)
- **Backend**: Django 4.2.26

### New Stack (Target)
- **Dynamic HTML**: HTMX 1.9.10 (server-side rendering with minimal JS)
- **Reactive Components**: Alpine.js 3.13.5 (lightweight client-side interactivity)
- **CSS**: Modern CSS with custom framework (optional: Tailwind CSS later)
- **Complex Components**: Vue.js 3.x (when needed, not immediately)
- **Backend**: Django 4.2.26 (unchanged)

## Architecture Philosophy

### HTMX First
- Use HTMX for server-driven interactions
- Leverage Django's template system
- Minimize client-side JavaScript
- Benefits: SEO, simplicity, server control

### Alpine.js for Interactivity
- Use for client-side state management
- Form validation and dynamic UIs
- Modals, dropdowns, tabs
- Benefits: Lightweight, simple syntax

### Vue.js as Escape Hatch
- Only when HTMX + Alpine can't handle complexity
- Complex data grids
- Real-time collaborative features
- Rich interactive components

## Migration Phases

### ✅ Phase 1: Foundation (COMPLETED)

**Timeline**: Completed November 6, 2025

**Objectives**:
- Set up HTMX and Alpine.js infrastructure
- Create modern base templates
- Migrate authentication/login
- Establish CSS framework

**Completed Work**:
1. ✅ Created `script_links_modern.html` with HTMX + Alpine.js
2. ✅ Created `style_links_modern.html` with modern CSS
3. ✅ Created `base_modern.html` as new base template
4. ✅ Created `modern.css` with custom CSS framework
5. ✅ Created `login_modern.html` with modern login page
6. ✅ Created `login_modern.js` for Alpine.js login handling
7. ✅ Updated URLs to use modern login template
8. ✅ Completed audit of Dojo dependencies

**Files Created**:
- `/src/AuShadha/aushadha_ui/templates/aushadha_ui/script_links_modern.html`
- `/src/AuShadha/aushadha_ui/templates/aushadha_ui/style_links_modern.html`
- `/src/AuShadha/aushadha_ui/templates/aushadha_ui/base_modern.html`
- `/src/AuShadha/aushadha_ui/static/aushadha_ui/styles/modern.css`
- `/src/AuShadha/aushadha_ui/static/aushadha_ui/js/login_modern.js`
- `/src/AuShadha/aushadha_users/templates/registration/login_modern.html`

**Testing Needed**:
- Test login functionality with modern template
- Verify CSRF handling
- Test error handling
- Verify redirects work correctly

---

### Phase 2: Core UI & Navigation (NEXT)

**Timeline**: Estimated 2-3 weeks
**Priority**: HIGH
**Dependencies**: Phase 1 complete

**Objectives**:
- Migrate main application layout
- Replace BorderContainer with CSS Grid/Flexbox
- Update navigation system
- Migrate notification system

**Tasks**:

#### 2.1 Application Layout
- [ ] Create `home_modern.html` to replace `home.html`
- [ ] Convert BorderContainer layout to CSS Grid
  ```
  Old: <div data-dojo-type="dijit/layout/BorderContainer">
  New: <div class="app-layout" x-data="app()">
  ```
- [ ] Migrate header/footer sections
- [ ] Create responsive navigation menu
- [ ] Update main content area
- **Estimated Effort**: 5 days

#### 2.2 Notification System
- [ ] Replace dojox/widget/Toaster with Alpine.js notifications
- [ ] Create notification component in Alpine.js
  ```javascript
  Alpine.data('notifications', () => ({
      messages: [],
      show(message, type) { ... }
  }))
  ```
- [ ] Update `notification_dialog.js` → `notifications_modern.js`
- [ ] Test success, error, warning, info notifications
- **Estimated Effort**: 2 days

#### 2.3 Dialog/Modal System
- [ ] Create Alpine.js modal component
- [ ] Replace dijit/Dialog with modern modals
- [ ] Update `dialogs_and_misc.html` → `dialogs_modern.html`
- [ ] Test modal open/close, focus trap, ESC key handling
- **Estimated Effort**: 2 days

#### 2.4 Loading States
- [ ] Replace Dojo loader with HTMX indicators
- [ ] Create loading overlay component
- [ ] Add skeleton screens where appropriate
- **Estimated Effort**: 1 day

**Files to Create**:
- `home_modern.html`
- `header_modern.html`
- `footer_modern.html`
- `notifications_modern.js`
- `dialogs_modern.html`
- `modal_component.html`

**Testing Requirements**:
- Navigation between pages
- Notification display and timing
- Modal interactions
- Loading states during AJAX calls
- Responsive design on mobile/tablet

---

### Phase 3: Patient Management (HIGH PRIORITY)

**Timeline**: Estimated 2-3 weeks
**Priority**: HIGH
**Dependencies**: Phase 2 complete

**Objectives**:
- Migrate patient add/edit forms
- Update form validation
- Migrate patient search
- Update patient summary views

**Tasks**:

#### 3.1 Patient Forms
- [ ] Migrate `patient_detail/add.html` → `patient_detail/add_modern.html`
  - Replace dijit/form widgets with HTML5 inputs
  - Add Alpine.js for client-side validation
  - Use HTMX for form submission
  ```html
  <form hx-post="/AuShadha/patient/add/"
        hx-target="#patient-list"
        x-data="patientForm()">
  ```
- [ ] Migrate `patient_detail/edit.html` → `patient_detail/edit_modern.html`
- [ ] Create reusable form components
- [ ] Add inline validation feedback
- **Estimated Effort**: 5 days

#### 3.2 Patient Search
- [ ] Migrate `patient_search.js` → `patient_search_modern.js`
- [ ] Replace FilteringSelect with HTMX autocomplete
  ```html
  <input type="search"
         hx-get="/AuShadha/patient/search/"
         hx-trigger="keyup changed delay:300ms"
         hx-target="#search-results">
  ```
- [ ] Add debounced search
- [ ] Show search results dynamically
- **Estimated Effort**: 3 days

#### 3.3 Patient Summary
- [ ] Migrate `patient_detail/summary.html` → `patient_detail/summary_modern.html`
- [ ] Replace ContentPane with modern layout
- [ ] Add tabs with Alpine.js
- [ ] Update data display
- **Estimated Effort**: 3 days

#### 3.4 Patient List/Grid
- [ ] Evaluate grid library options:
  - Option A: Simple HTML table with Alpine.js + HTMX
  - Option B: TanStack Table (lightweight)
  - Option C: AG Grid (feature-rich, but heavier)
- [ ] Implement chosen solution
- [ ] Add sorting, filtering, pagination
- **Estimated Effort**: 5 days

**Files to Create**:
- `patient_detail/add_modern.html`
- `patient_detail/edit_modern.html`
- `patient_detail/summary_modern.html`
- `patient_search_modern.js`
- `patient_form_components.html`
- `patient_grid_modern.html`

**Testing Requirements**:
- Form validation (client and server-side)
- Form submission and error handling
- Patient search functionality
- Grid sorting and filtering
- Responsive design

---

### Phase 4: Search Components (MEDIUM PRIORITY)

**Timeline**: Estimated 1 week
**Priority**: MEDIUM
**Dependencies**: Phase 3 complete

**Objectives**:
- Migrate global search functionality
- Replace FilteringSelect widgets
- Implement autocomplete

**Tasks**:

#### 4.1 Global Search
- [ ] Migrate `search/search.html` → `search/search_modern.html`
- [ ] Create HTMX-based search
- [ ] Add real-time search results
- **Estimated Effort**: 2 days

#### 4.2 Autocomplete Component
- [ ] Create reusable autocomplete component
- [ ] Replace `search_filtering_select.html`
- [ ] Replace `search_filtering_select_small.html`
- [ ] Test with various data sources
- **Estimated Effort**: 3 days

**Files to Create**:
- `search/search_modern.html`
- `search/autocomplete_component.html`
- `search_modern.js`

---

### Phase 5: Data Display & Grids (MEDIUM PRIORITY)

**Timeline**: Estimated 2 weeks
**Priority**: MEDIUM
**Dependencies**: Phase 4 complete

**Objectives**:
- Replace Dojo DataGrid
- Implement modern table component
- Add sorting, filtering, pagination

**Tasks**:

#### 5.1 Grid Infrastructure
- [ ] Evaluate and choose grid solution
- [ ] Create base grid component
- [ ] Implement pagination
- [ ] Add sorting
- [ ] Add filtering
- **Estimated Effort**: 5 days

#### 5.2 Grid Integration
- [ ] Migrate all DataGrid instances
- [ ] Update `generic_grid_setup.js` → `grid_modern.js`
- [ ] Test with various data sources
- **Estimated Effort**: 5 days

**Files to Create**:
- `grid_modern.js`
- `grid_component.html`
- `pagination_component.html`

---

### Phase 6: Registry & Reference Data (MEDIUM-LOW PRIORITY)

**Timeline**: Estimated 1-2 weeks
**Priority**: MEDIUM-LOW
**Dependencies**: Phase 5 complete

**Objectives**:
- Migrate ICD10/ICD10PCS pages
- Update drug database search
- Convert tree widgets

**Tasks**:

#### 6.1 Drug Database
- [ ] Migrate `drug_db/fda_drugs/advanced_search.html`
- [ ] Update search functionality
- [ ] Migrate grid views
- **Estimated Effort**: 3 days

#### 6.2 ICD10/ICD10PCS
- [ ] Migrate `icd10pcs/codepage.html`
- [ ] Evaluate tree widget alternatives
  - Option A: Alpine.js custom tree
  - Option B: Simple library (e.g., arborist)
- [ ] Implement chosen solution
- **Estimated Effort**: 5 days

**Files to Create**:
- `drug_db/advanced_search_modern.html`
- `icd10pcs/codepage_modern.html`
- `tree_component.html` (if needed)

---

### Phase 7: Utility Components (LOW PRIORITY)

**Timeline**: Estimated 1 week
**Priority**: LOW
**Dependencies**: Phase 6 complete

**Objectives**:
- Migrate tooltips
- Update keyboard shortcuts
- Migrate remaining utilities

**Tasks**:

#### 7.1 Tooltips
- [ ] Replace dijit/Tooltip with CSS + Alpine.js
- [ ] Migrate `tooltips.html` → `tooltips_modern.html`
- **Estimated Effort**: 1 day

#### 7.2 Keyboard Shortcuts
- [ ] Update `key_bindings.js` → `key_bindings_modern.js`
- [ ] Use native KeyboardEvent
- [ ] Test all shortcuts
- **Estimated Effort**: 2 days

#### 7.3 Other Utilities
- [ ] Migrate `timer.js` (if still needed)
- [ ] Update `overlay.js` → use HTMX indicators
- [ ] Clean up unused utilities
- **Estimated Effort**: 2 days

---

### Phase 8: Testing & Cleanup (FINAL)

**Timeline**: Estimated 1-2 weeks
**Priority**: HIGH
**Dependencies**: All previous phases complete

**Objectives**:
- Comprehensive testing
- Remove Dojo library
- Clean up old files
- Update documentation

**Tasks**:

#### 8.1 Testing
- [ ] End-to-end testing of all features
- [ ] Cross-browser testing (Chrome, Firefox, Safari, Edge)
- [ ] Mobile/responsive testing
- [ ] Performance testing and optimization
- [ ] Accessibility testing
- **Estimated Effort**: 5 days

#### 8.2 Cleanup
- [ ] Remove Dojo library files
- [ ] Delete old templates
- [ ] Delete old JavaScript files
- [ ] Update .gitignore if needed
- **Estimated Effort**: 2 days

#### 8.3 Documentation
- [ ] Update developer documentation
- [ ] Update user documentation
- [ ] Create migration notes
- [ ] Document new architecture
- **Estimated Effort**: 3 days

---

## Technical Implementation Guidelines

### HTMX Patterns

#### Form Submission
```html
<form hx-post="/api/endpoint/"
      hx-target="#result"
      hx-swap="outerHTML"
      hx-indicator="#spinner">
  <input type="text" name="field">
  <button type="submit">Submit</button>
  <div id="spinner" class="htmx-indicator">Loading...</div>
</form>
```

#### Dynamic Content Loading
```html
<div hx-get="/api/content/"
     hx-trigger="load"
     hx-swap="innerHTML">
  Loading...
</div>
```

#### Infinite Scroll
```html
<div hx-get="/api/more/"
     hx-trigger="revealed"
     hx-swap="afterend">
  Load More
</div>
```

### Alpine.js Patterns

#### Form Validation
```html
<div x-data="formValidator()">
  <input type="text"
         x-model="email"
         @blur="validateEmail"
         :class="{ 'error': errors.email }">
  <span x-show="errors.email" x-text="errors.email"></span>
</div>

<script>
Alpine.data('formValidator', () => ({
    email: '',
    errors: {},
    validateEmail() {
        if (!this.email.includes('@')) {
            this.errors.email = 'Invalid email';
        } else {
            delete this.errors.email;
        }
    }
}));
</script>
```

#### Modal
```html
<div x-data="{ open: false }">
  <button @click="open = true">Open Modal</button>

  <div x-show="open"
       x-transition
       @click.away="open = false"
       @keydown.escape.window="open = false"
       class="modal">
    <div class="modal-content">
      <h2>Modal Title</h2>
      <p>Modal content</p>
      <button @click="open = false">Close</button>
    </div>
  </div>
</div>
```

#### Tabs
```html
<div x-data="{ activeTab: 'tab1' }">
  <div class="tabs">
    <button @click="activeTab = 'tab1'"
            :class="{ 'active': activeTab === 'tab1' }">
      Tab 1
    </button>
    <button @click="activeTab = 'tab2'"
            :class="{ 'active': activeTab === 'tab2' }">
      Tab 2
    </button>
  </div>

  <div x-show="activeTab === 'tab1'">Content 1</div>
  <div x-show="activeTab === 'tab2'">Content 2</div>
</div>
```

### Django View Patterns

#### HTMX Response
```python
from django.http import HttpResponse
from django.template import loader

def htmx_view(request):
    if request.htmx:  # Check if it's an HTMX request
        template = loader.get_template('partials/content.html')
        html = template.render({'data': data}, request)
        return HttpResponse(html)
    else:
        # Return full page for non-HTMX requests
        return render(request, 'full_page.html', {'data': data})
```

#### JSON Response for Alpine.js
```python
from django.http import JsonResponse

def api_view(request):
    if request.method == 'POST':
        form = MyForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({
                'success': True,
                'message': 'Saved successfully'
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            }, status=400)
```

## Risk Management

### Potential Risks

1. **Breaking Changes**
   - Risk: Migration breaks existing functionality
   - Mitigation: Thorough testing, keep old code until verified
   - Impact: HIGH

2. **Performance Issues**
   - Risk: New implementation is slower
   - Mitigation: Performance testing, optimization
   - Impact: MEDIUM

3. **Browser Compatibility**
   - Risk: Modern features not supported in older browsers
   - Mitigation: Test on target browsers, add polyfills if needed
   - Impact: LOW (modern browsers widely adopted in healthcare)

4. **Learning Curve**
   - Risk: Development team unfamiliar with new stack
   - Mitigation: Documentation, training, code examples
   - Impact: MEDIUM

5. **Incomplete Migration**
   - Risk: Migration stalls partway through
   - Mitigation: Phased approach, maintain both systems temporarily
   - Impact: MEDIUM

### Rollback Strategy

If migration needs to be rolled back:
1. Revert URL changes to use old templates
2. Old Dojo code remains in place until Phase 8
3. Each phase is independent and can be rolled back individually
4. Use feature flags in settings to toggle between old/new UIs

## Success Criteria

### Performance Metrics
- [ ] Page load time reduced by 30%
- [ ] JavaScript bundle size reduced by 60%
- [ ] Time to Interactive (TTI) improved by 40%
- [ ] Lighthouse score > 90

### Code Quality
- [ ] No Dojo dependencies remaining
- [ ] All tests passing
- [ ] Code coverage > 80%
- [ ] No console errors in browser

### User Experience
- [ ] All existing features working
- [ ] Improved responsiveness on mobile
- [ ] Better accessibility (WCAG 2.1 AA)
- [ ] Faster interactions (subjective)

## Resources

### Documentation
- HTMX: https://htmx.org/docs/
- Alpine.js: https://alpinejs.dev/
- Django + HTMX: https://django-htmx.readthedocs.io/
- Vue.js (future): https://vuejs.org/

### Tools
- Browser DevTools for debugging
- Lighthouse for performance auditing
- axe DevTools for accessibility testing
- Django Debug Toolbar

### Team Communication
- Regular standup meetings
- Code review for all changes
- Documentation updates in real-time
- Issue tracking in GitHub

## Timeline Summary

| Phase | Priority | Duration | Status |
|-------|----------|----------|--------|
| Phase 1: Foundation | HIGH | 1 week | ✅ COMPLETED |
| Phase 2: Core UI | HIGH | 2-3 weeks | 🔜 NEXT |
| Phase 3: Patient Mgmt | HIGH | 2-3 weeks | Pending |
| Phase 4: Search | MEDIUM | 1 week | Pending |
| Phase 5: Data Grids | MEDIUM | 2 weeks | Pending |
| Phase 6: Registry | MEDIUM-LOW | 1-2 weeks | Pending |
| Phase 7: Utilities | LOW | 1 week | Pending |
| Phase 8: Testing | HIGH | 1-2 weeks | Pending |

**Total Estimated Time**: 11-16 weeks (2.5-4 months)

## Notes

- Migration can be done iteratively - old and new code can coexist
- Priority should be given to frequently-used features
- Each phase should be fully tested before moving to the next
- User feedback should be gathered during migration
- Performance should be monitored throughout

## Change Log

- 2025-11-06: Initial migration plan created
- 2025-11-06: Phase 1 completed - Foundation established
- 2025-11-06: Audit completed - 22 template files, 25 JS files identified

## Next Actions

1. Test the modern login page
2. Begin Phase 2: Core UI & Navigation
3. Create home_modern.html
4. Migrate notification system

---

**Document Maintained By**: AuShadha Development Team
**Last Updated**: November 6, 2025
