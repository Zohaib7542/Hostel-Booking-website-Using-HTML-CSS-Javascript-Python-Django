from django.shortcuts import render ,HttpResponse
from HostelHive.models import Booknow
from django.contrib import messages
import csv
from datetime import datetime
from email.mime.base import MIMEBase
from email import encoders
# Create your views here.

# Email work :
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from invoice.invoice import generate_invoice
def send_emailll(subject, message, recipients):
    # SMTP server configuration
    smtp_server = "smtp.gmail.com"
    smtp_port = 587  # Change it according to your SMTP server configuration
    smtp_username = "hostelhive00@gmail.com"
    # smtp_password = os.environ.get("SMTP_PASSWORD")
    smtp_password = "uprmgeoqsbeguwqr"
    # print("secret is : ",smtp_password)



    # Email content
    email_from = "hostelhive00@gmail.com"
    email_to = recipients
    email_subject = subject
    email_message = message

    # Create a MIME multipart message
    msg = MIMEMultipart()
    msg['From'] = email_from
    msg['To'] = ', '.join(email_to)
    msg['Subject'] = email_subject

    # Attach the message to the email
    msg.attach(MIMEText(email_message, 'plain'))

    try:
        # Create an SMTP connection
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            # Identify yourself to the SMTP server
            server.ehlo()

            # Start TLS encryption
            server.starttls()

            # Login to the SMTP server
            server.login(smtp_username, smtp_password)

            # Send the email
            server.sendmail(email_from, email_to, msg.as_string())

        print("Email sent successfully!")
        # messages.warning("Email sent successfully!")
    except Exception as e:
        # messages.warning(f"An error occurred while sending the email: {str(e)}")
        print(f"An error occurred while sending the email: {str(e)}")

def send_email(subject, message, recipients, attachment_path = '/Users/zohaibakhtar/Desktop/Hostel-Hive/Hostel-Hive/HostelBookingWebsite/invoice/invoice.pdf'):
    # SMTP server configuration
    smtp_server = "smtp.gmail.com"
    smtp_port = 587  # Change it according to your SMTP server configuration
    smtp_username = "hostelhive00@gmail.com"
    smtp_password = "uprmgeoqsbeguwqr"

    # Email content
    email_from = "hostelhive00@gmail.com"
    email_to = recipients
    email_subject = subject
    email_message = message

    # Create a MIME multipart message
    msg = MIMEMultipart()
    msg['From'] = email_from
    msg['To'] = ', '.join(email_to)
    msg['Subject'] = email_subject

    # Attach the message to the email
    msg.attach(MIMEText(email_message, 'plain'))

    # Add the PDF attachment if provided
    if attachment_path:
        with open(attachment_path, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename=invoice.pdf')
            msg.attach(part)

    try:
        # Create an SMTP connection
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            # Identify yourself to the SMTP server
            server.ehlo()

            # Start TLS encryption
            server.starttls()

            # Login to the SMTP server
            server.login(smtp_username, smtp_password)

            # Send the email
            server.sendmail(email_from, email_to, msg.as_string())

        print("Email sent successfully!")
    except Exception as e:
        print(f"An error occurred while sending the email: {str(e)}")


def index(request):
    data = []
    with open('./static/pincodes.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
        if data != []:
            print("\n\n\n\t location list send successfully \n\n\n")
        else :
            print("\n\n\n\tsending locations list failed\n\n\n")

    context = {'data': data}

    return render(request,'index.html', context)
    
def home(request):
    return HttpResponse("This is the home page")

def about(request):
    return render(request,'about.html')
def pricing(request):
    return render(request,'pricing.html')
def booknow(request):
    data = []
    with open('./static/pincodes.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
        if data != []:
            print("\n\n\n\t location list send successfully \n\n\n")
        else :
            print("\n\n\n\tsending locations list failed\n\n\n")

    context = {'data': data}
    if request.method == "POST" :
        name = request.POST.get('name')
        country_zip = request.POST.get('country_zip')
        checkin =  request.POST.get('checkin')
        checkout = request.POST.get('checkout')
        rooms = request.POST.get('rooms')
        adults = request.POST.get('adults')
        children = request.POST.get('children')
        email = request.POST.get('email')
        phonenumber = request.POST.get('phonenumber')
        bknow = Booknow(name = name , country_zip = country_zip, checkin = checkin , checkout = checkout, rooms = rooms  ,adults=adults, children = children , email=email , phonenumber = phonenumber)
        bknow.save()
        # i want this messages to print if and only if the data is saved without anyissues
        try:
            bknow.save()
            messages.warning(request, "Your Reservation is Successfully Registered")
            messages.success(request, "We will shortly contact you through your email or phone number")
            # Example usage
            subject = "🌟 Welcome to HostelHive! - Reservation Confirmation🌟"
            today_date = datetime.today().strftime("%d %b, %Y")
            invoice_data = {
                'today_date': today_date,
                'my_name': name,
                'country_zip': country_zip,
                'checkin': checkin,
                'checkout': checkout,
                'rooms': rooms,
                'adults': adults,
                'children': children,
                'email': email,
                'phonenumber': phonenumber
            # Additional data required for the invoice
            }
            generate_invoice(invoice_data)
            message = f"""
                    

Dear {name},

Thank you 🙏 for choosing our hostel booking service. We are delighted to inform you that we have received your reservation request. Your details have been successfully recorded, and we are currently processing your booking.

Here are the details of your reservation:

🏨 Name: {name}
🌍 City/ZIP: {country_zip}
📅 Check-in: {checkin}
📆 Check-out: {checkout}
🛌 Rooms: {rooms}
👥 Adults: {adults}
🧒 Children: {children}
📧 Email: {email}
📞 Phone Number: {phonenumber}

We understand the importance of a smooth and enjoyable stay, and our team is working diligently to confirm your reservation. We will reach out to you shortly with further information and to provide the status of your booking.

🚀 If you have any questions or require any additional assistance, please feel free to contact us at any time. We are here to ensure your stay is as comfortable as possible.

Thank you again for choosing our hostel booking service. We look forward to welcoming you soon.

Warm regards,

HostelHive 🏰 
"Experience the world on a budget"



📞 CONTACT US 
+91 43523450972
+91 23475928723
 📧 hostelhive00@gmail.com


Please note: This is an automated message. Please do not reply to this email.
                    """
            recipients = [email]
            send_email(subject, message, recipients)
        except Exception as e:
            messages.error(request, f"An error occurred while saving the reservation: {str(e)}")
    return render(request,'booknow.html',context)

def location(request):
    data = []
    with open('./static/pincodes.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
        if data != []:
            print("\n\n\n\tsuccess\n\n\n")
        else :
            print("\n\n\n\tfailed\n\n\n")

    context = {'data': data}
    # print(context)
    return render(request,'location.html', context)
