import jinja2
import pdfkit
from datetime import datetime


def generate_invoice(context):
    template_loader = jinja2.FileSystemLoader('./')
    template_env = jinja2.Environment(loader=template_loader)

    html_template = './invoice/invoice.html'
    template = template_env.get_template(html_template)
    output_text = template.render(context)

    config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')
    output_pdf = './invoice/invoice.pdf'
    pdfkit.from_string(output_text, output_pdf, configuration=config, css='./invoice/invoice.css')
