from django.db import models

class ListOfStructure(models.Model):
    structure = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.structure


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
    CIRCUIT_CHOICES = [(i, str(i)) for i in range(1, 11)]

    structure = models.ForeignKey('ListOfStructure', on_delete=models.CASCADE, related_name='tower_deadends', unique=True)

    num_3_phase_circuits = models.PositiveIntegerField(choices=CIRCUIT_CHOICES)
    num_shield_wires = models.PositiveIntegerField(choices=CIRCUIT_CHOICES)
    num_1_phase_circuits = models.PositiveIntegerField(choices=CIRCUIT_CHOICES)
    num_communication_cables = models.PositiveIntegerField(choices=CIRCUIT_CHOICES)

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
    CIRCUIT_CHOICES = [(i, str(i)) for i in range(1, 11)]

    structure = models.ForeignKey('ListOfStructure', on_delete=models.CASCADE, related_name='h_deadends1', unique=True)

    num_3_phase_circuits = models.PositiveIntegerField(choices=CIRCUIT_CHOICES)
    num_shield_wires = models.PositiveIntegerField(choices=CIRCUIT_CHOICES)
    num_1_phase_circuits = models.PositiveIntegerField(choices=CIRCUIT_CHOICES)
    num_communication_cables = models.PositiveIntegerField(choices=CIRCUIT_CHOICES)

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
    
        
class HDeadend2(models.Model):
    CIRCUIT_CHOICES = [(i, str(i)) for i in range(1, 11)]

    structure = models.ForeignKey('ListOfStructure', on_delete=models.CASCADE, related_name='h_deadends2', unique=True)

    num_3_phase_circuits = models.PositiveIntegerField(choices=CIRCUIT_CHOICES)
    num_shield_wires = models.PositiveIntegerField(choices=CIRCUIT_CHOICES)
    num_1_phase_circuits = models.PositiveIntegerField(choices=CIRCUIT_CHOICES)
    num_communication_cables = models.PositiveIntegerField(choices=CIRCUIT_CHOICES)

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