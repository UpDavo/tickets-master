from django.template.loader import get_template
from weasyprint import HTML

def generate_pdf_from_template(template_name, context_dict):
    # Renderiza el template con el contexto proporcionado
    template = get_template(template_name)
    html_content = template.render(context_dict)

    # Crea un objeto HTML con el contenido renderizado
    html = HTML(string=html_content)

    # Genera el PDF
    pdf_file = html.write_pdf()

    return pdf_file