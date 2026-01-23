from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from io import BytesIO

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .forms import SeleccionSeccionesForm
from .models import (
    DatosPersonales,
    ExperienciaLaboral,
    Reconocimientos,
    CursosRealizados,
    ProductosAcademicos,
    ProductosLaborales,
    VentaGarage
)
from .forms import (
    DatosPersonalesForm,
    ExperienciaLaboralForm,
    ReconocimientosForm,
    CursosRealizadosForm,
    ProductosAcademicosForm,
    ProductosLaboralesForm,
    VentaGarageForm
)

# Vista de inicio/home - Pagina de bienvenida para TODOS
def home(request):
    """Página de bienvenida que muestra directamente la hoja de vida"""
    return mi_hoja_vida(request)
        

# Vista de login
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bienvenido {username}!')
                return redirect('curriculum:mi_hoja_vida')
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = AuthenticationForm()
    return render(request, 'curriculum/login.html', {'form': form})

# Vista de logout
def user_logout(request):
    logout(request)
    messages.success(request, 'Sesion cerrada exitosamente!')
    return redirect('curriculum:home')

# Vista de perfil personal
@login_required
def mi_perfil(request):
    perfil, created = DatosPersonales.objects.get_or_create(
        nombres=request.user.username,
        defaults={
            'apellidos': '',
            'numerocedula': '0000000000',
            'sexo': 'H',
            'perfilactivo': 1
        }
    )
    
    experiencias = ExperienciaLaboral.objects.filter(idperfilconqueestaactivo=perfil)
    reconocimientos = Reconocimientos.objects.filter(idperfilconqueestaactivo=perfil)
    cursos = CursosRealizados.objects.filter(idperfilconqueestaactivo=perfil)
    productos_academicos = ProductosAcademicos.objects.filter(idperfilconqueestaactivo=perfil)
    productos_laborales = ProductosLaborales.objects.filter(idperfilconqueestaactivo=perfil)
    ventas = VentaGarage.objects.filter(idperfilconqueestaactivo=perfil)
    
    context = {
        'perfil': perfil,
        'experiencias': experiencias,
        'reconocimientos': reconocimientos,
        'cursos': cursos,
        'productos_academicos': productos_academicos,
        'productos_laborales': productos_laborales,
        'ventas': ventas,
    }
    
    return render(request, 'curriculum/mi_perfil.html', context)



# PANEL DE GESTION (como el admin de Django)
@login_required
def panel_gestion(request):
    perfil = DatosPersonales.objects.filter(perfilactivo=1).first()

    if not perfil:
        return redirect('curriculum:agregar_datos_personales')

    # Inicializamos el formulario para que SIEMPRE exista la variable 'form_secciones'
    if request.method == 'POST':
        form_secciones = SeleccionSeccionesForm(request.POST, instance=perfil)
        if form_secciones.is_valid():
            form_secciones.save()
            messages.success(request, 'Preferencias de PDF actualizadas correctamente.')
            return redirect('curriculum:panel_gestion')
    else:
        form_secciones = SeleccionSeccionesForm(instance=perfil)

    # Cargamos el contexto
    context = {
        'perfil': perfil,
        'form_secciones': form_secciones, # Aquí se pasa el formulario sin errores
        'experiencias': ExperienciaLaboral.objects.filter(idperfilconqueestaactivo=perfil),
        'reconocimientos': Reconocimientos.objects.filter(idperfilconqueestaactivo=perfil),
        'cursos': CursosRealizados.objects.filter(idperfilconqueestaactivo=perfil),
        'productos_academicos': ProductosAcademicos.objects.filter(idperfilconqueestaactivo=perfil),
        'productos_laborales': ProductosLaborales.objects.filter(idperfilconqueestaactivo=perfil),
        'ventas': VentaGarage.objects.filter(idperfilconqueestaactivo=perfil),
    }
    
    return render(request, 'curriculum/panel_gestion.html', context)

# AGREGAR DATOS PERSONALES
@login_required
def agregar_datos_personales(request):
    if request.method == 'POST':
        form = DatosPersonalesForm(request.POST, request.FILES)
        if form.is_valid():
            nuevo_perfil = form.save(commit=False)
            nuevo_perfil.perfilactivo = 1  # Activar el nuevo perfil
            nuevo_perfil.save()
            messages.success(request, 'Perfil creado exitosamente.')
            return redirect('curriculum:panel_gestion')
    else:
        form = DatosPersonalesForm()
    
    return render(request, 'curriculum/agregar_datos_personales.html', {'form': form})

# EDITAR DATOS PERSONALES
@login_required
def editar_datos_personales(request):
    perfil = DatosPersonales.objects.filter(perfilactivo=1).first()
    
    if request.method == 'POST':
        form = DatosPersonalesForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            messages.success(request, 'Datos personales actualizados.')
            return redirect('curriculum:panel_gestion')
    else:
        form = DatosPersonalesForm(instance=perfil)
    
    return render(request, 'curriculum/editar_datos_personales.html', {'form': form, 'perfil': perfil})

# AGREGAR EXPERIENCIA
@login_required
def agregar_experiencia(request):
    perfil = DatosPersonales.objects.filter(perfilactivo=1).first()
    
    if request.method == 'POST':
        form = ExperienciaLaboralForm(request.POST, request.FILES)
        if form.is_valid():
            experiencia = form.save(commit=False)
            experiencia.idperfilconqueestaactivo = perfil
            experiencia.save()
            messages.success(request, 'Experiencia agregada.')
            return redirect('curriculum:panel_gestion')
    else:
        form = ExperienciaLaboralForm()
    
    return render(request, 'curriculum/agregar_experiencia.html', {'form': form})

# EDITAR EXPERIENCIA
@login_required
def editar_experiencia(request, pk):
    experiencia = get_object_or_404(ExperienciaLaboral, pk=pk)
    
    if request.method == 'POST':
        form = ExperienciaLaboralForm(request.POST, request.FILES, instance=experiencia)
        if form.is_valid():
            form.save()
            messages.success(request, 'Experiencia actualizada.')
            return redirect('curriculum:panel_gestion')
    else:
        form = ExperienciaLaboralForm(instance=experiencia)
    
    return render(request, 'curriculum/editar_experiencia.html', {'form': form, 'experiencia': experiencia})

# ELIMINAR EXPERIENCIA
@login_required
def eliminar_experiencia(request, pk):
    experiencia = get_object_or_404(ExperienciaLaboral, pk=pk)
    experiencia.delete()
    messages.success(request, 'Experiencia eliminada.')
    return redirect('curriculum:panel_gestion')

# AGREGAR CURSO
@login_required
def agregar_curso(request):
    perfil = DatosPersonales.objects.filter(perfilactivo=1).first()
    
    if request.method == 'POST':
        form = CursosRealizadosForm(request.POST, request.FILES)
        if form.is_valid():
            curso = form.save(commit=False)
            curso.idperfilconqueestaactivo = perfil
            curso.save()
            messages.success(request, 'Curso agregado.')
            return redirect('curriculum:panel_gestion')
    else:
        form = CursosRealizadosForm()
    
    return render(request, 'curriculum/agregar_curso.html', {'form': form})

# EDITAR CURSO
@login_required
def editar_curso(request, pk):
    curso = get_object_or_404(CursosRealizados, pk=pk)
    
    if request.method == 'POST':
        form = CursosRealizadosForm(request.POST, request.FILES, instance=curso)
        if form.is_valid():
            form.save()
            messages.success(request, 'Curso actualizado.')
            return redirect('curriculum:panel_gestion')
    else:
        form = CursosRealizadosForm(instance=curso)
    
    return render(request, 'curriculum/editar_curso.html', {'form': form, 'curso': curso})

# ELIMINAR CURSO
@login_required
def eliminar_curso(request, pk):
    curso = get_object_or_404(CursosRealizados, pk=pk)
    curso.delete()
    messages.success(request, 'Curso eliminado.')
    return redirect('curriculum:panel_gestion')

# AGREGAR RECONOCIMIENTO
@login_required
def agregar_reconocimiento(request):
    perfil = DatosPersonales.objects.filter(perfilactivo=1).first()
    
    if request.method == 'POST':
        form = ReconocimientosForm(request.POST, request.FILES)
        if form.is_valid():
            reconocimiento = form.save(commit=False)
            reconocimiento.idperfilconqueestaactivo = perfil
            reconocimiento.save()
            messages.success(request, 'Reconocimiento agregado.')
            return redirect('curriculum:panel_gestion')
    else:
        form = ReconocimientosForm()
    
    return render(request, 'curriculum/agregar_reconocimiento.html', {'form': form})

# EDITAR RECONOCIMIENTO
@login_required
def editar_reconocimiento(request, pk):
    reconocimiento = get_object_or_404(Reconocimientos, pk=pk)
    
    if request.method == 'POST':
        form = ReconocimientosForm(request.POST, request.FILES, instance=reconocimiento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reconocimiento actualizado.')
            return redirect('curriculum:panel_gestion')
    else:
        form = ReconocimientosForm(instance=reconocimiento)
    
    return render(request, 'curriculum/editar_reconocimiento.html', {'form': form, 'reconocimiento': reconocimiento})

# ELIMINAR RECONOCIMIENTO
@login_required
def eliminar_reconocimiento(request, pk):
    reconocimiento = get_object_or_404(Reconocimientos, pk=pk)
    reconocimiento.delete()
    messages.success(request, 'Reconocimiento eliminado.')
    return redirect('curriculum:panel_gestion')

# AGREGAR PRODUCTO ACADÉMICO
@login_required
def agregar_producto_academico(request):
    perfil = DatosPersonales.objects.filter(perfilactivo=1).first()
    
    if request.method == 'POST':
        form = ProductosAcademicosForm(request.POST)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.idperfilconqueestaactivo = perfil
            producto.save()
            messages.success(request, 'Producto académico agregado.')
            return redirect('curriculum:panel_gestion')
    else:
        form = ProductosAcademicosForm(request.POST, request.FILES)
    
    return render(request, 'curriculum/agregar_producto_academico.html', {'form': form})

# EDITAR PRODUCTO ACADÉMICO
@login_required
def editar_producto_academico(request, pk):
    producto = get_object_or_404(ProductosAcademicos, pk=pk)
    
    if request.method == 'POST':
        form = ProductosAcademicosForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto académico actualizado.')
            return redirect('curriculum:panel_gestion')
    else:
        form = ProductosAcademicosForm(instance=producto)
    
    return render(request, 'curriculum/editar_producto_academico.html', {'form': form, 'producto': producto})

# ELIMINAR PRODUCTO ACADÉMICO
@login_required
def eliminar_producto_academico(request, pk):
    producto = get_object_or_404(ProductosAcademicos, pk=pk)
    producto.delete()
    messages.success(request, 'Producto académico eliminado.')
    return redirect('curriculum:panel_gestion')

# AGREGAR PRODUCTO LABORAL
@login_required
def agregar_producto_laboral(request):
    perfil = DatosPersonales.objects.filter(perfilactivo=1).first()
    
    if request.method == 'POST':
        form = ProductosLaboralesForm(request.POST)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.idperfilconqueestaactivo = perfil
            producto.save()
            messages.success(request, 'Producto laboral agregado.')
            return redirect('curriculum:panel_gestion')
    else:
        form = ProductosLaboralesForm(request.POST, request.FILES) 
    
    return render(request, 'curriculum/agregar_producto_laboral.html', {'form': form})

# EDITAR PRODUCTO LABORAL
@login_required
def editar_producto_laboral(request, pk):
    producto = get_object_or_404(ProductosLaborales, pk=pk)
    
    if request.method == 'POST':
        form = ProductosLaboralesForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto laboral actualizado.')
            return redirect('curriculum:panel_gestion')
    else:
        form = ProductosLaboralesForm(instance=producto)
    
    return render(request, 'curriculum/editar_producto_laboral.html', {'form': form, 'producto': producto})

# ELIMINAR PRODUCTO LABORAL
@login_required
def eliminar_producto_laboral(request, pk):
    producto = get_object_or_404(ProductosLaborales, pk=pk)
    producto.delete()
    messages.success(request, 'Producto laboral eliminado.')
    return redirect('curriculum:panel_gestion')

# AGREGAR VENTA GARAGE
@login_required
def agregar_venta(request):
    perfil = DatosPersonales.objects.filter(perfilactivo=1).first()
    
    if request.method == 'POST':
        form = VentaGarageForm(request.POST, request.FILES) 
        if form.is_valid():
            venta = form.save(commit=False)
            venta.idperfilconqueestaactivo = perfil
            venta.save()
            messages.success(request, 'Artículo agregado con imagen.')
            return redirect('curriculum:panel_gestion')
    else:
        form = VentaGarageForm()
    
    return render(request, 'curriculum/agregar_venta.html', {'form': form})

# EDITAR VENTA GARAGE
@login_required
def editar_venta(request, pk):
    venta = get_object_or_404(VentaGarage, pk=pk)
    
    if request.method == 'POST':
        form = VentaGarageForm(request.POST, request.FILES, instance=venta)
        if form.is_valid():
            form.save()
            messages.success(request, 'Artículo actualizado con éxito.')
            return redirect('curriculum:panel_gestion')
    else:
        form = VentaGarageForm(instance=venta)
    
    return render(request, 'curriculum/editar_venta.html', {'form': form, 'venta': venta})

@login_required
def eliminar_venta(request, pk):
    venta = get_object_or_404(VentaGarage, pk=pk)
    venta.delete()
    messages.success(request, 'Artículo eliminado.')
    return redirect('curriculum:panel_gestion')

# Vista de Mi Hoja de Vida - TODOS
def mi_hoja_vida(request):
    try:
        perfil = DatosPersonales.objects.filter(perfilactivo=1).first()
        
        if perfil:
            experiencias = ExperienciaLaboral.objects.filter(
                idperfilconqueestaactivo=perfil,
                activarparaqueseveaenfront=True
            )
            
            reconocimientos = Reconocimientos.objects.filter(
                idperfilconqueestaactivo=perfil,
                activarparaqueseveaenfront=True
            )
            
            cursos = CursosRealizados.objects.filter(
                idperfilconqueestaactivo=perfil,
                activarparaqueseveaenfront=True
            )
            
            productos_academicos = ProductosAcademicos.objects.filter(
                idperfilconqueestaactivo=perfil,
                activarparaqueseveaenfront=True
            )
            
            productos_laborales = ProductosLaborales.objects.filter(
                idperfilconqueestaactivo=perfil,
                activarparaqueseveaenfront=True
            )
            
            ventas = VentaGarage.objects.filter(
                idperfilconqueestaactivo=perfil,
                activarparaqueseveaenfront=True
            )
            
            context = {
                'perfil': perfil,
                'experiencias': experiencias,
                'reconocimientos': reconocimientos,
                'cursos': cursos,
                'productos_academicos': productos_academicos,
                'productos_laborales': productos_laborales,
                'ventas': ventas,
            }

            return render(request, 'curriculum/mi_hoja_vida.html', context)
        else:
            # Si no hay perfil, mostramos la hoja vacía pero sin errores
            return render(request, 'curriculum/mi_hoja_vida.html', {'perfil': None})
            
    except Exception as e:
        return HttpResponse(f"Error al cargar: {e}")


def descargar_pdf(request):
    """Genera y descarga la hoja de vida en PDF"""
    perfil = DatosPersonales.objects.filter(perfilactivo=1).first()
    
    if not perfil:
        messages.error(request, 'No hay perfil disponible')
        return redirect('curriculum:home')  
    # Crear el PDF en memoria
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)  
    # Estilos
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#667eea'),
        spaceAfter=12,
        spaceBefore=12
    )
    
    normal_style = styles['Normal']
    
    # Contenido del PDF
    story = []
    
    # Título
    story.append(Paragraph(f"{perfil.nombres} {perfil.apellidos}", title_style))
    if perfil.descripcionperfil:
        story.append(Paragraph(perfil.descripcionperfil, styles['Italic']))
    story.append(Spacer(1, 0.3*inch))
    
    # Datos Personales
    story.append(Paragraph("DATOS PERSONALES", heading_style))
    datos_personales = [
        ['Cédula:', perfil.numerocedula],
        ['Fecha de Nacimiento:', perfil.fechanacimiento.strftime('%d/%m/%Y') if perfil.fechanacimiento else 'No especificada'],
        ['Sexo:', 'Hombre' if perfil.sexo == 'H' else 'Mujer'],
        ['Nacionalidad:', perfil.nacionalidad or 'No especificada'],
    ]
    
    if perfil.telefonoconvencional:
        datos_personales.append(['Teléfono:', perfil.telefonoconvencional])
    
    if perfil.direcciondomiciliaria:
        datos_personales.append(['Dirección:', perfil.direcciondomiciliaria])
    
    if perfil.sitioweb:
        datos_personales.append(['Sitio Web:', perfil.sitioweb])
    
    tabla_datos = Table(datos_personales, colWidths=[2*inch, 4*inch])
    tabla_datos.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2c3e50')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
    ]))
    story.append(tabla_datos)
    story.append(Spacer(1, 0.3*inch))
    
    # Experiencia Laboral
    experiencias = ExperienciaLaboral.objects.filter(
        idperfilconqueestaactivo=perfil,
        activarparaqueseveaenfront=True
    )
    
    if experiencias.exists():
        story.append(Paragraph("EXPERIENCIA LABORAL", heading_style))
        for exp in experiencias:
            story.append(Paragraph(f"<b>{exp.cargodesempenado}</b>", normal_style))
            story.append(Paragraph(f"{exp.nombrempresa}", normal_style))
            fecha_fin = exp.fechafingestion.strftime('%m/%Y') if exp.fechafingestion else 'Actualidad'
            story.append(Paragraph(f"{exp.fechainiciogestion.strftime('%m/%Y')} - {fecha_fin}", normal_style))
            if exp.lugarempresa:
                story.append(Paragraph(f"📍 {exp.lugarempresa}", normal_style))
            if exp.descripcionfunciones:
                story.append(Paragraph(exp.descripcionfunciones, normal_style))
            story.append(Spacer(1, 0.2*inch))
    
    # Reconocimientos
    reconocimientos = Reconocimientos.objects.filter(
        idperfilconqueestaactivo=perfil,
        activarparaqueseveaenfront=True
    )
    
    if reconocimientos.exists():
        story.append(Paragraph("RECONOCIMIENTOS", heading_style))
        for rec in reconocimientos:
            story.append(Paragraph(f"<b>{rec.descripcionreconocimiento}</b>", normal_style))
            story.append(Paragraph(f"{rec.tiporeconocimiento} - {rec.fechareconocimiento.strftime('%d/%m/%Y')}", normal_style))
            if rec.entidadpatrocinadora:
                story.append(Paragraph(f"Otorgado por: {rec.entidadpatrocinadora}", normal_style))
            story.append(Spacer(1, 0.2*inch))
    
    # Cursos
    cursos = CursosRealizados.objects.filter(
        idperfilconqueestaactivo=perfil,
        activarparaqueseveaenfront=True
    )
    
    if cursos.exists():
        story.append(Paragraph("CURSOS REALIZADOS", heading_style))
        for curso in cursos:
            story.append(Paragraph(f"<b>{curso.nombrecurso}</b>", normal_style))
            if curso.entidadpatrocinadora:
                story.append(Paragraph(f"Impartido por: {curso.entidadpatrocinadora}", normal_style))
            fecha_info = f"{curso.fechainicio.strftime('%m/%Y')}"
            if curso.fechafin:
                fecha_info += f" - {curso.fechafin.strftime('%m/%Y')}"
            if curso.totalhoras:
                fecha_info += f" | {curso.totalhoras} horas"
            story.append(Paragraph(fecha_info, normal_style))
            if curso.descripcioncurso:
                story.append(Paragraph(curso.descripcioncurso, normal_style))
            story.append(Spacer(1, 0.2*inch))
    
    # Productos Académicos
    productos_academicos = ProductosAcademicos.objects.filter(
        idperfilconqueestaactivo=perfil,
        activarparaqueseveaenfront=True
    )
    
    if productos_academicos.exists():
        story.append(Paragraph("PRODUCTOS ACADÉMICOS", heading_style))
        for prod in productos_academicos:
            story.append(Paragraph(f"<b>{prod.nombrerecurso}</b>", normal_style))
            if prod.clasificador:
                story.append(Paragraph(f"Categoría: {prod.clasificador}", normal_style))
            if prod.descripcion:
                story.append(Paragraph(prod.descripcion, normal_style))
            story.append(Spacer(1, 0.2*inch))
    
    # Productos Laborales
    productos_laborales = ProductosLaborales.objects.filter(
        idperfilconqueestaactivo=perfil,
        activarparaqueseveaenfront=True
    )
    
    if productos_laborales.exists():
        story.append(Paragraph("PRODUCTOS LABORALES", heading_style))
        for prod in productos_laborales:
            story.append(Paragraph(f"<b>{prod.nombreproducto}</b>", normal_style))
            story.append(Paragraph(f"{prod.fechaproducto.strftime('%m/%Y')}", normal_style))
            if prod.descripcion:
                story.append(Paragraph(prod.descripcion, normal_style))
            story.append(Spacer(1, 0.2*inch))
    
    # Venta Garage
    ventas = VentaGarage.objects.filter(
        idperfilconqueestaactivo=perfil,
        activarparaqueseveaenfront=True
    )
    
    if ventas.exists():
        story.append(Paragraph("VENTA GARAGE", heading_style))
        for venta in ventas:
            story.append(Paragraph(f"<b>{venta.nombreproducto}</b>", normal_style))
            story.append(Paragraph(f"Precio: ${venta.valordelbien} | Estado: {venta.estadoproducto}", normal_style))
            if venta.descripcion:
                story.append(Paragraph(venta.descripcion, normal_style))
            story.append(Spacer(1, 0.2*inch))
    
    # Construir PDF
    doc.build(story)
    
    # Obtener el valor del BytesIO buffer
    pdf = buffer.getvalue()
    buffer.close()
    
    # Crear la respuesta HTTP
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="CV_{perfil.nombres}_{perfil.apellidos}.pdf"'
    response.write(pdf)
    
    return response