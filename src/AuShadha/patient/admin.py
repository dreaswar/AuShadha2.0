from django.contrib import admin
from .models import (
    PatientDetail,
    PatientModule,
    ModuleAssignmentRule,
    PatientTag,
)


@admin.register(PatientDetail)
class PatientDetailAdmin(admin.ModelAdmin):
    """Admin interface for Patient Details"""
    list_display = [
        'patient_hospital_id',
        'full_name',
        'age',
        'sex',
        'parent_clinic',
    ]
    list_filter = ['sex', 'parent_clinic']
    search_fields = [
        'patient_hospital_id',
        'first_name',
        'middle_name',
        'last_name',
        'full_name',
    ]
    readonly_fields = ['full_name']

    fieldsets = (
        ('Basic Information', {
            'fields': (
                'patient_hospital_id',
                'first_name',
                'middle_name',
                'last_name',
                'full_name',
            )
        }),
        ('Demographics', {
            'fields': ('age', 'sex')
        }),
        ('Clinic', {
            'fields': ('parent_clinic',)
        }),
    )


@admin.register(PatientModule)
class PatientModuleAdmin(admin.ModelAdmin):
    """Admin interface for Patient Modules"""
    list_display = [
        'icon',
        'display_name',
        'name',
        'category',
        'is_active',
        'requires_privilege',
        'sort_order',
    ]
    list_filter = ['category', 'is_active']
    search_fields = ['name', 'display_name', 'description']
    list_editable = ['is_active', 'sort_order']
    ordering = ['sort_order', 'name']

    fieldsets = (
        ('Module Information', {
            'fields': (
                'name',
                'display_name',
                'icon',
                'description',
            )
        }),
        ('Configuration', {
            'fields': (
                'url_pattern',
                'category',
                'is_active',
                'requires_privilege',
                'sort_order',
            )
        }),
    )


class ModuleAssignmentRuleInline(admin.TabularInline):
    """Inline admin for Module Assignment Rules"""
    model = ModuleAssignmentRule
    extra = 1
    fields = [
        'rule_type',
        'priority',
        'is_active',
        'min_age',
        'max_age',
        'sex',
    ]


@admin.register(ModuleAssignmentRule)
class ModuleAssignmentRuleAdmin(admin.ModelAdmin):
    """Admin interface for Module Assignment Rules"""
    list_display = [
        'module',
        'rule_type',
        'priority',
        'is_active',
        'get_criteria_summary',
    ]
    list_filter = ['rule_type', 'is_active', 'module', 'sex']
    search_fields = [
        'module__name',
        'module__display_name',
        'description',
        'icd_codes',
        'patient_tags',
    ]
    list_editable = ['is_active', 'priority']
    ordering = ['-priority', 'rule_type']

    fieldsets = (
        ('Rule Information', {
            'fields': (
                'module',
                'rule_type',
                'priority',
                'is_active',
                'description',
            )
        }),
        ('Age Criteria', {
            'fields': ('min_age', 'max_age'),
            'classes': ('collapse',),
            'description': 'Used for age_range rule type'
        }),
        ('Sex Criteria', {
            'fields': ('sex',),
            'classes': ('collapse',),
            'description': 'Used for sex rule type'
        }),
        ('Diagnosis Criteria', {
            'fields': ('icd_codes',),
            'classes': ('collapse',),
            'description': 'Comma-separated ICD-10 codes (e.g., E11.9, I10)'
        }),
        ('Tag Criteria', {
            'fields': ('patient_tags',),
            'classes': ('collapse',),
            'description': 'Comma-separated tags (e.g., diabetic, hypertensive)'
        }),
        ('Procedure Criteria', {
            'fields': ('procedure_codes',),
            'classes': ('collapse',),
            'description': 'Comma-separated procedure codes'
        }),
        ('Specific Assignment', {
            'fields': ('assigned_doctor', 'assigned_patient'),
            'classes': ('collapse',),
            'description': 'Assign to specific doctor or patient'
        }),
    )

    def get_criteria_summary(self, obj):
        """Display a summary of the rule criteria"""
        if obj.rule_type == 'age_range':
            min_age = obj.min_age if obj.min_age else '0'
            max_age = obj.max_age if obj.max_age else '∞'
            return f"Age: {min_age}-{max_age}"
        elif obj.rule_type == 'sex':
            return f"Sex: {obj.sex}"
        elif obj.rule_type == 'diagnosis':
            codes = obj.icd_codes[:30] if obj.icd_codes else ''
            return f"ICD: {codes}..." if len(codes) >= 30 else f"ICD: {codes}"
        elif obj.rule_type == 'tag':
            tags = obj.patient_tags[:30] if obj.patient_tags else ''
            return f"Tags: {tags}..." if len(tags) >= 30 else f"Tags: {tags}"
        elif obj.rule_type == 'doctor':
            return f"Doctor: {obj.assigned_doctor}" if obj.assigned_doctor else "No doctor"
        elif obj.rule_type == 'patient':
            return f"Patient: {obj.assigned_patient}" if obj.assigned_patient else "No patient"
        elif obj.rule_type == 'global':
            return "All patients"
        return "-"

    get_criteria_summary.short_description = "Criteria"


@admin.register(PatientTag)
class PatientTagAdmin(admin.ModelAdmin):
    """Admin interface for Patient Tags"""
    list_display = [
        'patient',
        'tag',
        'added_by',
    ]
    list_filter = ['tag', 'added_by']
    search_fields = [
        'patient__full_name',
        'patient__patient_hospital_id',
        'tag',
        'notes',
    ]

    fieldsets = (
        ('Tag Information', {
            'fields': (
                'patient',
                'tag',
                'added_by',
                'notes',
            )
        }),
    )
