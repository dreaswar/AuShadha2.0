# AuShadha 1.0 → 2.0 Migration & Modernization Plan

## Executive Summary

AuShadha 2.0 is currently a **partial migration** of AuShadha 1.0 with:
- ✅ **Completed**: Core infrastructure (patient, clinic, registry, users, base models)
- ❌ **Missing**: All clinical data modules (70% of functionality)
- ⚠️ **Issues**: Security vulnerabilities, outdated dependencies, broken imports

This plan outlines a complete migration strategy to restore full functionality with modern dependencies.

---

## Current State Analysis

### What's Working in 2.0
- Patient registration (basic)
- Clinic management
- Medical registries (ICD10, ICD10-PCS, Drug DB, Vaccines)
- User authentication
- Base model framework
- UI widget system

### Critical Missing Modules (from 1.0)

| Module | Lines of Code | Priority | Clinical Impact |
|--------|--------------|----------|-----------------|
| **Demographics** | ~3,500 | HIGH | Patient contact information |
| **Visit Management** | ~8,000 | CRITICAL | Core clinical workflow |
| **Medical History** | ~4,000 | CRITICAL | Patient medical records |
| **Medication List** | ~2,000 | CRITICAL | Prescriptions & drugs |
| **Allergy List** | ~1,500 | HIGH | Patient safety |
| **Immunisation** | ~1,800 | MEDIUM | Vaccination records |
| **Utility Apps** | ~2,500 | LOW | Dashboard, tasks, notes |

**Total Missing**: ~23,300 lines of functional code

---

## Phase 1: Foundation & Security (Week 1)

### 1.1 Security Hardening (Day 1)

#### Priority: 🔴 CRITICAL

**Issues to Fix:**
```python
# settings.py Line 42
SECRET_KEY = 'i_x=+rho3+kn7imy8p7mykdx@7l^h10rs&ir^a^f4s*_wyphm@'  # ❌ EXPOSED

# settings.py Line 45
DEBUG = True  # ❌ PRODUCTION UNSAFE

# settings.py Line 47
ALLOWED_HOSTS = []  # ❌ ALLOWS ANY HOST

# settings.py Line 207
yaml.load()  # ❌ ARBITRARY CODE EXECUTION

# settings.py Lines 120-122
DATABASE credentials hardcoded  # ❌ SECURITY RISK
```

**Solution:**
1. Create `.env` file (add to .gitignore)
2. Use `python-decouple` or `django-environ`
3. Implement environment-based configuration
4. Change `yaml.load()` to `yaml.safe_load()`

**Files to Create:**
- `.env.example` (template)
- `.env` (local, gitignored)
- `AuShadha/settings/base.py`
- `AuShadha/settings/development.py`
- `AuShadha/settings/production.py`

### 1.2 Dependency Modernization (Day 2-3)

#### Current Dependencies (10+ years old):
```txt
Django>=1.5.4      # Released 2013, EOL 2015 ❌
psycopg2           # Unversioned ❌
PyYAML>=3.10       # 2013 release ❌
Sphinx>=1.2b2      # Beta version ❌
```

#### Target Dependencies (2025):
```txt
Django>=4.2,<5.0              # LTS version, supported until April 2026
psycopg2-binary>=2.9.9        # Latest stable
PyYAML>=6.0.1                 # Security fixes included
python-decouple>=3.8          # Environment variable management

# Testing
pytest>=7.4.3
pytest-django>=4.7.0
pytest-cov>=4.1.0
factory-boy>=3.3.0

# Code Quality
black>=23.12.1
flake8>=7.0.0
mypy>=1.8.0

# API (Future)
djangorestframework>=3.14.0

# Documentation
Sphinx>=7.2.6
```

**Migration Strategy:**
1. Create new virtual environment with Python 3.11+
2. Install Django 4.2 LTS
3. Run tests after each dependency upgrade
4. Fix deprecated API calls
5. Update code for Django 4.2 compatibility

### 1.3 Fix Broken Code (Day 3)

#### Deprecated APIs to Fix:

```python
# patient/models.py:89 - Deprecated in Django 1.10+
for item in self._meta.get_fields_with_model():  # ❌

# Fixed:
for field in self._meta.get_fields():
    if not isinstance(field, (AutoField, OneToOneField)):
        exportable_fields[field.name] = field.value_from_object(self)
```

#### Exception Handling Bugs:

```python
# patient/views.py:204, 256
except TypeError or ValueError or AttributeError:  # ❌ ONLY CATCHES TypeError!

# Fixed:
except (TypeError, ValueError, AttributeError):  # ✅
```

Found in 4 files - need systematic fix.

#### request.is_ajax() Deprecation:

```python
# Removed in Django 4.0
if request.is_ajax():  # ❌

# Replace with:
def is_ajax(request):
    return request.headers.get('X-Requested-With') == 'XMLHttpRequest'
```

---

## Phase 2: Demographics Module Migration (Week 2)

### 2.1 Module Structure

Create new top-level `demographics/` module:

```
demographics/
├── __init__.py
├── apps.py
├── models.py (parent Demographics model)
├── urls.py
├── views.py
├── tests/
├── contact/           # Patient addresses
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   └── urls.py
├── phone/             # Phone numbers
│   ├── models.py
│   ├── views.py
│   └── urls.py
├── guardian/          # Guardian information
│   ├── models.py
│   ├── views.py
│   └── urls.py
├── email_and_fax/     # Email/Fax contact
│   ├── models.py
│   ├── views.py
│   └── urls.py
└── templates/
    └── demographics/
```

### 2.2 Model Migrations

**Parent Model:**
```python
class Demographics(AuShadhaBaseModel):
    patient = models.OneToOneField(PatientDetail, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    marital_status = models.CharField(max_length=50)
    ethnicity = models.CharField(max_length=100)
    # ... other demographics fields
```

**Related Models:**
- `Contact` (addresses)
- `Phone` (phone numbers - multiple)
- `Guardian` (emergency contacts)
- `EmailAndFax` (digital contact)

### 2.3 Update Patient Model

Add relationship support back to `PatientDetail`:

```python
class PatientDetail(AuShadhaBaseModel):
    # ... existing fields ...

    _can_add_list_or_json = [
        'demographics',
        'contact',
        'phone',
        'guardian',
        'email_and_fax',
        # ... will add more in later phases
    ]
```

---

## Phase 3: History Module Migration (Week 3)

### 3.1 History Module Structure

```
history/
├── __init__.py
├── apps.py
├── medical_history/      # Medical conditions
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   └── templates/
├── surgical_history/     # Surgical procedures
│   ├── models.py
│   ├── views.py
│   └── templates/
├── family_history/       # Hereditary conditions
│   ├── models.py
│   ├── views.py
│   └── templates/
├── social_history/       # Lifestyle factors
│   ├── models.py
│   ├── views.py
│   └── templates/
└── obs_and_gyn/         # OB/GYN history
    ├── models.py
    ├── views.py
    └── templates/
```

### 3.2 Key Models

```python
class MedicalHistory(AuShadhaBaseModel):
    patient = models.ForeignKey(PatientDetail, on_delete=models.CASCADE)
    condition = models.CharField(max_length=500)
    icd10_code = models.ForeignKey('registry.ICD10', null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50)  # Active, Resolved, Chronic
    notes = models.TextField()
```

Similar for:
- `SurgicalHistory`
- `FamilyHistory`
- `SocialHistory`
- `ObstetricHistoryDetail`

---

## Phase 4: Visit Management (Week 4-5)

### 4.1 Visit Module Structure

**Most Complex Module** - Core clinical workflow

```
visit/
├── __init__.py
├── apps.py
├── visit/                    # Main visit/encounter
│   ├── models.py            # VisitDetail
│   ├── views.py
│   └── templates/
├── visit_complaints/         # Chief complaints
│   ├── models.py
│   └── views.py
├── visit_hpi/               # History of Present Illness
│   ├── models.py
│   └── views.py
├── visit_ros/               # Review of Systems
│   ├── models.py
│   └── views.py
├── visit_phyexam/           # Physical Examination
│   ├── models.py
│   └── views.py
├── visit_assessment_and_plan/  # Assessment & Plan
│   ├── models.py
│   └── views.py
├── visit_soap/              # SOAP note generation
│   ├── models.py
│   └── views.py
├── visit_prescription/      # Prescriptions
│   ├── models.py
│   └── views.py
├── visit_imaging/           # Imaging orders
│   ├── models.py
│   └── views.py
└── visit_inv/              # Lab investigations
    ├── models.py
    └── views.py
```

### 4.2 Core Visit Model

```python
class VisitDetail(AuShadhaBaseModel):
    patient = models.ForeignKey(PatientDetail, on_delete=models.CASCADE)
    visit_date = models.DateField()
    visit_time = models.TimeField()
    visit_type = models.CharField(max_length=50)  # OPD, Follow-up, Emergency
    provider = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20)  # Active, Completed, Cancelled

    # Relationships to visit components
    # complaints, hpi, ros, physical_exam, assessment, prescriptions, etc.
```

### 4.3 SOAP Note Components

- **S** (Subjective): `VisitComplaint`, `VisitHPI`
- **O** (Objective): `VisitPhyExam`, `VisitInv`, `VisitImaging`
- **A** (Assessment): Diagnosis codes, assessment
- **P** (Plan): `VisitPrescription`, procedures, follow-up

---

## Phase 5: Medication & Allergy Management (Week 6)

### 5.1 Medication List Module

```
medication_list/
├── __init__.py
├── apps.py
├── models.py              # MedicationList
├── views.py
├── forms.py
├── urls.py
├── templates/
│   └── medication_list/
└── tests/
```

**Key Model:**
```python
class MedicationList(AuShadhaBaseModel):
    patient = models.ForeignKey(PatientDetail, on_delete=models.CASCADE)
    drug = models.ForeignKey('registry.DrugDB', null=True, blank=True)
    drug_name = models.CharField(max_length=500)
    dose = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)
    route = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50)  # Active, Discontinued, Completed
    prescribed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    notes = models.TextField(blank=True)
```

### 5.2 Allergy List Module

```
allergy_list/
├── __init__.py
├── apps.py
├── models.py              # Allergy
├── views.py
├── forms.py
├── urls.py
├── templates/
│   └── allergy_list/
└── tests/
```

**Key Model:**
```python
class Allergy(AuShadhaBaseModel):
    patient = models.ForeignKey(PatientDetail, on_delete=models.CASCADE)
    allergen = models.CharField(max_length=500)
    allergen_type = models.CharField(max_length=100)  # Drug, Food, Environmental
    reaction = models.TextField()
    severity = models.CharField(max_length=50)  # Mild, Moderate, Severe, Life-threatening
    onset_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50)  # Active, Inactive, Resolved
```

---

## Phase 6: Immunisation Module (Week 7)

### 6.1 Immunisation Structure

```
immunisation/
├── __init__.py
├── apps.py
├── models.py              # Immunisation
├── views.py
├── forms.py
├── urls.py
├── templates/
│   └── immunisation/
└── tests/
```

**Key Model:**
```python
class Immunisation(AuShadhaBaseModel):
    patient = models.ForeignKey(PatientDetail, on_delete=models.CASCADE)
    vaccine = models.ForeignKey('registry.VaccineRegistry', null=True, blank=True)
    vaccine_name = models.CharField(max_length=500)
    dose_number = models.IntegerField()
    administration_date = models.DateField()
    administered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    site = models.CharField(max_length=100)  # Injection site
    lot_number = models.CharField(max_length=100)
    expiry_date = models.DateField()
    notes = models.TextField(blank=True)
```

---

## Phase 7: Testing & Quality Assurance (Week 8)

### 7.1 Test Coverage Requirements

**Minimum 80% code coverage** for:
- Models (100% target)
- Views (80% target)
- Forms (90% target)
- URL routing (100% target)

### 7.2 Test Structure

```
tests/
├── conftest.py                    # Pytest fixtures
├── factories.py                   # Factory Boy factories
├── test_models/
│   ├── test_patient.py
│   ├── test_demographics.py
│   ├── test_history.py
│   ├── test_visit.py
│   ├── test_medication.py
│   ├── test_allergy.py
│   └── test_immunisation.py
├── test_views/
│   ├── test_patient_views.py
│   ├── test_visit_views.py
│   └── ...
└── test_integration/
    ├── test_patient_workflow.py
    ├── test_visit_workflow.py
    └── test_prescription_workflow.py
```

### 7.3 Critical Test Scenarios

**Patient Registration:**
- Create patient with unique hospital ID
- Prevent duplicate hospital IDs
- Full name generation
- Age calculation from DOB

**Visit Workflow:**
- Create visit → Add complaints → HPI → Physical exam → Assessment → Prescription
- Generate SOAP note
- Visit completion
- Visit cancellation

**Medication Safety:**
- Drug interaction checking (if DB supports)
- Allergy cross-checking
- Duplicate prescription detection

**Data Integrity:**
- Foreign key constraints
- Cascade deletion behavior
- Unique constraints
- Required field validation

---

## Phase 8: Documentation & Deployment (Week 9)

### 8.1 Documentation Requirements

**Create/Update:**
1. `README.md` - Updated installation for 2.0
2. `INSTALLATION.md` - Detailed setup guide
3. `MIGRATION_FROM_1.0.md` - Data migration guide
4. `API_DOCUMENTATION.md` - If implementing REST API
5. `USER_MANUAL.md` - Clinical workflow guide
6. `DEVELOPER_GUIDE.md` - Contributing guidelines

**Sphinx Documentation:**
- Update API docs
- Add module documentation
- Clinical workflow diagrams
- Database schema documentation

### 8.2 Deployment Checklist

**Pre-deployment:**
- [ ] All security fixes implemented
- [ ] Environment variables configured
- [ ] Database migrations tested
- [ ] Static files collected
- [ ] Test coverage >80%
- [ ] Load testing completed
- [ ] Backup strategy implemented

**Production Settings:**
- [ ] `DEBUG = False`
- [ ] `ALLOWED_HOSTS` configured
- [ ] Secret key from environment
- [ ] Database credentials from environment
- [ ] HTTPS enforced
- [ ] Security headers enabled
- [ ] Logging configured

**Post-deployment:**
- [ ] Data migration from 1.0 (if applicable)
- [ ] User acceptance testing
- [ ] Performance monitoring
- [ ] Error tracking (Sentry recommended)
- [ ] Database backup verification

---

## Implementation Priorities

### Phase Priority Matrix

| Phase | Priority | Impact | Effort | Start Week |
|-------|----------|--------|--------|------------|
| Security Fixes | 🔴 CRITICAL | HIGH | LOW | Week 1 |
| Dependency Update | 🔴 CRITICAL | HIGH | MEDIUM | Week 1 |
| Code Fixes | 🟠 HIGH | HIGH | LOW | Week 1 |
| Demographics | 🟠 HIGH | HIGH | MEDIUM | Week 2 |
| History | 🟠 HIGH | HIGH | MEDIUM | Week 3 |
| Visit Management | 🔴 CRITICAL | HIGH | HIGH | Week 4-5 |
| Medication/Allergy | 🔴 CRITICAL | HIGH | MEDIUM | Week 6 |
| Immunisation | 🟡 MEDIUM | MEDIUM | MEDIUM | Week 7 |
| Testing | 🔴 CRITICAL | HIGH | HIGH | Week 8 |
| Documentation | 🟡 MEDIUM | MEDIUM | MEDIUM | Week 9 |
| Utility Apps | 🟢 LOW | LOW | MEDIUM | Future |

---

## Risk Assessment

### High Risk Areas

| Risk | Impact | Mitigation |
|------|--------|------------|
| **Data Loss during migration** | CATASTROPHIC | Full backup before any migration, test on copy first |
| **Breaking changes in Django 4.2** | HIGH | Comprehensive test suite, incremental upgrades |
| **Security vulnerabilities in production** | HIGH | Fix all security issues before ANY deployment |
| **Performance degradation** | MEDIUM | Load testing, database indexing, query optimization |
| **Incomplete feature migration** | HIGH | Use 1.0 as reference, verify feature parity |

### Medium Risk Areas

| Risk | Impact | Mitigation |
|------|--------|------------|
| **UI/UX changes** | MEDIUM | Keep Dojo widgets compatible, gradual UI updates |
| **Test coverage gaps** | MEDIUM | Enforce 80% minimum coverage, code review |
| **Documentation outdated** | MEDIUM | Update docs in parallel with code changes |

---

## Success Criteria

### Technical Metrics
- ✅ Django 4.2 LTS compatibility
- ✅ Python 3.11+ support
- ✅ Zero critical security vulnerabilities
- ✅ >80% test coverage
- ✅ All deprecated APIs replaced
- ✅ CI/CD pipeline functional

### Functional Metrics
- ✅ All 1.0 modules migrated
- ✅ Feature parity with 1.0
- ✅ No broken imports
- ✅ All CRUD operations working
- ✅ Patient workflow complete (registration → visit → prescription)
- ✅ SOAP note generation working

### Performance Metrics
- ✅ Page load <2 seconds
- ✅ API response <500ms
- ✅ Support 1000+ patient records
- ✅ Support 100 concurrent users

---

## Resources Required

### Development Team
- **1 Backend Developer** (Full-time, 9 weeks)
- **1 QA Engineer** (Part-time, weeks 3-9)
- **1 Medical Domain Expert** (Consultation, as needed)

### Tools & Services
- GitHub for version control
- PostgreSQL database server
- CI/CD platform (GitHub Actions recommended)
- Test environment (staging server)
- Code quality tools (Black, Flake8, MyPy)

### Infrastructure
- Development environment
- Staging environment (clone of production)
- Production environment (secured, HTTPS, backups)

---

## Timeline Summary

| Week | Phase | Deliverables |
|------|-------|-------------|
| 1 | Foundation | Security fixes, dependency updates, code fixes |
| 2 | Demographics | Demographics module complete + tests |
| 3 | History | History module complete + tests |
| 4-5 | Visit | Visit management complete + tests |
| 6 | Medication/Allergy | Both modules complete + tests |
| 7 | Immunisation | Immunisation module complete + tests |
| 8 | Testing | Full test suite, integration tests, QA |
| 9 | Documentation | Docs, deployment, production release |

**Total Duration: 9 weeks**

---

## Next Steps

1. **Review this plan** with stakeholders
2. **Approve budget** and resources
3. **Set up development environment**
4. **Begin Phase 1** (Security & Foundation)
5. **Establish weekly progress reviews**
6. **Create GitHub project board** for tracking

---

## Questions to Answer Before Starting

1. Is there existing production data in 1.0 that needs migration?
2. What is the target Python version? (Recommend 3.11+)
3. What is the target Django version? (Recommend 4.2 LTS)
4. Are there any custom modifications to 1.0 that aren't in the repo?
5. What is the deployment environment? (Linux/Docker/Cloud?)
6. What is the acceptable downtime window for deployment?
7. What are the backup and disaster recovery requirements?
8. Are there any compliance requirements (HIPAA, GDPR, etc.)?
9. What is the expected user load (concurrent users, patients)?
10. Is there a preference for REST API implementation?

---

**Document Version:** 1.0
**Created:** November 5, 2025
**Author:** Claude (AI Assistant)
**Project:** AuShadha 2.0 Migration
**Repository:** https://github.com/dreaswar/AuShadha2.0
