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