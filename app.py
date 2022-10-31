from flask import Flask, render_template, url_for, request, send_file, render_template_string
import zimbra_mail
import generate_document

app = Flask(__name__,template_folder='./templates', static_folder='./static')
app.secret_key = 'ADARSH_QUOTE'


@app.route('/', methods=['POST', 'GET'])
def hello_world():  # put application's code here
    if request.method == 'POST':
        uri, auth_token, communication = zimbra_mail.authenticate_zimbra()
        html_string = open('templates//email-template.html', 'r').read()
        ret_obj = generate_document.populate_fields(request_form_object=request.form)
        zimbra_mail.send_mail(applicant_name=request.form['nameinput'], dpcode='19893',
                              uri=uri, usr_token=auth_token, comm=communication, invoice_file=ret_obj[0],
                              challan_file=ret_obj[1],mudra_file=ret_obj[2])
        return render_template_string(
            zimbra_mail.html_builder(html_string_in=html_string, email_client=request.form['nameinput']))
    else:
        return render_template('index.html')



if __name__ == '__main__':
    app.run()
