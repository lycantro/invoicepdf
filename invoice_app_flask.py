from flask import Flask, render_template, request, make_response, session
import pdfkit
import os

# Configuración de la ruta de la carpeta de plantillas explícitamente
template_dir = r'C:\Users\leona\invoice_app_flask.py\templates'
app = Flask(__name__, template_folder=template_dir)

path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

# Configuración de la clave secreta para la sesión.
# En un entorno de producción, esta clave debería ser algo secreto y único.
app.secret_key = 'a_random_string'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name', '')
        bank_name = request.form.get('bank_name', '')
        bsb = request.form.get('bsb', '')
        account_number = request.form.get('account_number', '')
        company_name = request.form.get('company_name', '')
        hourly_rate = float(request.form.get('hourly_rate', 0))

        dates_locations_hours = []
        total_hours = 0
        for i in range(1, 8):
            date = request.form.get(f'date_{i}', '')
            location = request.form.get(f'location_{i}', '')
            hours_str = request.form.get(f'hours_{i}', '0')

            hours = float(hours_str) if hours_str.strip() else 0.0
            total_hours += hours

            if date and location:
                dates_locations_hours.append((date, location, hours))

        total_payment = total_hours * hourly_rate

        data = {
            'name': name,
            'bank_name': bank_name,
            'bsb': bsb,
            'account_number': account_number,
            'company_name': company_name,
            'hourly_rate': hourly_rate,
            'dates_locations_hours': dates_locations_hours,
            'total': total_payment
        }

        # Guardamos los datos en la sesión
        session['invoice_data'] = data

        return render_template('invoice.html', data=data)
    return render_template('input_form.html')


@app.route('/download-invoice', methods=['GET'])
def download_invoice():
    # Obtenemos los datos de la sesión
    data = session.get('invoice_data', {})

    rendered = render_template('invoice.html', data=data)

    pdf = pdfkit.from_string(rendered, False, configuration=config)

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=invoice.pdf'
    return response


if __name__ == '__main__':
    app.run(debug=True)

if __name__ == '__main__':
    app.run(debug=True)