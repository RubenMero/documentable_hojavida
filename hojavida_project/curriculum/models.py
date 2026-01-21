from django.db import models
from django.core.validators import RegexValidator

# TABLA PRINCIPAL: DATOS PERSONALES
class DatosPersonales(models.Model):
    SEXO_CHOICES = [
        ('H', 'Hombre'),
        ('M', 'Mujer'),
    ]
    
    idperfil = models.AutoField(primary_key=True)
    descripcionperfil = models.CharField(max_length=50, blank=True, null=True)
    perfilactivo = models.IntegerField(default=1)
    apellidos = models.CharField(max_length=60)
    nombres = models.CharField(max_length=60)

    foto_perfil = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)
    
    nacionalidad = models.CharField(max_length=20, blank=True, null=True)
    lugarnacimiento = models.CharField(max_length=60, blank=True, null=True)
    fechanacimiento = models.DateField(blank=True, null=True)
    numerocedula = models.CharField(
        max_length=10, 
        unique=True,
        validators=[RegexValidator(r'^\d{10}$', 'La cédula debe tener 10 dígitos')]
    )
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    estadocivil = models.CharField(max_length=50, blank=True, null=True)
    licenciaconducir = models.CharField(max_length=6, blank=True, null=True)
    telefonoconvencional = models.CharField(max_length=15, blank=True, null=True)
    telefonofijo = models.CharField(max_length=15, blank=True, null=True)
    direcciontrabajo = models.CharField(max_length=50, blank=True, null=True)
    direcciondomiciliaria = models.CharField(max_length=50, blank=True, null=True)
    sitioweb = models.CharField(max_length=60, blank=True, null=True)
    
    class Meta:
        db_table = 'datospersonales'
        verbose_name = 'Datos Personales'
        verbose_name_plural = 'Datos Personales'
    
    def __str__(self):
        return f"{self.nombres} {self.apellidos}"


# EXPERIENCIA LABORAL
class ExperienciaLaboral(models.Model):
    idexperiencialaboral = models.AutoField(primary_key=True)
    idperfilconqueestaactivo = models.ForeignKey(
        DatosPersonales, 
        on_delete=models.CASCADE,
        related_name='experiencias'
    )
    cargodesempenado = models.CharField(max_length=100)
    nombrempresa = models.CharField(max_length=50)
    lugarempresa = models.CharField(max_length=50, blank=True, null=True)
    emailempresa = models.EmailField(max_length=100, blank=True, null=True)
    sitiowebempresa = models.CharField(max_length=100, blank=True, null=True)
    nombrecontactoempresarial = models.CharField(max_length=100, blank=True, null=True)
    telefonocontactoempresarial = models.CharField(max_length=60, blank=True, null=True)
    fechainiciogestion = models.DateField()
    fechafingestion = models.DateField(blank=True, null=True)
    descripcionfunciones = models.TextField(blank=True, null=True)
    activarparaqueseveaenfront = models.BooleanField(default=True)
    rutacertificado = models.FileField(upload_to='certificados/experiencia/', blank=True, null=True)
    
    class Meta:
        db_table = 'experiencialaboral'
        verbose_name = 'Experiencia Laboral'
        verbose_name_plural = 'Experiencias Laborales'
        ordering = ['-fechainiciogestion']
    
    def __str__(self):
        return f"{self.cargodesempenado} en {self.nombrempresa}"


# RECONOCIMIENTOS
class Reconocimientos(models.Model):
    TIPO_CHOICES = [
        ('Académico', 'Académico'),
        ('Público', 'Público'),
        ('Privado', 'Privado'),
    ]
    
    idreconocimiento = models.AutoField(primary_key=True)
    idperfilconqueestaactivo = models.ForeignKey(
        DatosPersonales, 
        on_delete=models.CASCADE,
        related_name='reconocimientos'
    )
    tiporeconocimiento = models.CharField(max_length=100, choices=TIPO_CHOICES)
    fechareconocimiento = models.DateField()
    descripcionreconocimiento = models.TextField(blank=True, null=True)
    entidadpatrocinadora = models.CharField(max_length=100, blank=True, null=True)
    nombrecontactoauspicia = models.CharField(max_length=100, blank=True, null=True)
    telefonocontactoauspicia = models.CharField(max_length=60, blank=True, null=True)
    activarparaqueseveaenfront = models.BooleanField(default=True)
    rutacertificado = models.FileField(upload_to='certificados/reconocimientos/', blank=True, null=True)
    
    class Meta:
        db_table = 'reconocimientos'
        verbose_name = 'Reconocimiento'
        verbose_name_plural = 'Reconocimientos'
        ordering = ['-fechareconocimiento']
    
    def __str__(self):
        return f"{self.tiporeconocimiento} - {self.descripcionreconocimiento}"


# CURSOS REALIZADOS
class CursosRealizados(models.Model):
    idcursorealizado = models.AutoField(primary_key=True)
    idperfilconqueestaactivo = models.ForeignKey(
        DatosPersonales, 
        on_delete=models.CASCADE,
        related_name='cursos'
    )
    nombrecurso = models.CharField(max_length=100)
    fechainicio = models.DateField()
    fechafin = models.DateField(blank=True, null=True)
    totalhoras = models.IntegerField(blank=True, null=True)
    descripcioncurso = models.TextField(blank=True, null=True)
    entidadpatrocinadora = models.CharField(max_length=100, blank=True, null=True)
    nombrecontactoauspicia = models.CharField(max_length=100, blank=True, null=True)
    telefonocontactoauspicia = models.CharField(max_length=60, blank=True, null=True)
    emailempresapatrocinadora = models.EmailField(max_length=60, blank=True, null=True)
    activarparaqueseveaenfront = models.BooleanField(default=True)
    rutacertificado = models.FileField(upload_to='certificados/cursos/', blank=True, null=True)
    
    class Meta:
        db_table = 'cursosrealizados'
        verbose_name = 'Curso Realizado'
        verbose_name_plural = 'Cursos Realizados'
        ordering = ['-fechainicio']
    
    def __str__(self):
        return self.nombrecurso


# PRODUCTOS ACADÉMICOS
class ProductosAcademicos(models.Model):
    idproductoacademico = models.AutoField(primary_key=True)
    idperfilconqueestaactivo = models.ForeignKey(
        DatosPersonales, 
        on_delete=models.CASCADE,
        related_name='productos_academicos'
    )
    nombrerecurso = models.CharField(max_length=100)
    clasificador = models.CharField(max_length=100, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    

    # CAMPOS NUEVOS
    archivo = models.FileField(
        upload_to='productos_academicos/', 
        blank=True, 
        null=True
    )
    link = models.URLField(
        blank=True,
        null=True
    )

    activarparaqueseveaenfront = models.BooleanField(default=True)

    class Meta:
        db_table = 'productosacademicos'
        verbose_name = 'Producto Académico'
        verbose_name_plural = 'Productos Académicos'
    
    def __str__(self):
        return self.nombrerecurso


# PRODUCTOS LABORALES
class ProductosLaborales(models.Model):
    idproductoslaborales = models.AutoField(primary_key=True)
    idperfilconqueestaactivo = models.ForeignKey(
        DatosPersonales, 
        on_delete=models.CASCADE,
        related_name='productos_laborales'
    )
    nombreproducto = models.CharField(max_length=100)
    fechaproducto = models.DateField()
    descripcion = models.TextField(blank=True, null=True)

    archivo = models.FileField(upload_to='productos_laborales/', blank=True, null=True)
    link = models.URLField(blank=True, null=True)

    activarparaqueseveaenfront = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'productoslaborales'
        verbose_name = 'Producto Laboral'
        verbose_name_plural = 'Productos Laborales'
        ordering = ['-fechaproducto']
    
    def __str__(self):
        return self.nombreproducto


# VENTA GARAGE
class VentaGarage(models.Model):
    ESTADO_CHOICES = [
        ('Bueno', 'Bueno'),
        ('Regular', 'Regular'),
    ]
    
    idventagarage = models.AutoField(primary_key=True)
    idperfilconqueestaactivo = models.ForeignKey(
        DatosPersonales, 
        on_delete=models.CASCADE,
        related_name='ventas_garage'
    )
    nombreproducto = models.CharField(max_length=100)
    estadoproducto = models.CharField(max_length=40, choices=ESTADO_CHOICES)
    descripcion = models.TextField(blank=True, null=True)
    valordelbien = models.DecimalField(max_digits=7, decimal_places=2)

    imagen = models.ImageField(upload_to='ventas_garage/', blank=True, null=True)

    activarparaqueseveaenfront = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'ventagarage'
        verbose_name = 'Venta Garage'
        verbose_name_plural = 'Ventas Garage'
    
    def __str__(self):
        return f"{self.nombreproducto} - ${self.valordelbien}"