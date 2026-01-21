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
        fields = ['nombreproducto', 'estadoproducto', 'descripcion', 'valordelbien', 'imagen', 'activarparaqueseveaenfront']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }
