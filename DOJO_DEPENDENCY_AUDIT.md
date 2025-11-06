# Dojo Dependency Audit - AuShadha 2.0

**Date**: November 6, 2025
**Purpose**: Identify all Dojo Toolkit dependencies for migration to HTMX + Alpine.js

## Executive Summary

This audit identifies all components of AuShadha 2.0 that currently depend on the Dojo Toolkit framework. The migration to HTMX + Alpine.js will modernize the frontend stack, reduce complexity, and improve maintainability.

## Dojo Usage Statistics

- **Total Template Files with Dojo**: 22 files
- **Custom JavaScript Files Using Dojo**: ~25 files
- **Dojo Components Used**: dojo, dijit, dojox

## Application Templates Using Dojo

### Authentication & Login (Priority: HIGH - ✅ COMPLETED)
- ✅ `src/AuShadha/aushadha_users/templates/registration/login.html` - Migrated to `login_modern.html`
- ✅ `src/AuShadha/aushadha_users/templates/registration/login_form.html` - Replaced with modern form
- `src/AuShadha/aushadha_users/templates/registration/footer.html`
- `src/AuShadha/AuShadha/templates/registration/login.html` (duplicate)
- `src/AuShadha/AuShadha/templates/registration/login_form.html` (duplicate)
- `src/AuShadha/AuShadha/templates/registration/footer.html` (duplicate)

### Base Templates (Priority: HIGH)
- `src/AuShadha/aushadha_ui/templates/aushadha_ui/base.html`
  - **Status**: Legacy template, modern alternative created as `base_modern.html`
  - **Dependencies**: Full Dojo framework
  - **Components**: BorderContainer, ContentPane, Dialog, TabContainer
  - **Migration Notes**: Core application layout, requires careful migration

- `src/AuShadha/aushadha_ui/templates/aushadha_ui/style_links.html`
  - **Status**: References all Dojo CSS files
  - **Alternative**: `style_links_modern.html` created

- `src/AuShadha/aushadha_ui/templates/aushadha_ui/script_links.html`
  - **Status**: Loads Dojo framework
  - **Alternative**: `script_links_modern.html` created

- `src/AuShadha/aushadha_ui/templates/aushadha_ui/home.html`
  - **Dependencies**: BorderContainer, GridContainer, Portlet widgets
  - **Migration Complexity**: MEDIUM

### Patient Management (Priority: HIGH)
- `src/AuShadha/patient/templates/patient_detail/add.html`
  - **Dependencies**: dijit/form widgets, validation
  - **Migration Complexity**: MEDIUM

- `src/AuShadha/patient/templates/patient_detail/edit.html`
  - **Dependencies**: dijit/form widgets, validation
  - **Migration Complexity**: MEDIUM

- `src/AuShadha/patient/templates/patient_detail/summary.html`
  - **Dependencies**: Grid widgets, ContentPane
  - **Migration Complexity**: MEDIUM

### Search Components (Priority: MEDIUM)
- `src/AuShadha/search/templates/search/search.html`
  - **Dependencies**: FilteringSelect, autocomplete
  - **Migration Complexity**: LOW-MEDIUM

- `src/AuShadha/search/templates/search/search_filtering_select.html`
  - **Dependencies**: dijit/form/FilteringSelect
  - **Migration Complexity**: LOW

- `src/AuShadha/search/templates/search/search_filtering_select_small.html`
  - **Dependencies**: dijit/form/FilteringSelect
  - **Migration Complexity**: LOW

### Registry/Reference Data (Priority: LOW)
- `src/AuShadha/registry/drug_db/templates/drug_db/fda_drugs/advanced_search.html`
  - **Dependencies**: Complex form widgets, DataGrid
  - **Migration Complexity**: MEDIUM-HIGH

- `src/AuShadha/registry/icd10pcs/templates/icd10pcs/codepage.html`
  - **Dependencies**: Tree widgets, ContentPane
  - **Migration Complexity**: MEDIUM

### UI Components (Priority: MEDIUM)
- `src/AuShadha/aushadha_ui/templates/aushadha_ui/tooltips.html`
  - **Dependencies**: dijit/Tooltip
  - **Migration Complexity**: LOW

- `src/AuShadha/aushadha_ui/templates/aushadha_ui/dialogs_and_misc.html`
  - **Dependencies**: dijit/Dialog
  - **Migration Complexity**: LOW-MEDIUM

- `src/AuShadha/aushadha_ui/templates/aushadha_ui/about_credits_and_license.html`
  - **Dependencies**: ContentPane, Dialog
  - **Migration Complexity**: LOW

- `src/AuShadha/aushadha_ui/templates/aushadha_ui/credits.html`
  - **Dependencies**: ContentPane
  - **Migration Complexity**: LOW

## Custom JavaScript Files Using Dojo

### Core Application Files (Priority: HIGH)
1. **script.js** - Main application initialization
   - Loads UI after authentication
   - Creates application layout
   - **Migration Complexity**: HIGH

2. **main.js** - Core utilities and setup
   - **Migration Complexity**: MEDIUM

3. **login.js** - ✅ Replaced with `login_modern.js`

### UI Component Files (Priority: MEDIUM)
4. **pane_and_widget_creator.js** - Dynamic widget creation
5. **app_container_creator.js** - Container layouts
6. **dynamic_html_pane_creator.js** - Dynamic content panes
7. **create.js** - Pane creation utilities
8. **create_add_button.js** - Button generation

### Grid & Data Display (Priority: MEDIUM)
9. **generic_grid_setup.js** - DataGrid configuration
10. **stores.js** - Data stores for grids
11. **table_tools.js** - Table utilities

### Form & CRUD (Priority: HIGH)
12. **crud.js** - Create, Read, Update, Delete operations
13. **patient_search.js** - Patient search functionality

### Utility Files (Priority: LOW-MEDIUM)
14. **notification_dialog.js** - Toast notifications
15. **notifications.js** - Notification system
16. **overlay.js** - Loading overlays
17. **key_bindings.js** - Keyboard shortcuts
18. **timer.js** - Timer utilities
19. **event_controller.js** - Event management
20. **global_behaviours.js** - Global event handlers

### Tree Components (Priority: MEDIUM)
21. **pane_tree_creator.js** - Tree widget creation
22. **main.js** (in tree/ directory) - Tree utilities

### Dialog Components (Priority: LOW)
23. **NonModalDialog.js** - Custom dialog widget

### Included Template JS (Priority: HIGH)
- **constants.js** - Application constants
- **urls.js** - URL definitions (uses Django templates)
- **resources.js** - Resource paths (uses Django templates)

## Dojo Components Currently Used

### Core Modules
- `dojo/parser` - Widget parser
- `dojo/ready` - DOM ready handler
- `dojo/on` - Event handling
- `dojo/request` - AJAX requests
- `dojo/dom` - DOM manipulation
- `dojo/dom-form` - Form utilities

### Dijit Widgets (UI Components)
- `dijit/form/Form` - Form container
- `dijit/form/Button` - Buttons
- `dijit/form/TextBox` - Text inputs
- `dijit/form/ValidationTextBox` - Validated inputs
- `dijit/form/Textarea` - Text areas
- `dijit/form/FilteringSelect` - Autocomplete selects
- `dijit/Dialog` - Modal dialogs
- `dijit/Tooltip` - Tooltips
- `dijit/layout/ContentPane` - Content containers
- `dijit/layout/TabContainer` - Tabbed interfaces
- `dijit/layout/BorderContainer` - Border layouts

### Dojox Extensions
- `dojox/form/Manager` - Form management
- `dojox/validate/web` - Form validation
- `dojox/layout/ContentPane` - Extended content pane
- `dojox/layout/GridContainer` - Grid layouts
- `dojox/layout/ExpandoPane` - Expandable panes
- `dojox/layout/FloatingPane` - Floating windows
- `dojox/widget/Portlet` - Dashboard widgets
- `dojox/widget/Toaster` - Toast notifications
- `dojox/widget/Calendar` - Calendar widget
- `dojox/grid/DataGrid` - Data grids

## Migration Recommendations

### Phase 1: Foundation (✅ COMPLETED)
1. ✅ Set up HTMX + Alpine.js infrastructure
2. ✅ Create modern base templates
3. ✅ Migrate login/authentication pages
4. ✅ Create modern CSS framework

### Phase 2: Core UI (NEXT PRIORITY)
1. Migrate base application layout (home.html, base.html)
2. Replace BorderContainer with modern CSS Grid/Flexbox
3. Migrate notification system (toaster → Alpine.js + CSS)
4. Update dialog system (Dialog → Alpine.js modals)

### Phase 3: Patient Management (HIGH PRIORITY)
1. Migrate patient add/edit forms
2. Convert form validation to HTML5 + Alpine.js
3. Update patient search functionality
4. Migrate patient summary views

### Phase 4: Data Grids & Tables
1. Replace Dojo DataGrid with modern table component
   - Consider: TanStack Table, AG Grid, or simple HTML tables with Alpine.js
2. Update data stores to use fetch API
3. Migrate pagination and sorting

### Phase 5: Search & Autocomplete
1. Replace FilteringSelect with modern autocomplete
   - Consider: Alpine.js + HTMX for server-side filtering
   - Or client-side libraries like Tom Select

### Phase 6: Registry & Reference Data
1. Migrate ICD10/ICD10PCS pages
2. Update drug database search
3. Convert tree widgets to modern alternatives

### Phase 7: Cleanup
1. Remove Dojo library files
2. Update all references
3. Clean up unused JavaScript files
4. Update documentation

## Modern Equivalents

| Dojo Component | Modern Alternative |
|----------------|-------------------|
| dojo/parser | Not needed (use x-data, x-init) |
| dojo/request | fetch API or HTMX |
| dojo/dom | Native DOM APIs |
| dijit/Dialog | Alpine.js x-show + modal |
| dijit/form/ValidationTextBox | HTML5 validation + Alpine.js |
| dijit/layout/BorderContainer | CSS Grid / Flexbox |
| dijit/layout/TabContainer | Alpine.js tabs |
| dojox/widget/Toaster | Alpine.js notifications |
| dojox/grid/DataGrid | TanStack Table or custom table |
| dojox/form/FilteringSelect | HTMX + Alpine.js autocomplete |

## Complexity Assessment

- **Login System**: ✅ COMPLETED (LOW complexity)
- **Base Templates**: HIGH complexity - Core application structure
- **Forms**: MEDIUM complexity - Validation migration needed
- **Grids**: MEDIUM-HIGH complexity - May need third-party library
- **Search**: LOW-MEDIUM complexity - HTMX handles this well
- **Dialogs/Modals**: LOW complexity - Alpine.js handles easily
- **Notifications**: LOW complexity - CSS + Alpine.js
- **Tree Widgets**: MEDIUM complexity - May need library

## Next Steps

1. ✅ Complete Phase 1 (Foundation)
2. Create migration plan document
3. Start Phase 2: Core UI migration
4. Test each component thoroughly
5. Update documentation as you go

## Notes

- Keep old Dojo files until migration is complete
- Test thoroughly in development before removing Dojo
- Consider adding Vue.js for complex components (grids, trees) if needed
- Document any issues or gotchas during migration
- Update this audit as components are migrated

## Files Created

### Modern Stack Files
- `/src/AuShadha/aushadha_ui/templates/aushadha_ui/script_links_modern.html`
- `/src/AuShadha/aushadha_ui/templates/aushadha_ui/style_links_modern.html`
- `/src/AuShadha/aushadha_ui/templates/aushadha_ui/base_modern.html`
- `/src/AuShadha/aushadha_ui/static/aushadha_ui/styles/modern.css`
- `/src/AuShadha/aushadha_ui/static/aushadha_ui/js/login_modern.js`
- `/src/AuShadha/aushadha_users/templates/registration/login_modern.html`

### Configuration Changes
- Updated `/src/AuShadha/aushadha_users/urls.py` to use modern login template
