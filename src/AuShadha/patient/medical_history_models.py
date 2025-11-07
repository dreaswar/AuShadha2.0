################################################################################
# PROJECT      : AuShadha2.0
# Description  : Medical History Models for Patient Module
# Author       : Dr. Easwar T R
# Date         : 07-11-2025
# Licence      : GNU GPL V3. Please see AuShadha/LICENSE.txt
################################################################################

from django.db import models
from django.contrib.auth.models import User
from aushadha_base_models.models import AuShadhaBaseModel, AuShadhaBaseModelForm
from .models import PatientDetail


class PastMedicalHistory(AuShadhaBaseModel):
    """
    Model for recording past medical conditions, illnesses, diagnoses, and surgeries
    """
    patient = models.ForeignKey(PatientDetail, on_delete=models.CASCADE, related_name='past_medical_history')

    CONDITION_TYPE_CHOICES = (
        ('illness', 'Illness/Disease'),
        ('surgery', 'Surgery/Procedure'),
        ('injury', 'Injury/Trauma'),
        ('hospitalization', 'Hospitalization'),
        ('other', 'Other'),
    )

    condition_type = models.CharField(
        max_length=20,
        choices=CONDITION_TYPE_CHOICES,
        default='illness',
        help_text="Type of medical condition"
    )

    condition_name = models.CharField(
        max_length=200,
        help_text="Name of the condition, surgery, or procedure"
    )

    icd_code = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="ICD-10 code if applicable"
    )

    date_diagnosed = models.DateField(
        blank=True,
        null=True,
        help_text="Date when condition was diagnosed or procedure was performed"
    )

    status = models.CharField(
        max_length=20,
        choices=(
            ('active', 'Active'),
            ('resolved', 'Resolved'),
            ('chronic', 'Chronic'),
        ),
        default='resolved'
    )

    notes = models.TextField(
        blank=True,
        null=True,
        help_text="Additional notes about the condition"
    )

    class Meta:
        verbose_name = "Past Medical History"
        verbose_name_plural = "Past Medical History"
        ordering = ['-date_diagnosed']

    def __str__(self):
        return f"{self.patient.full_name} - {self.condition_name}"


class CurrentMedication(AuShadhaBaseModel):
    """
    Model for recording current medications
    """
    patient = models.ForeignKey(PatientDetail, on_delete=models.CASCADE, related_name='current_medications')

    medication_name = models.CharField(
        max_length=200,
        help_text="Name of the medication"
    )

    dosage = models.CharField(
        max_length=100,
        help_text="Dosage (e.g., 500mg, 10ml)"
    )

    frequency = models.CharField(
        max_length=100,
        help_text="Frequency (e.g., twice daily, once a week)"
    )

    route = models.CharField(
        max_length=50,
        choices=(
            ('oral', 'Oral'),
            ('iv', 'Intravenous'),
            ('im', 'Intramuscular'),
            ('topical', 'Topical'),
            ('inhaled', 'Inhaled'),
            ('other', 'Other'),
        ),
        default='oral'
    )

    start_date = models.DateField(
        blank=True,
        null=True,
        help_text="Date medication was started"
    )

    prescribed_by = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Name of prescribing physician"
    )

    indication = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Reason for taking this medication"
    )

    notes = models.TextField(
        blank=True,
        null=True,
        help_text="Additional notes"
    )

    class Meta:
        verbose_name = "Current Medication"
        verbose_name_plural = "Current Medications"
        ordering = ['medication_name']

    def __str__(self):
        return f"{self.patient.full_name} - {self.medication_name} {self.dosage}"


class Allergy(AuShadhaBaseModel):
    """
    Model for recording allergies and adverse reactions
    """
    patient = models.ForeignKey(PatientDetail, on_delete=models.CASCADE, related_name='allergies')

    ALLERGY_TYPE_CHOICES = (
        ('drug', 'Drug/Medication'),
        ('food', 'Food'),
        ('environmental', 'Environmental'),
        ('other', 'Other'),
    )

    allergy_type = models.CharField(
        max_length=20,
        choices=ALLERGY_TYPE_CHOICES,
        default='drug'
    )

    allergen = models.CharField(
        max_length=200,
        help_text="Name of the allergen"
    )

    SEVERITY_CHOICES = (
        ('mild', 'Mild'),
        ('moderate', 'Moderate'),
        ('severe', 'Severe'),
        ('life_threatening', 'Life Threatening'),
    )

    severity = models.CharField(
        max_length=20,
        choices=SEVERITY_CHOICES,
        default='mild'
    )

    reaction = models.TextField(
        help_text="Description of the allergic reaction"
    )

    date_identified = models.DateField(
        blank=True,
        null=True,
        help_text="Date when allergy was identified"
    )

    notes = models.TextField(
        blank=True,
        null=True,
        help_text="Additional notes"
    )

    class Meta:
        verbose_name = "Allergy"
        verbose_name_plural = "Allergies"
        ordering = ['-severity', 'allergen']

    def __str__(self):
        return f"{self.patient.full_name} - {self.allergen} ({self.get_allergy_type_display()})"


class FamilyHistory(AuShadhaBaseModel):
    """
    Model for recording family medical history
    """
    patient = models.ForeignKey(PatientDetail, on_delete=models.CASCADE, related_name='family_history')

    RELATIONSHIP_CHOICES = (
        ('father', 'Father'),
        ('mother', 'Mother'),
        ('brother', 'Brother'),
        ('sister', 'Sister'),
        ('grandfather_paternal', 'Grandfather (Paternal)'),
        ('grandmother_paternal', 'Grandmother (Paternal)'),
        ('grandfather_maternal', 'Grandfather (Maternal)'),
        ('grandmother_maternal', 'Grandmother (Maternal)'),
        ('uncle', 'Uncle'),
        ('aunt', 'Aunt'),
        ('child', 'Child'),
        ('other', 'Other'),
    )

    relationship = models.CharField(
        max_length=30,
        choices=RELATIONSHIP_CHOICES
    )

    condition = models.CharField(
        max_length=200,
        help_text="Medical condition"
    )

    age_of_onset = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="Age when condition developed"
    )

    notes = models.TextField(
        blank=True,
        null=True,
        help_text="Additional notes"
    )

    class Meta:
        verbose_name = "Family History"
        verbose_name_plural = "Family History"
        ordering = ['relationship']

    def __str__(self):
        return f"{self.patient.full_name} - {self.get_relationship_display()}: {self.condition}"


class SocialHistory(AuShadhaBaseModel):
    """
    Model for recording social history (smoking, alcohol, etc.)
    Note: Typically one record per patient, updated as needed
    """
    patient = models.OneToOneField(
        PatientDetail,
        on_delete=models.CASCADE,
        related_name='social_history'
    )

    # Smoking
    smoking_status = models.CharField(
        max_length=20,
        choices=(
            ('never', 'Never Smoked'),
            ('former', 'Former Smoker'),
            ('current', 'Current Smoker'),
        ),
        default='never'
    )

    smoking_details = models.TextField(
        blank=True,
        null=True,
        help_text="Details about smoking (packs per day, years smoked, quit date, etc.)"
    )

    # Alcohol
    alcohol_use = models.CharField(
        max_length=20,
        choices=(
            ('none', 'No Alcohol Use'),
            ('occasional', 'Occasional'),
            ('moderate', 'Moderate'),
            ('heavy', 'Heavy'),
        ),
        default='none'
    )

    alcohol_details = models.TextField(
        blank=True,
        null=True,
        help_text="Details about alcohol use (drinks per week, type, etc.)"
    )

    # Drug Use
    drug_use = models.CharField(
        max_length=20,
        choices=(
            ('none', 'No Drug Use'),
            ('former', 'Former User'),
            ('current', 'Current User'),
        ),
        default='none'
    )

    drug_details = models.TextField(
        blank=True,
        null=True,
        help_text="Details about drug use"
    )

    # Exercise
    exercise_frequency = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Exercise frequency (e.g., 3 times per week)"
    )

    # Occupation
    occupation = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    occupational_hazards = models.TextField(
        blank=True,
        null=True,
        help_text="Any occupational hazards or exposures"
    )

    # Other
    marital_status = models.CharField(
        max_length=20,
        choices=(
            ('single', 'Single'),
            ('married', 'Married'),
            ('divorced', 'Divorced'),
            ('widowed', 'Widowed'),
            ('other', 'Other'),
        ),
        blank=True,
        null=True
    )

    living_situation = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Living situation (lives alone, with family, etc.)"
    )

    notes = models.TextField(
        blank=True,
        null=True,
        help_text="Additional social history notes"
    )

    class Meta:
        verbose_name = "Social History"
        verbose_name_plural = "Social History"

    def __str__(self):
        return f"{self.patient.full_name} - Social History"


# Model Forms
class PastMedicalHistoryForm(AuShadhaBaseModelForm):
    class Meta:
        model = PastMedicalHistory
        exclude = ('patient',)


class CurrentMedicationForm(AuShadhaBaseModelForm):
    class Meta:
        model = CurrentMedication
        exclude = ('patient',)


class AllergyForm(AuShadhaBaseModelForm):
    class Meta:
        model = Allergy
        exclude = ('patient',)


class FamilyHistoryForm(AuShadhaBaseModelForm):
    class Meta:
        model = FamilyHistory
        exclude = ('patient',)


class SocialHistoryForm(AuShadhaBaseModelForm):
    class Meta:
        model = SocialHistory
        exclude = ('patient',)
