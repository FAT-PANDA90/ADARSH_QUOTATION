from datetime import datetime, timedelta, timezone
from dateutil.relativedelta import relativedelta
import decimal
from mailmerge import MailMerge


wdFormatPDF = 17
## to timestamp output file
dt = datetime.now()
utc_time = dt.replace(tzinfo=timezone.utc)
utc_timestamp = utc_time.timestamp()

def ord(n):
    return str(n)+("th" if 4<=n%100<=20 else {1:"st",2:"nd",3:"rd"}.get(n%10, "th"))

def populate_date(dateofmortgage):
    date_mortgage = datetime.strptime(dateofmortgage,'%Y-%m-%d')
    date_mortgage = date_mortgage.strftime('{th} day of %B %Y').replace("{th}", ord(date_mortgage.day))
    return date_mortgage

def populate_fields(request_form_object):
    application_file = f"{request_form_object['nameinput'][0:3]}{str(utc_timestamp)[-6:]}_1.docx"
    template = 'QUOTATION.docx'
    document1 = MailMerge(template)
    document1.merge(
        pincode=request_form_object['pincode'],
        CUSTOMER_NAME=request_form_object['nameinput'],
        Address_1=request_form_object['Address1'],
        Address_2=request_form_object['Address2'],
        Address_3=request_form_object['Address3'],
        Address_4=request_form_object['Address4'],
        PAN_NUMBER=request_form_object['pan'],
        QUOTATION_NUMBER = request_form_object['QNO'],
        Mobile_no=request_form_object['mobaaplicant'],
        DATE=populate_date(request_form_object['dateofcheque'])
    )
    document1.write(application_file)
    return application_file


