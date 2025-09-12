from django.db import models

class ListOfStructure(models.Model):
    structure = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.structure


# models.py
from django.db import models

class LoadCondition(models.Model):
    description = models.CharField(max_length=100)
    temperature = models.FloatField(verbose_name="°F")
    ice_radial = models.FloatField(verbose_name="Radial (in)")
    wind_pressure = models.FloatField(verbose_name="Pressure (psf)")
    angle_factor = models.FloatField()
    transverse_factor = models.FloatField()
    vertical_factor = models.FloatField()
    longitudinal_factor = models.FloatField()
    
    def __str__(self):
        return self.description

class AttachmentLoad(models.Model):
    LOAD_CASE_CHOICES = [
        ('LC1', 'LC1, NESC LIGHT (250B)'),
        ('LC2', 'LC2, NESC EXTREME WIND (250C)'),
        ('LC3', 'LC3, NESC COMBINED ICE AND WIND (250D)'),
        ('LC4', 'LC4, NORMAL EVERYDAY'),
        ('LC5', 'LC5, 2% POLE DEFLECTION'),
        ('LC6', 'LC6, FULL BREAK (250B)'),
        ('LC7', 'LC7, Full Break (250D)'),
    ]
    
    ATTACHMENT_CHOICES = [
        ('S1', 'S1'),
        ('P1,A', 'P1,A'),
        ('P1,B', 'P1,B'),
        ('P1,C', 'P1,C'),
        ('F1', 'F1'),
        ('D1,A & D2,A', 'D1,A & D2,A'),
        ('D1,B & D2,B', 'D1,B & D2,B'),
        ('D1,C & D2,C', 'D1,C & D2,C'),
        ('N1 & N2', 'N1 & N2'),
        ('C1', 'C1'),
        ('C2', 'C2'),
        ('C3', 'C3'),
        ('C4', 'C4'),
    ]
    
    load_case = models.CharField(max_length=3, choices=LOAD_CASE_CHOICES)
    attachment = models.CharField(max_length=20, choices=ATTACHMENT_CHOICES)
    vertical_load = models.FloatField(verbose_name="V")
    transverse_load = models.FloatField(verbose_name="T")
    longitudinal_load = models.FloatField(verbose_name="L")
    
    class Meta:
        unique_together = ('load_case', 'attachment')
    
    def __str__(self):
        return f"{self.get_load_case_display()} - {self.attachment}"

from django.db import models

class MonopoleDeadend(models.Model):
    CIRCUIT_CHOICES = [(i, str(i)) for i in range(1, 11)]

    structure = models.ForeignKey('ListOfStructure', on_delete=models.CASCADE, related_name='monopole_deadends', unique=True)

    num_3_phase_circuits = models.PositiveIntegerField(choices=CIRCUIT_CHOICES)
    num_shield_wires = models.PositiveIntegerField(choices=CIRCUIT_CHOICES)
    num_1_phase_circuits = models.PositiveIntegerField(choices=CIRCUIT_CHOICES)
    num_communication_cables = models.PositiveIntegerField(choices=CIRCUIT_CHOICES)

    def __str__(self):
        return f"MonopoleDeadend {self.id} - Structure: {self.structure}"
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['structure'], name='unique_monopole_per_structure')
        ]

class MonopoleDeadend1(models.Model):
    CIRCUIT_CHOICES = [(i, str(i)) for i in range(1, 11)]

    structure = models.ForeignKey('ListOfStructure', on_delete=models.CASCADE, related_name='monopole_deadends1', unique=True)

    num_3_phase_circuits = models.PositiveIntegerField(choices=CIRCUIT_CHOICES)
    num_shield_wires = models.PositiveIntegerField(choices=CIRCUIT_CHOICES)
    num_1_phase_circuits = models.PositiveIntegerField(choices=CIRCUIT_CHOICES)
    num_communication_cables = models.PositiveIntegerField(choices=CIRCUIT_CHOICES)

    def __str__(self):
        return f"MonopoleDeadend1 {self.id} - Structure: {self.structure}"
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['structure'], name='unique_monopole_per_structure1')
        ]
        
class MonopoleDeadend4(models.Model):
    CIRCUIT_CHOICES = [(i, str(i)) for i in range(1, 11)]

    structure = models.ForeignKey('ListOfStructure', on_delete=models.CASCADE, related_name='monopole_deadends4', unique=True)

    num_3_phase_circuits = models.PositiveIntegerField(choices=CIRCUIT_CHOICES)
    num_shield_wires = models.PositiveIntegerField(choices=CIRCUIT_CHOICES)
    num_1_phase_circuits = models.PositiveIntegerField(choices=CIRCUIT_CHOICES)
    num_communication_cables = models.PositiveIntegerField(choices=CIRCUIT_CHOICES)

    def __str__(self):
        return f"MonopoleDeadend4 {self.id} - Structure: {self.structure}"
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['structure'], name='unique_monopole_per_structure4')
        ]


class UploadedFile1(models.Model):
    structure = models.ForeignKey(ListOfStructure, on_delete=models.CASCADE, related_name='uploaded_files')
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name} ({self.structure.structure})"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['structure'], name='unique_file_per_structure')
        ]

class UploadedFile3(models.Model):
    structure = models.ForeignKey(ListOfStructure, on_delete=models.CASCADE, related_name='uploaded_files3')
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name} ({self.structure.structure})"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['structure'], name='unique_file_per_structure3')
        ]

class UploadedFile2(models.Model):
    structure = models.ForeignKey(ListOfStructure, on_delete=models.CASCADE, related_name='uploaded_files1')
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name} ({self.structure.structure})"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['structure'], name='unique_file_per_structure1')
        ]
        
        
class UploadedFile4(models.Model):
    structure = models.ForeignKey(ListOfStructure, on_delete=models.CASCADE, related_name='uploaded_files4')
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name} ({self.structure.structure})"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['structure'], name='unique_file_per_structure4')
        ]
        
        
        
class TowerDeadend(models.Model):
    CIRCUIT_CHOICES = [
        (0, "0"),
        (None, "None"),
    ] + [(i, str(i)) for i in range(1, 11)]

    structure = models.ForeignKey(
        'ListOfStructure',
        on_delete=models.CASCADE,
        related_name='tower_deadends',
        unique=True
    )

    num_3_phase_circuits = models.PositiveIntegerField(choices=CIRCUIT_CHOICES,null=True, blank=True)
    num_shield_wires = models.PositiveIntegerField(choices=CIRCUIT_CHOICES,null=True, blank=True)
    num_1_phase_circuits = models.PositiveIntegerField(choices=CIRCUIT_CHOICES,null=True, blank=True)
    num_communication_cables = models.PositiveIntegerField(choices=CIRCUIT_CHOICES,null=True, blank=True)

    def __str__(self):
        return f"TowerDeadend {self.id} - Structure: {self.structure}"
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['structure'], name='unique_tower_per_structure')
        ]


class TowerDeadend3(models.Model):
    CIRCUIT_CHOICES = [(i, str(i)) for i in range(1, 11)]

    structure = models.ForeignKey('ListOfStructure', on_delete=models.CASCADE, related_name='tower_deadends3', unique=True)

    num_3_phase_circuits = models.PositiveIntegerField(choices=CIRCUIT_CHOICES)
    num_shield_wires = models.PositiveIntegerField(choices=CIRCUIT_CHOICES)
    num_1_phase_circuits = models.PositiveIntegerField(choices=CIRCUIT_CHOICES)
    num_communication_cables = models.PositiveIntegerField(choices=CIRCUIT_CHOICES)

    def __str__(self):
        return f"TowerDeadend {self.id} - Structure: {self.structure}"
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['structure'], name='unique_tower_per_structure3')
        ]
        
class TowerDeadend4(models.Model):
    CIRCUIT_CHOICES = [(i, str(i)) for i in range(1, 11)]

    structure = models.ForeignKey('ListOfStructure', on_delete=models.CASCADE, related_name='tower_deadendss', unique=True)

    num_3_phase_circuits = models.PositiveIntegerField(choices=CIRCUIT_CHOICES)
    num_shield_wires = models.PositiveIntegerField(choices=CIRCUIT_CHOICES)
    num_1_phase_circuits = models.PositiveIntegerField(choices=CIRCUIT_CHOICES)
    num_communication_cables = models.PositiveIntegerField(choices=CIRCUIT_CHOICES)

    def __str__(self):
        return f"TowerDeadend {self.id} - Structure: {self.structure}"
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['structure'], name='unique_tower_per_structure4')
        ]
        
class TowerDeadend5(models.Model):
    CIRCUIT_CHOICES = [(i, str(i)) for i in range(1, 11)]

    structure = models.ForeignKey('ListOfStructure', on_delete=models.CASCADE, related_name='tower_deadends5', unique=True)

    num_3_phase_circuits = models.PositiveIntegerField(choices=CIRCUIT_CHOICES)
    num_shield_wires = models.PositiveIntegerField(choices=CIRCUIT_CHOICES)
    num_1_phase_circuits = models.PositiveIntegerField(choices=CIRCUIT_CHOICES)
    num_communication_cables = models.PositiveIntegerField(choices=CIRCUIT_CHOICES)

    def __str__(self):
        return f"TowerDeadend {self.id} - Structure: {self.structure}"
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['structure'], name='unique_tower_per_structure5')
        ]
        
    

class tUploadedFile1(models.Model):
    structure = models.ForeignKey(ListOfStructure, on_delete=models.CASCADE, related_name='tuploaded_files1')
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name} ({self.structure.structure})"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['structure'], name='tunique_file_per_structure1')
        ]
        
        
class tUploadedFile2(models.Model):
    structure = models.ForeignKey(ListOfStructure, on_delete=models.CASCADE, related_name='tuploaded_files2')
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name} ({self.structure.structure})"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['structure'], name='tunique_file_per_structure2')
        ]
        
        
        
class tUploadedFile3(models.Model):
    structure = models.ForeignKey(ListOfStructure, on_delete=models.CASCADE, related_name='tuploaded_files3')
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name} ({self.structure.structure})"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['structure'], name='tunique_file_per_structure3')
        ]
        
        
class tUploadedFile4(models.Model):
    structure = models.ForeignKey(ListOfStructure, on_delete=models.CASCADE, related_name='tuploaded_files4')
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name} ({self.structure.structure})"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['structure'], name='tunique_file_per_structure4')
        ]
        
        
class tUploadedFile5(models.Model):
    structure = models.ForeignKey(ListOfStructure, on_delete=models.CASCADE, related_name='tuploaded_files5')
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name} ({self.structure.structure})"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['structure'], name='tunique_file_per_structure5')
        ]
        
        
        
        
class HDeadend1(models.Model):
    CIRCUIT_CHOICES = [
        (0, "0"),
        (None, "None"),
    ] + [(i, str(i)) for i in range(1, 11)]

    structure = models.ForeignKey(
        'ListOfStructure',
        on_delete=models.CASCADE,
        related_name='h_deadends1',
        unique=True
    )

    num_3_phase_circuits = models.PositiveIntegerField(choices=CIRCUIT_CHOICES, null=True, blank=True)
    num_shield_wires = models.PositiveIntegerField(choices=CIRCUIT_CHOICES, null=True, blank=True)
    num_1_phase_circuits = models.PositiveIntegerField(choices=CIRCUIT_CHOICES, null=True, blank=True)
    num_communication_cables = models.PositiveIntegerField(choices=CIRCUIT_CHOICES, null=True, blank=True)

    def __str__(self):
        return f"HDeadend {self.id} - Structure: {self.structure}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['structure'], name='unique_h_per_structure1')
        ]

        
class hUploadedFile1(models.Model):
    structure = models.ForeignKey(ListOfStructure, on_delete=models.CASCADE, related_name='huploaded_files1')
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name} ({self.structure.structure})"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['structure'], name='hunique_file_per_structure1')
        ]

class LoadCaseGroup(models.Model):
    name = models.CharField(max_length=100)
    structure = models.ForeignKey(ListOfStructure, on_delete=models.CASCADE, related_name='hload_case_groups')
    is_custom = models.BooleanField(default=False)  # Flag to identify custom groups
    
    def __str__(self):
        return self.name

class LoadCase(models.Model):
    name = models.CharField(max_length=100)
    group = models.ForeignKey(LoadCaseGroup, on_delete=models.CASCADE, related_name='load_cases', null=True, blank=True)
    structure = models.ForeignKey(ListOfStructure, on_delete=models.CASCADE, related_name='hload_cases')
    
    def __str__(self):
        return self.name
    
class BufferConfiguration(models.Model):
    name = models.CharField(max_length=100, default="Default Buffer Config")
    vertical_buffer = models.FloatField(default=0)
    vertical_rounding = models.IntegerField(default=100)
    transverse_buffer = models.FloatField(default=0)
    transverse_rounding = models.IntegerField(default=100)
    longitudinal_buffer = models.FloatField(default=0)
    longitudinal_rounding = models.IntegerField(default=100)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
        
class HDeadend2(models.Model):
    CIRCUIT_CHOICES = [
        (0, "0"),
        (None, "None"),
    ] + [(i, str(i)) for i in range(1, 11)]

    structure = models.ForeignKey(
        'ListOfStructure',
        on_delete=models.CASCADE,
        related_name='h_deadends2',
        unique=True
    )

    num_3_phase_circuits = models.PositiveIntegerField(choices=CIRCUIT_CHOICES, null=True, blank=True)
    num_shield_wires = models.PositiveIntegerField(choices=CIRCUIT_CHOICES, null=True, blank=True)
    num_1_phase_circuits = models.PositiveIntegerField(choices=CIRCUIT_CHOICES, null=True, blank=True)
    num_communication_cables = models.PositiveIntegerField(choices=CIRCUIT_CHOICES, null=True, blank=True)

    def __str__(self):
        return f"HDeadend {self.id} - Structure: {self.structure}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['structure'], name='unique_h_per_structure2')
        ]
        
class hUploadedFile2(models.Model):
    structure = models.ForeignKey(ListOfStructure, on_delete=models.CASCADE, related_name='huploaded_files2')
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name} ({self.structure.structure})"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['structure'], name='hunique_file_per_structure2')
        ]