from django import forms
from .models import (
    DatosPersonales,
    ExperienciaLaboral,
    Reconocimientos,
    CursosRealizados,
    ProductosAcademicos,
    ProductosLaborales,
    VentaGarage
)

from django import forms
from .models import DatosPersonales

class SeleccionSeccionesForm(forms.ModelForm):
    class Meta:
        model = DatosPersonales
        fields = [
            'imprimir_experiencia', 
            'imprimir_reconocimientos', 
            'imprimir_cursos', 
            'imprimir_productos_academicos',
            'imprimir_productos_laborales',
            'imprimir_venta_garage', 
        ]
        widgets = {
            'imprimir_experiencia': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'imprimir_reconocimientos': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'imprimir_cursos': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'imprimir_productos_academicos': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'imprimir_productos_laborales': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'imprimir_venta_garage': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
class DatosPersonalesForm(forms.ModelForm):
    class Meta:
        model = DatosPersonales
        fields = [
            'foto_perfil',
            'descripcionperfil', 'nombres', 'apellidos', 'nacionalidad',
            'lugarnacimiento', 'fechanacimiento', 'numerocedula', 'sexo',
            'estadocivil', 'licenciaconducir', 'telefonoconvencional',
            'telefonofijo', 'direcciontrabajo', 'direcciondomiciliaria', 'sitioweb'
        ]
        widgets = {
            'fechanacimiento': forms.DateInput(attrs={'type': 'date'}),
            'descripcionperfil': forms.TextInput(attrs={'placeholder': 'Ej: Desarrollador Full Stack'}),
            'nombres': forms.TextInput(attrs={'placeholder': 'Nombres completos'}),
            'apellidos': forms.TextInput(attrs={'placeholder': 'Apellidos completos'}),
        }

class ExperienciaLaboralForm(forms.ModelForm):
    class Meta:
        model = ExperienciaLaboral
        fields = [
            'cargodesempenado', 'nombrempresa', 'lugarempresa', 'emailempresa',
            'sitiowebempresa', 'nombrecontactoempresarial', 'telefonocontactoempresarial',
            'fechainiciogestion', 'fechafingestion', 'descripcionfunciones',
            'activarparaqueseveaenfront', 'rutacertificado'
        ]
        widgets = {
            'fechainiciogestion': forms.DateInput(attrs={'type': 'date'}),
            'fechafingestion': forms.DateInput(attrs={'type': 'date'}),
            'descripcionfunciones': forms.Textarea(attrs={'rows': 4}),
        }

class ReconocimientosForm(forms.ModelForm):
    class Meta:
        model = Reconocimientos
        fields = [
            'tiporeconocimiento', 'fechareconocimiento', 'descripcionreconocimiento',
            'entidadpatrocinadora', 'nombrecontactoauspicia', 'telefonocontactoauspicia',
            'activarparaqueseveaenfront', 'rutacertificado'
        ]
        widgets = {
            'fechareconocimiento': forms.DateInput(attrs={'type': 'date'}),
            'descripcionreconocimiento': forms.Textarea(attrs={'rows': 3}),
        }

class CursosRealizadosForm(forms.ModelForm):
    class Meta:
        model = CursosRealizados
        fields = [
            'nombrecurso', 'fechainicio', 'fechafin', 'totalhoras',
            'descripcioncurso', 'entidadpatrocinadora', 'nombrecontactoauspicia',
            'telefonocontactoauspicia', 'emailempresapatrocinadora',
            'activarparaqueseveaenfront', 'rutacertificado'
        ]
        widgets = {
            'fechainicio': forms.DateInput(attrs={'type': 'date'}),
            'fechafin': forms.DateInput(attrs={'type': 'date'}),
            'descripcioncurso': forms.Textarea(attrs={'rows': 3}),
        }

class ProductosAcademicosForm(forms.ModelForm):
    class Meta:
        model = ProductosAcademicos
        fields = ['nombrerecurso', 'clasificador', 'descripcion', 'archivo', 'link', 'activarparaqueseveaenfront']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }

class ProductosLaboralesForm(forms.ModelForm):
    class Meta:
        model = ProductosLaborales
        fields = ['nombreproducto', 'fechaproducto', 'descripcion', 'archivo', 'link', 'activarparaqueseveaenfront']
        widgets = {
            'fechaproducto': forms.DateInput(attrs={'type': 'date'}),
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }
        
class VentaGarageForm(forms.ModelForm):
    class Meta:
        model = VentaGarage
        # Excluimos el perfil (se asigna automático) y la fecha (es auto_now_add)
        exclude = ['idperfilconqueestaactivo', 'fecha_publicacion']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'estadoproducto': forms.Select(attrs={'class': 'form-control'}),
            'valordelbien': forms.NumberInput(attrs={'class': 'form-control'}),
            'nombreproducto': forms.TextInput(attrs={'class': 'form-control'}),
        }