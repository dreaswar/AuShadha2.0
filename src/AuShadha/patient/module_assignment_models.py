################################################################################
# PROJECT      : AuShadha2.0
# Description  : Patient Module Assignment Models
# Author       : Dr. Easwar T R
# Date         : 10-11-2025
# Licence      : GNU GPL V3. Please see AuShadha/LICENSE.txt
################################################################################

from django.db import models
from django.contrib.auth.models import User
from aushadha_base_models.models import AuShadhaBaseModel
from patient.models import PatientDetail


class PatientModule(AuShadhaBaseModel):
    """
    Defines available modules that can be assigned to patients
    """
    MODULE_CATEGORY_CHOICES = (
        ('clinical', 'Clinical'),
        ('diagnostic', 'Diagnostic'),
        ('screening', 'Screening'),
        ('administrative', 'Administrative'),
        ('other', 'Other'),
    )

    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Module name (e.g., 'Medical History', 'Immunizations')"
    )

    display_name = models.CharField(
        max_length=100,
        help_text="Display name shown in UI"
    )

    icon = models.CharField(
        max_length=10,
        default='📋',
        help_text="Emoji or icon for the module"
    )

    url_pattern = models.CharField(
        max_length=200,
        help_text="URL pattern with {patient_id} placeholder"
    )

    category = models.CharField(
        max_length=20,
        choices=MODULE_CATEGORY_CHOICES,
        default='clinical'
    )

    description = models.TextField(
        blank=True,
        help_text="Module description"
    )

    is_active = models.BooleanField(
        default=True,
        help_text="Is this module available?"
    )

    requires_privilege = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Required user privilege/permission"
    )

    sort_order = models.IntegerField(
        default=0,
        help_text="Display order (lower numbers first)"
    )

    class Meta:
        verbose_name = "Patient Module"
        verbose_name_plural = "Patient Modules"
        ordering = ['sort_order', 'name']

    def __str__(self):
        return f"{self.icon} {self.display_name}"


class ModuleAssignmentRule(AuShadhaBaseModel):
    """
    Rules for automatically assigning modules to patients
    """
    RULE_TYPE_CHOICES = (
        ('age_range', 'Age Range'),
        ('sex', 'Sex'),
        ('diagnosis', 'Diagnosis (ICD Code)'),
        ('tag', 'Patient Tag'),
        ('procedure', 'Procedure Done'),
        ('doctor', 'Specific Doctor'),
        ('patient', 'Specific Patient'),
        ('global', 'Global (All Patients)'),
    )

    module = models.ForeignKey(
        PatientModule,
        on_delete=models.CASCADE,
        related_name='assignment_rules'
    )

    rule_type = models.CharField(
        max_length=20,
        choices=RULE_TYPE_CHOICES
    )

    is_active = models.BooleanField(
        default=True
    )

    priority = models.IntegerField(
        default=0,
        help_text="Higher priority rules checked first"
    )

    # Age-based criteria
    min_age = models.IntegerField(
        blank=True,
        null=True,
        help_text="Minimum age for this rule"
    )

    max_age = models.IntegerField(
        blank=True,
        null=True,
        help_text="Maximum age for this rule"
    )

    # Sex-based criteria
    sex = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        choices=(('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others'))
    )

    # Diagnosis-based criteria (ICD codes)
    icd_codes = models.TextField(
        blank=True,
        null=True,
        help_text="Comma-separated ICD-10 codes (e.g., E11.9, I10)"
    )

    # Tag-based criteria
    patient_tags = models.TextField(
        blank=True,
        null=True,
        help_text="Comma-separated tags (e.g., diabetic, hypertensive)"
    )

    # Procedure-based criteria
    procedure_codes = models.TextField(
        blank=True,
        null=True,
        help_text="Comma-separated procedure codes"
    )

    # Doctor-specific assignment
    assigned_doctor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='module_assignments',
        help_text="Module available only for this doctor's patients"
    )

    # Patient-specific assignment
    assigned_patient = models.ForeignKey(
        PatientDetail,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='specific_module_assignments',
        help_text="Module assigned to specific patient"
    )

    description = models.TextField(
        blank=True,
        help_text="Description of this rule"
    )

    class Meta:
        verbose_name = "Module Assignment Rule"
        verbose_name_plural = "Module Assignment Rules"
        ordering = ['-priority', 'rule_type']

    def __str__(self):
        return f"{self.module.display_name} - {self.get_rule_type_display()}"

    def matches_patient(self, patient, user=None):
        """
        Check if this rule matches the given patient
        """
        if not self.is_active:
            return False

        # Check rule type
        if self.rule_type == 'global':
            return True

        if self.rule_type == 'patient':
            return self.assigned_patient == patient

        if self.rule_type == 'doctor':
            if not user or not self.assigned_doctor:
                return False
            # Check if patient's primary doctor is the assigned doctor
            # (This would need a primary_doctor field on PatientDetail)
            return self.assigned_doctor == user

        if self.rule_type == 'age_range':
            if not patient.age:
                return False
            try:
                age = int(patient.age.split()[0])  # Extract number from "45 years"
                if self.min_age and age < self.min_age:
                    return False
                if self.max_age and age > self.max_age:
                    return False
                return True
            except (ValueError, IndexError):
                return False

        if self.rule_type == 'sex':
            return self.sex == patient.sex

        if self.rule_type == 'diagnosis':
            # Check if patient has any of the specified ICD codes
            # This would require a PatientDiagnosis model
            if not self.icd_codes:
                return False
            # TODO: Implement diagnosis checking when PatientDiagnosis model exists
            return False

        if self.rule_type == 'tag':
            # Check if patient has any of the specified tags
            # This would require a PatientTag model
            if not self.patient_tags:
                return False
            # TODO: Implement tag checking when PatientTag model exists
            return False

        if self.rule_type == 'procedure':
            # Check if patient has had any of the specified procedures
            # This would require a PatientProcedure model
            if not self.procedure_codes:
                return False
            # TODO: Implement procedure checking when PatientProcedure model exists
            return False

        return False


class PatientTag(AuShadhaBaseModel):
    """
    Tags for categorizing patients (e.g., diabetic, hypertensive, high-risk)
    """
    patient = models.ForeignKey(
        PatientDetail,
        on_delete=models.CASCADE,
        related_name='tags'
    )

    tag = models.CharField(
        max_length=50,
        help_text="Tag name"
    )

    added_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='patient_tags_added'
    )

    notes = models.TextField(
        blank=True,
        help_text="Additional notes about this tag"
    )

    class Meta:
        verbose_name = "Patient Tag"
        verbose_name_plural = "Patient Tags"
        unique_together = ['patient', 'tag']

    def __str__(self):
        return f"{self.patient.full_name} - {self.tag}"


# Helper function to get modules for a patient
def get_patient_modules(patient, user=None):
    """
    Get all modules that should be displayed for a patient
    based on assignment rules
    """
    modules = []

    # Get all active modules
    active_modules = PatientModule.objects.filter(is_active=True)

    for module in active_modules:
        # Check if any rule matches
        rules = module.assignment_rules.filter(is_active=True).order_by('-priority')

        for rule in rules:
            if rule.matches_patient(patient, user):
                # Check user privileges if required
                if module.requires_privilege and user:
                    if not user.has_perm(module.requires_privilege):
                        break

                modules.append({
                    'icon': module.icon,
                    'name': module.display_name,
                    'url': module.url_pattern.format(patient_id=patient.id),
                    'category': module.category,
                    'disabled': False
                })
                break  # Module matched, no need to check more rules

    return modules
