from datetime import datetime, timedelta, timezone
from fillpdf import fillpdfs
from datetime import datetime, timedelta, timezone

# fillpdfs.print_form_fields('Invoice_mail.pdf')
# fillpdfs.print_form_fields('CHALLAN_mail.pdf')
# fillpdfs.print_form_fields('MUDRA.pdf')
dt = datetime.now()
utc_time = dt.replace(tzinfo=timezone.utc)
utc_timestamp = utc_time.timestamp()

def num2words(number):
    def get_word(n):
        words = {0: "", 1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven", 8: "Eight",
                 9: "Nine", 10: "Ten", 11: "Eleven", 12: "Twelve", 13: "Thirteen", 14: "Fourteen", 15: "Fifteen",
                 16: "Sixteen", 17: "Seventeen", 18: "Eighteen", 19: "Nineteen", 20: "Twenty", 30: "Thirty",
                 40: "Forty", 50: "Fifty", 60: "Sixty", 70: "Seventy", 80: "Eighty", 90: "Ninty"}
        if n <= 20:
            return words[n]
        else:
            ones = n % 10
            tens = n - ones
            return words[tens] + " " + words[ones]

    def get_all_word(n):
        d = [100, 10, 100, 100]
        v = ["", "Hundred And", "Thousand", "lakh"]
        w = []
        for i, x in zip(d, v):
            t = get_word(n % i)
            if t != "":
                t += " " + x
            w.append(t.rstrip(" "))
            n = n // i
        w.reverse()
        w = ' '.join(w).strip()
        if w.endswith("And"):
            w = w[:-3]
        return w

    arr = str(number).split(".")
    number = int(arr[0])
    crore = number // 10000000
    number = number % 10000000
    word = ""
    if crore > 0:
        word += get_all_word(crore)
        word += " crore "
    word += get_all_word(number).strip() + " Rupees Only"
    # if len(arr) > 1:
    #     if len(arr[1]) == 1:
    #         arr[1] += "0"
    #     word += " and " + get_all_word(int(arr[1])) + " paisa"
    return word

def populate_fields(request_form_object):
    invoice_file = f"{request_form_object['nameinput'][0:3]}{str(utc_timestamp)[-6:]}_invoice.pdf"
    challan_file = f"{request_form_object['nameinput'][0:3]}{str(utc_timestamp)[-6:]}_challan.pdf"
    mudra_file = f"{request_form_object['nameinput'][0:3]}{str(utc_timestamp)[-6:]}_mudra.pdf"
    date_invoice = datetime.strptime(request_form_object['dateofcheque'], '%Y-%m-%d')
    date_invoice = date_invoice.strftime('%d/%m/%Y')
    total_invoice = int(request_form_object['RATE'])*1.05
    SGST = CGST = str(int(request_form_object['RATE']) * 0.025)
    invoice_word =num2words(total_invoice)
    challan_word = num2words(int(request_form_object['CH_Rate']))

    to_fill_dict = {
        'Name': request_form_object['nameinput'].upper(),
        'DATE': date_invoice,
        'Father_Name': request_form_object['Father_Name'].upper(),
        'PAN': request_form_object['pan'].upper(),
        'mobaaplicant': request_form_object['mobaaplicant'],
        'Address_1': f"C/O {request_form_object['Father_Name'].upper()}, {request_form_object['Address1'].upper()}",
        'Address_2': f"{request_form_object['Address2'].upper()}, District {request_form_object['Address3'].upper()}, PIN:-{request_form_object['pincode']}",
        'pincode': request_form_object['pincode'],
        'Model_Name': request_form_object['Model_Name'],
        'Chassis': request_form_object['Chassis'].upper(),
        'Motor': request_form_object['Motor'].upper(),
        'Colour': request_form_object['Colour'].upper(),
        'Battery_Make': request_form_object['Battery_Make'].upper(),
        'BAT_1': request_form_object['BAT_1'].upper(),
        'BAT_2': request_form_object['BAT_2'].upper(),
        'BAT_3': request_form_object['BAT_3'].upper(),
        'BAT_4': request_form_object['BAT_4'].upper(),
        'RATE': request_form_object['RATE'],
        'SGST': SGST,
        'CGST': CGST,
        'TOTAL_NUM': str(total_invoice),
        'Total_Words': invoice_word.upper(),
        'Invoice_no': request_form_object['Invoice_no'],
        'CH_Rate': request_form_object['CH_Rate'],
        'CH_Rate_words': challan_word.upper(),
    }
    # print(to_fill_dict)
    fillpdfs.write_fillable_pdf('Invoice_mail.pdf', invoice_file, to_fill_dict, flatten=True)
    fillpdfs.write_fillable_pdf('CHALLAN_mail.pdf', challan_file, to_fill_dict, flatten=True)
    fillpdfs.write_fillable_pdf('MUDRA.pdf', mudra_file, to_fill_dict, flatten=True)

    return [invoice_file,challan_file,mudra_file]