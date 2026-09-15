from django.db import models


class Gender(models.Model):
    id = models.AutoField(primary_key=True, db_column='Id')
    gendername = models.CharField(max_length=50, db_column='GenderName')

    class Meta:
        managed = False
        db_table = 'Gender'


class Department(models.Model):
    id = models.AutoField(primary_key=True, db_column='Id')
    departmentname = models.CharField(max_length=50, db_column='DepartmentName')

    class Meta:
        managed = False
        db_table = 'Department'


class Post(models.Model):
    id = models.AutoField(primary_key=True, db_column='Id')
    postname = models.CharField(max_length=50, db_column='PostName')

    class Meta:
        managed = False
        db_table = 'Post'


class MedicalService(models.Model):
    id = models.AutoField(primary_key=True, db_column='Id')
    titleservice = models.CharField(max_length=50, db_column='TitleService')
    duration = models.IntegerField(db_column='Duration')
    cost = models.DecimalField(max_digits=10, decimal_places=2, db_column='Cost')

    class Meta:
        managed = False
        db_table = 'MedicalService'


class Patient(models.Model):
    id = models.AutoField(primary_key=True, db_column='Id')
    fname = models.CharField(max_length=50, db_column='FName')
    lname = models.CharField(max_length=50, db_column='LName')
    mname = models.CharField(max_length=50, null=True, blank=True, db_column='MName')
    adress = models.CharField(max_length=100, db_column='Adress')
    phone = models.CharField(max_length=12, db_column='Phone')
    idgender = models.ForeignKey(Gender, on_delete=models.DO_NOTHING, db_column='IDGender')
    dateofbirth = models.DateField(db_column='DateOfBirth')
    email = models.CharField(max_length=50, db_column='Email')
    login = models.CharField(max_length=100, null=True, blank=True, db_column='Login')
    password = models.CharField(max_length=100, null=True, blank=True, db_column='Password')

    class Meta:
        managed = False
        db_table = 'Patient'


class Worker(models.Model):
    id = models.AutoField(primary_key=True, db_column='Id')
    fname = models.CharField(max_length=50, db_column='FName')
    lname = models.CharField(max_length=50, db_column='LName')
    mname = models.CharField(max_length=50, null=True, blank=True, db_column='MName')
    idgender = models.ForeignKey(Gender, on_delete=models.DO_NOTHING,
                                 db_column='IdGender', related_name='workers')

    class Meta:
        managed = False
        db_table = 'Worker'


class Appointment(models.Model):
    id = models.AutoField(primary_key=True, db_column='Id')
    idworker = models.ForeignKey(Worker, on_delete=models.DO_NOTHING, db_column='IdWorker')
    idmedicalservice = models.ForeignKey(MedicalService, on_delete=models.DO_NOTHING,
                                         db_column='IdMedicalService')
    dataservice = models.DateTimeField(db_column='DataService')

    class Meta:
        managed = False
        db_table = 'Appointment'


class Order(models.Model):
    id = models.AutoField(primary_key=True, db_column='Id')
    idappoinment = models.ForeignKey(Appointment, on_delete=models.DO_NOTHING,
                                     db_column='IdAppoinment')
    idpatient = models.ForeignKey(Patient, on_delete=models.DO_NOTHING, db_column='IdPatient')
    totalprice = models.DecimalField(max_digits=10, decimal_places=2, db_column='TotalPrice')

    class Meta:
        managed = False
        db_table = 'Order'


class Diagnosis(models.Model):
    id = models.AutoField(primary_key=True, db_column='Id')
    diagnosisname = models.CharField(max_length=50, db_column='DiagnosisName')

    class Meta:
        managed = False
        db_table = 'Diagnosis'


class PatientDiagnosis(models.Model):
    id = models.AutoField(primary_key=True, db_column='Id')
    idpatient = models.ForeignKey(Patient, on_delete=models.DO_NOTHING, db_column='IdPatient')
    iddiagnosis = models.ForeignKey(Diagnosis, on_delete=models.DO_NOTHING,
                                    db_column='IdDiagnosis')

    class Meta:
        managed = False
        db_table = 'PatientDiagnosis'