from django.db import models

class ListOfStructure(models.Model):
    structure = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.structure

class StructureGroup(models.Model):
    name = models.CharField(max_length=100, unique=True)
    structures = models.ManyToManyField(ListOfStructure, related_name='groups')

    def __str__(self):
        return self.name

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


class LoadConditionSelection(models.Model):
    custom_group_name = models.CharField(max_length=100)
    load_condition = models.ForeignKey(LoadCondition, on_delete=models.CASCADE)
    is_selected = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('custom_group_name', 'load_condition')
    
    def __str__(self):
        return f"{self.custom_group_name} - {self.load_condition.description}"
    
    
from django.db import models



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
    structure = models.ForeignKey(ListOfStructure, on_delete=models.CASCADE, related_name='muploaded_files1')
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name} ({self.structure.structure})"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['structure'], name='unique_file_per_structure')
        ]
        

class UploadedFile22(models.Model):
    structure = models.ForeignKey(ListOfStructure, on_delete=models.CASCADE, related_name='muploaded_files22')
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name} ({self.structure.structure})"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['structure'], name='unique_file_per_structure22')
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
    CIRCUIT_CHOICES = [
        (0, "0"),
    ] + [(i, str(i)) for i in range(1, 11)]

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
    CIRCUIT_CHOICES = [
        (0, "0"),
    ] + [(i, str(i)) for i in range(1, 11)]

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
    CIRCUIT_CHOICES = [
        (0, "0"),
    ] + [(i, str(i)) for i in range(1, 11)]

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
        
class HDeadend2(models.Model):             # **************
    CIRCUIT_CHOICES = [
        (0, "0"),
    ] + [(i, str(i)) for i in range(1, 11)]

    structure = models.ForeignKey(
        'ListOfStructure',
        on_delete=models.CASCADE,
        related_name='h_deadends2',             # **************
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
            models.UniqueConstraint(fields=['structure'], name='unique_h_per_structure2')  # **************
        ]

        
class hUploadedFile2(models.Model):
    structure = models.ForeignKey(ListOfStructure, on_delete=models.CASCADE, related_name='huploaded_files2')  # **************
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name} ({self.structure.structure})"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['structure'], name='hunique_file_per_structure2')   # **************
        ]
        
        
class HDeadend3(models.Model):             # **************
    CIRCUIT_CHOICES = [
        (0, "0"),
    ] + [(i, str(i)) for i in range(1, 11)]

    structure = models.ForeignKey(
        'ListOfStructure',
        on_delete=models.CASCADE,
        related_name='h_deadends3',             # **************
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
            models.UniqueConstraint(fields=['structure'], name='unique_h_per_structure3')  # **************
        ]

        
class hUploadedFile3(models.Model):
    structure = models.ForeignKey(ListOfStructure, on_delete=models.CASCADE, related_name='huploaded_files3')  # **************
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name} ({self.structure.structure})"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['structure'], name='hunique_file_per_structure3')   # **************
        ]
        
        
class HDeadend4(models.Model):             # **************
    CIRCUIT_CHOICES = [
        (0, "0"),
    ] + [(i, str(i)) for i in range(1, 11)]

    structure = models.ForeignKey(
        'ListOfStructure',
        on_delete=models.CASCADE,
        related_name='h_deadends4',             # **************
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
            models.UniqueConstraint(fields=['structure'], name='unique_h_per_structure4')  # **************
        ]

        
class hUploadedFile4(models.Model):
    structure = models.ForeignKey(ListOfStructure, on_delete=models.CASCADE, related_name='huploaded_files4')  # **************
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name} ({self.structure.structure})"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['structure'], name='hunique_file_per_structure4')   # **************
        ]
        
        
        
class TDeadend6(models.Model):
    CIRCUIT_CHOICES = [
        (0, "0"),                                   # ************Here**********
    ] + [(i, str(i)) for i in range(1, 11)]

    structure = models.ForeignKey(
        'ListOfStructure',
        on_delete=models.CASCADE,
        related_name='t_deadends6',                 # ************Here**********
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
            models.UniqueConstraint(fields=['structure'], name='unique_t_per_structure6')
        ]      



class tUploadedFile6(models.Model):
    structure = models.ForeignKey(ListOfStructure, on_delete=models.CASCADE, related_name='tuploaded_files6')
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name} ({self.structure.structure})"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['structure'], name='tunique_file_per_structure6')
        ]
        
        
class TDeadend7(models.Model):
    CIRCUIT_CHOICES = [
        (0, "0"),                                   # ************Here**********
    ] + [(i, str(i)) for i in range(1, 11)]

    structure = models.ForeignKey(
        'ListOfStructure',
        on_delete=models.CASCADE,
        related_name='t_deadends7',                 # ************Here**********
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
            models.UniqueConstraint(fields=['structure'], name='unique_t_per_structure7')
        ]      



class tUploadedFile7(models.Model):
    structure = models.ForeignKey(ListOfStructure, on_delete=models.CASCADE, related_name='tuploaded_files7')
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name} ({self.structure.structure})"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['structure'], name='tunique_file_per_structure7')
        ]
        
        
class TDeadend8(models.Model):
    CIRCUIT_CHOICES = [
        (0, "0"),                                   # ************Here**********
    ] + [(i, str(i)) for i in range(1, 11)]

    structure = models.ForeignKey(
        'ListOfStructure',
        on_delete=models.CASCADE,
        related_name='t_deadends8',                 # ************Here**********
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
            models.UniqueConstraint(fields=['structure'], name='unique_t_per_structure8')
        ]      



class tUploadedFile8(models.Model):
    structure = models.ForeignKey(ListOfStructure, on_delete=models.CASCADE, related_name='tuploaded_files8')
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name} ({self.structure.structure})"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['structure'], name='tunique_file_per_structure8')
        ]
        
        
class TDeadend9(models.Model):
    CIRCUIT_CHOICES = [
        (0, "0"),                                   # ************Here**********
    ] + [(i, str(i)) for i in range(1, 11)]

    structure = models.ForeignKey(
        'ListOfStructure',
        on_delete=models.CASCADE,
        related_name='t_deadends9',                 # ************Here**********
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
            models.UniqueConstraint(fields=['structure'], name='unique_t_per_structure9')
        ]      



class tUploadedFile9(models.Model):
    structure = models.ForeignKey(ListOfStructure, on_delete=models.CASCADE, related_name='tuploaded_files9')
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name} ({self.structure.structure})"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['structure'], name='tunique_file_per_structure9')
        ]
        
        
class TDeadend10(models.Model):
    CIRCUIT_CHOICES = [
        (0, "0"),                                   # ************Here**********
    ] + [(i, str(i)) for i in range(1, 11)]

    structure = models.ForeignKey(
        'ListOfStructure',
        on_delete=models.CASCADE,
        related_name='t_deadends10',                 # ************Here**********
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
            models.UniqueConstraint(fields=['structure'], name='unique_t_per_structure10')
        ]      



class tUploadedFile10(models.Model):
    structure = models.ForeignKey(ListOfStructure, on_delete=models.CASCADE, related_name='tuploaded_files10')
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name} ({self.structure.structure})"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['structure'], name='tunique_file_per_structure10')
        ]
        
        
class TDeadend11(models.Model):
    CIRCUIT_CHOICES = [
        (0, "0"),                                   # ************Here**********
    ] + [(i, str(i)) for i in range(1, 11)]

    structure = models.ForeignKey(
        'ListOfStructure',
        on_delete=models.CASCADE,
        related_name='t_deadends11',                 # ************Here**********
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
            models.UniqueConstraint(fields=['structure'], name='unique_t_per_structure11')
        ]      



class tUploadedFile11(models.Model):
    structure = models.ForeignKey(ListOfStructure, on_delete=models.CASCADE, related_name='tuploaded_files11')
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name} ({self.structure.structure})"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['structure'], name='tunique_file_per_structure11')
        ]
        
              
        
class MonopoleDeadend(models.Model):
    CIRCUIT_CHOICES = [
        (0, "0"),
    ] + [(i, str(i)) for i in range(1, 11)]

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
        
        
        
class MDeadend5(models.Model):
    CIRCUIT_CHOICES = [
        (0, "0"),                                   # ************Here**********
    ] + [(i, str(i)) for i in range(1, 11)]

    structure = models.ForeignKey(
        'ListOfStructure',
        on_delete=models.CASCADE,
        related_name='m_deadends5',                 # ************Here**********
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
            models.UniqueConstraint(fields=['structure'], name='unique_m_per_structure5')
        ]      



class mUploadedFile5(models.Model):
    structure = models.ForeignKey(ListOfStructure, on_delete=models.CASCADE, related_name='muploaded_files5')
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name} ({self.structure.structure})"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['structure'], name='munique_file_per_structure5')
        ]
        
        


class MDeadend6(models.Model):
    CIRCUIT_CHOICES = [
        (0, "0"),                                   # ************Here**********
    ] + [(i, str(i)) for i in range(1, 11)]

    structure = models.ForeignKey(
        'ListOfStructure',
        on_delete=models.CASCADE,
        related_name='m_deadends6',                 # ************Here**********
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
            models.UniqueConstraint(fields=['structure'], name='unique_m_per_structure6')
        ]      



class mUploadedFile6(models.Model):
    structure = models.ForeignKey(ListOfStructure, on_delete=models.CASCADE, related_name='muploaded_files6')
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name} ({self.structure.structure})"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['structure'], name='munique_file_per_structure6')
        ]
        

class MDeadend7(models.Model):
    CIRCUIT_CHOICES = [
        (0, "0"),                                   # ************Here**********
    ] + [(i, str(i)) for i in range(1, 11)]

    structure = models.ForeignKey(
        'ListOfStructure',
        on_delete=models.CASCADE,
        related_name='m_deadends7',                 # ************Here**********
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
            models.UniqueConstraint(fields=['structure'], name='unique_m_per_structure7')
        ]      



class mUploadedFile7(models.Model):
    structure = models.ForeignKey(ListOfStructure, on_delete=models.CASCADE, related_name='muploaded_files7')
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name} ({self.structure.structure})"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['structure'], name='munique_file_per_structure7')
        ]
        
        


class MDeadend8(models.Model):
    CIRCUIT_CHOICES = [
        (0, "0"),                                   # ************Here**********
    ] + [(i, str(i)) for i in range(1, 11)]

    structure = models.ForeignKey(
        'ListOfStructure',
        on_delete=models.CASCADE,
        related_name='m_deadends8',                 # ************Here**********
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
            models.UniqueConstraint(fields=['structure'], name='unique_m_per_structure8')
        ]      



class mUploadedFile8(models.Model):
    structure = models.ForeignKey(ListOfStructure, on_delete=models.CASCADE, related_name='muploaded_files8')
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name} ({self.structure.structure})"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['structure'], name='munique_file_per_structure8')
        ]
        
    
class MDeadend9(models.Model):
    CIRCUIT_CHOICES = [
        (0, "0"),                                   # ************Here**********
    ] + [(i, str(i)) for i in range(1, 11)]

    structure = models.ForeignKey(
        'ListOfStructure',
        on_delete=models.CASCADE,
        related_name='m_deadends9',                 # ************Here**********
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
            models.UniqueConstraint(fields=['structure'], name='unique_m_per_structure9')
        ]      



class mUploadedFile9(models.Model):
    structure = models.ForeignKey(ListOfStructure, on_delete=models.CASCADE, related_name='muploaded_files9')
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name} ({self.structure.structure})"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['structure'], name='munique_file_per_structure9')
        ]
        
        

class MDeadend10(models.Model):
    CIRCUIT_CHOICES = [
        (0, "0"),                                   # ************Here**********
    ] + [(i, str(i)) for i in range(1, 11)]

    structure = models.ForeignKey(
        'ListOfStructure',
        on_delete=models.CASCADE,
        related_name='m_deadends10',                 # ************Here**********
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
            models.UniqueConstraint(fields=['structure'], name='unique_m_per_structure10')
        ]      



class mUploadedFile10(models.Model):
    structure = models.ForeignKey(ListOfStructure, on_delete=models.CASCADE, related_name='muploaded_files10')
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name} ({self.structure.structure})"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['structure'], name='munique_file_per_structure10')
        ]
        

class MDeadend11(models.Model):
    CIRCUIT_CHOICES = [
        (0, "0"),                                   # ************Here**********
    ] + [(i, str(i)) for i in range(1, 11)]

    structure = models.ForeignKey(
        'ListOfStructure',
        on_delete=models.CASCADE,
        related_name='m_deadends11',                 # ************Here**********
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
            models.UniqueConstraint(fields=['structure'], name='unique_m_per_structure11')
        ]      



class mUploadedFile11(models.Model):
    structure = models.ForeignKey(ListOfStructure, on_delete=models.CASCADE, related_name='muploaded_files11')
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name} ({self.structure.structure})"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['structure'], name='munique_file_per_structure11')
        ]
        
        
class MDeadend12(models.Model):
    CIRCUIT_CHOICES = [
        (0, "0"),                                   # ************Here**********
    ] + [(i, str(i)) for i in range(1, 11)]

    structure = models.ForeignKey(
        'ListOfStructure',
        on_delete=models.CASCADE,
        related_name='m_deadends12',                 # ************Here**********
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
            models.UniqueConstraint(fields=['structure'], name='unique_m_per_structure12')
        ]      



class mUploadedFile12(models.Model):
    structure = models.ForeignKey(ListOfStructure, on_delete=models.CASCADE, related_name='muploaded_files12')
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name} ({self.structure.structure})"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['structure'], name='munique_file_per_structure12')
        ]
        
        
class MDeadend13(models.Model):
    CIRCUIT_CHOICES = [
        (0, "0"),                                   # ************Here**********
    ] + [(i, str(i)) for i in range(1, 11)]

    structure = models.ForeignKey(
        'ListOfStructure',
        on_delete=models.CASCADE,
        related_name='m_deadends13',                 # ************Here**********
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
            models.UniqueConstraint(fields=['structure'], name='unique_m_per_structure13')
        ]      



class mUploadedFile13(models.Model):
    structure = models.ForeignKey(ListOfStructure, on_delete=models.CASCADE, related_name='muploaded_files13')
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name} ({self.structure.structure})"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['structure'], name='munique_file_per_structure13')
        ]
        
        

class TowerModel(models.Model):
    name = models.CharField(max_length=255)
    model_file = models.FileField(upload_to='tower_models/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    def get_file_url(self):
        if self.model_file and hasattr(self.model_file, 'url'):
            return self.model_file.url
        return ''