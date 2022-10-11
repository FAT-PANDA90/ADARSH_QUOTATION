# https://stackoverflow.com/questions/28646214/accessing-zimbra-via-rest-api-how-do-i-get-the-zauthtoken
# https://github.com/Zimbra-Community/python-zimbra
import os

from pythonzimbra.communication import Communication
from pythonzimbra.tools import auth
from email.mime.base import MIMEBase
import requests
from requests_toolbelt import MultipartEncoder
import re
from zipfile import ZipFile

# raw = base64.urlsafe_b64encode(docx).decode()
# url to your zimbra server
def authenticate_zimbra():
    url = 'https://mapi.canarabank.in/service/soap'
    url_upload = 'https://mapi.canarabank.in:7071/service/upload'
    uri= 'https://mapi.canarabank.in/'
    comm = Communication(url)
    usr_token = auth.authenticate(url=url, account='sabyasachi@canarabank.in', key='Sabya@2025', use_password=True)
    return uri, usr_token, comm


def upload_request(uri,token, application_file,applicant):
    fileContent = 0
    zipObj = ZipFile(f'{applicant}.zip', 'w')
    zipObj.write(application_file)
    zipObj.close()
    print('this was triggered')
    with open(f'{applicant}.zip','rb') as f:
        fileContent = f.read()
    headers = {
    "Content-Type":"application/xml"
    }
    headers["Content-Type"]="multipart/form-data; boundary=----WebKitFormBoundary1abcdefghijklmno"
    headers["Cookie"]="ZM_AUTH_TOKEN="+token+";"
    m = MultipartEncoder(fields={
    'clientFile':(f'{applicant}.zip',fileContent,"application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    }, boundary = '----WebKitFormBoundary1abcdefghijklmno')
    r = requests.post(uri+"/service/upload",data=m,headers=headers,verify=False)
    re_pattern = "'\d+\S+'"
    attachment_id = str(re.search(re_pattern,r.text).group(0)[1:-1])
    print(attachment_id)
    os.remove(f'{applicant}.zip')
    return attachment_id


def send_mail(applicant_name, dpcode, uri, usr_token, comm, application_file):
    aid = upload_request(uri=uri, token=usr_token,
                         application_file=application_file, applicant=applicant_name[0:3])
    info_request = comm.gen_request(token=usr_token)
    info_request.add_request(
        'SendMsgRequest',
        {
            'm': {
                'su': f'Simpe Mortagage of {applicant_name}',
                'f': '!',
                'attach':{
                    'aid': aid,
                },
                'content': "Dear Sir,"
                           ""
                           ""
                           "Please download the attachment and unzip it to find the relevant files."
                           ""
                           ""
                           "Thanking You"
                           "Sabyasachi Sharma-835148",
                'e': {
                    'a': f'cb{dpcode}@canarabank.com',
                    't': 't',
                    'p':'CB SONARI'
                }
            },
        },
        'urn:zimbraMail'
    )
    info_response = comm.send_request(info_request)
    print(info_response.get_response())
    os.remove(application_file)

def html_builder(html_string_in, email_client):
    """
    :param html_string_in: a string type element containing html code
    :param email_client: name of the person email is addressed to
    :return: returns the rectified html string
    """
    pattern_string = '<p >Hi client name,'
    change_string = '<p >Hi ' + email_client
    pattern_string_footer = '>Sent to Client Name'
    change_string_footer = '>Sent to ' + email_client
    new_html_string = re.sub(pattern=pattern_string, repl=change_string, string=html_string_in)
    new_html_string = re.sub(pattern=pattern_string_footer, repl=change_string_footer, string=new_html_string)
    return new_html_string

def error_builder(html_string_in, email_client,error_msg):
    """
    :param html_string_in: a string type element containing html code
    :param email_client: name of the person email is addressed to
    :return: returns the rectified html string
    """
    pattern_string = '<p>Hi client name,'
    change_string = '<p>Hi ' + email_client
    pattern_body = "ERROR MESSAGE."
    change_body=  error_msg
    pattern_string_footer = '>Sent to Client Name'
    change_string_footer = '>Sent to ' + email_client
    new_html_string = re.sub(pattern=pattern_string, repl=change_string, string=html_string_in)
    new_html_string = re.sub(pattern=pattern_string_footer, repl=change_string_footer, string=new_html_string)
    new_html_string = re.sub(pattern=pattern_body, repl=change_body, string=new_html_string)
    return new_html_string
