import os
import smtplib
import logging
from logging.handlers import RotatingFileHandler 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)


SMTP_HOST = os.environ.get('SMTP_HOST', 'smtp.gmail.com')
SMTP_PORT = int(os.environ.get('SMTP_PORT', '587'))
SMTP_USER = os.environ.get('SMTP_USER')
SMTP_PASS = os.environ.get('SMTP_PASS')
RECIPIENT_EMAIL = os.environ.get('RECIPIENT_EMAIL')
NODE_ENV = os.environ.get('NODE_ENV', 'development')

def setup_logging():
    # Create a rotating log file (5MB max, keep 3 backups)
    file_handler = RotatingFileHandler("app.log", maxBytes=5 * 1024 * 1024, backupCount=3)
    file_handler.setLevel(logging.ERROR)  # only log errors
    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
    )
    file_handler.setFormatter(formatter)

    # Attach to app logger
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.DEBUG)  # log everything, filter via handlers

setup_logging()
def _create_smtp_client():
  """Create and return an authenticated SMTP client."""
  use_ssl = SMTP_PORT == 465
  if use_ssl:
    server = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT)
  else:
    server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
    server.ehlo()
    server.starttls()
  server.login(SMTP_USER, SMTP_PASS)
  return server


def _send_email(to_email: str, subject: str, html_body: str, text_body: str | None = None):
  msg = MIMEMultipart('alternative')
  msg['From'] = SMTP_USER
  msg['To'] = to_email
  msg['Subject'] = subject

  if text_body:
    msg.attach(MIMEText(text_body, 'plain', 'utf-8'))
  msg.attach(MIMEText(html_body, 'html', 'utf-8'))

  with _create_smtp_client() as client:
    client.sendmail(SMTP_USER, [to_email], msg.as_string())


def get_email_template(name: str, email: str, company: str | None, phone: str | None, message: str, timestamp: str) -> str:
  safe_company = company if company else 'Not provided'
  safe_phone = phone if phone else 'Not provided'
  safe_message_html = (message or '').replace('\n', '<br>')
  return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>New Contact Enquiry</title>
</head>
<body style="margin: 0; padding: 20px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f5f7fa;">
    <div style="max-width: 650px; margin: 0 auto; background-color: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.08);">
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 30px; text-align: center;">
            <div style="background-color: rgba(255,255,255,0.15); display: inline-block; padding: 12px 24px; border-radius: 25px; margin-bottom: 20px;">
                <h1 style="color: #ffffff; margin: 0; font-size: 24px; font-weight: 600; letter-spacing: 0.5px;">📧 New Contact Enquiry</h1>
            </div>
            <p style="color: rgba(255,255,255,0.9); margin: 0; font-size: 16px; font-weight: 300;">Shree Bharatraj Corporation</p>
        </div>

        <div style="padding: 30px;">
            <div style="background: linear-gradient(135deg, #f8faff 0%, #f0f4ff 100%); border: 1px solid #e1e8ff; border-radius: 10px; padding: 25px; margin-bottom: 25px; position: relative;">
                <div style="position: absolute; top: -10px; left: 25px; background-color: #667eea; color: white; padding: 5px 15px; border-radius: 15px; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">Contact Details</div>

                <div style="margin-top: 10px;">
                    <div style="display: flex; align-items: center; margin-bottom: 15px;">
                        <div style="width: 40px; height: 40px; background: linear-gradient(135deg, #667eea, #764ba2); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 15px;">
                            <span style="color: #ffffff; font-size: 18px; display: flex; align-items: center; justify-content: center; width: 100%; height: 100%; line-height: 1;">👤</span>
                        </div>
                        <div>
                            <p style="margin: 0; color: #6b7280; font-size: 13px; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px;">Full Name</p>
                            <p style="margin: 0; color: #1f2937; font-size: 16px; font-weight: 600;">{name}</p>
                        </div>
                    </div>

                    <div style="display: flex; align-items: center; margin-bottom: 15px;">
                        <div style="width: 40px; height: 40px; background: linear-gradient(135deg, #10b981, #059669); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 15px;">
                            <span style="color: #ffffff; font-size: 18px; display: flex; align-items: center; justify-content: center; width: 100%; height: 100%; line-height: 1;">✉️</span>
                        </div>
                        <div>
                            <p style="margin: 0; color: #6b7280; font-size: 13px; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px;">Email Address</p>
                            <p style="margin: 0; color: #1f2937; font-size: 16px; font-weight: 600;">{email}</p>
                        </div>
                    </div>

                    <div style="display: flex; align-items: center; margin-bottom: 15px;">
                        <div style="width: 40px; height: 40px; background: linear-gradient(135deg, #f59e0b, #d97706); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 15px;">
                            <span style="color: #ffffff; font-size: 18px; display: flex; align-items: center; justify-content: center; width: 100%; height: 100%; line-height: 1;">🏢</span>
                        </div>
                        <div>
                            <p style="margin: 0; color: #6b7280; font-size: 13px; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px;">Company</p>
                            <p style="margin: 0; color: #1f2937; font-size: 16px; font-weight: 600;">{safe_company}</p>
                        </div>
                    </div>

                    <div style="display: flex; align-items: center;">
                        <div style="width: 40px; height: 40px; background: linear-gradient(135deg, #8b5cf6, #7c3aed); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 15px;">
                            <span style="color: #ffffff; font-size: 18px; display: flex; align-items: center; justify-content: center; width: 100%; height: 100%; line-height: 1;">📱</span>
                        </div>
                        <div>
                            <p style="margin: 0; color: #6b7280; font-size: 13px; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px;">Phone Number</p>
                            <p style="margin: 0; color: #1f2937; font-size: 16px; font-weight: 600;">{safe_phone}</p>
                        </div>
                    </div>
                </div>
            </div>

            <div style="background-color: #ffffff; border: 2px solid #e5e7eb; border-radius: 10px; padding: 25px; position: relative;">
                <div style="position: absolute; top: -10px; left: 25px; background-color: #1f2937; color: white; padding: 5px 15px; border-radius: 15px; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">Message Content</div>
                <div style="margin-top: 15px;">
                    <div style="background-color: #f9fafb; padding: 20px; border-radius: 8px; border-left: 4px solid #667eea;">
                        <p style="margin: 0; color: #374151; font-size: 15px; line-height: 1.7;">{safe_message_html}</p>
                    </div>
                </div>
            </div>

            <div style="text-align: center; margin: 30px 0;">
                <a href="mailto:{email}" style="display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; text-decoration: none; padding: 12px 30px; border-radius: 25px; font-weight: 600; font-size: 14px; margin: 0 10px 10px 0;">📧 Reply to {name}</a>
                {f'<a href="tel:{phone}" style="display: inline-block; background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; text-decoration: none; padding: 12px 30px; border-radius: 25px; font-weight: 600; font-size: 14px; margin: 0 10px 10px 0;">📞 Call Now</a>' if phone else ''}
            </div>

            <div style="text-align: center; padding: 20px; background-color: #f8fafc; border-radius: 8px; border: 1px dashed #d1d5db;">
                <p style="margin: 0; color: #6b7280; font-size: 13px; font-weight: 500;"><span style="display: inline-block; margin-right: 10px;">🕐</span>Received on: {timestamp}</p>
                <p style="margin: 5px 0 0 0; color: #9ca3af; font-size: 11px;">Via Shree Bharatraj Corporation Website Contact Form</p>
            </div>
        </div>

        <div style="background-color: #1f2937; padding: 25px; text-align: center;">
            <div style="margin-bottom: 15px;">
                <h3 style="color: #ffffff; margin: 0 0 10px 0; font-size: 18px; font-weight: 600;">Shree Bharatraj Corporation</h3>
                <p style="color: #9ca3af; margin: 0; font-size: 14px; line-height: 1.5;">Excellence in Business Solutions</p>
            </div>
            <div style="border-top: 1px solid #374151; padding-top: 15px;">
                <p style="color: #6b7280; margin: 0; font-size: 12px;">This email was automatically generated from your website contact form.<br>Please respond to this enquiry at your earliest convenience.</p>
            </div>
        </div>
    </div>
</body>
</html>
  """


def get_acknowledgment_template(name: str, message: str) -> str:
  safe_message_html = (message or '').replace('\n', '<br>')
  return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Thank You - Shree Bharatraj Corporation</title>
</head>
<body style="margin: 0; padding: 20px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f5f7fa;">
    <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.08);">
        <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); padding: 40px 30px; text-align: center;">
            <h1 style="color: #ffffff; margin: 0; font-size: 28px; font-weight: 600;">✅ Thank You, {name}!</h1>
            <p style="color: rgba(255,255,255,0.9); margin: 15px 0 0 0; font-size: 16px;">We've received your enquiry</p>
        </div>

        <div style="padding: 40px 30px;">
            <div style="text-align: center; margin-bottom: 30px;">
                <div style="width: 80px; height: 80px; background: linear-gradient(135deg, #10b981, #059669); border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; margin-bottom: 20px;">
                    <span style="color: white; font-size: 32px;">📨</span>
                </div>
                <h2 style="color: #1f2937; margin: 0 0 15px 0; font-size: 24px; font-weight: 600;">Your Message Has Been Received</h2>
                <p style="color: #6b7280; margin: 0; font-size: 16px; line-height: 1.6;">Thank you for contacting us. Our team will review your enquiry and get back to you within 24 hours.</p>
            </div>

            <div style="background-color: #f0fdfa; border: 1px solid #a7f3d0; border-radius: 10px; padding: 25px; margin: 25px 0;">
                <h3 style="color: #065f46; margin: 0 0 15px 0; font-size: 16px; font-weight: 600;">📝 Your Message Summary:</h3>
                <div style="background-color: #ffffff; padding: 20px; border-radius: 8px; border-left: 4px solid #10b981;">
                    <p style="margin: 0; color: #374151; font-size: 14px; line-height: 1.7;">{safe_message_html}</p>
                </div>
            </div>

            <div style="background-color: #f8fafc; border-radius: 10px; padding: 25px; text-align: center;">
                <h3 style="color: #1f2937; margin: 0 0 15px 0; font-size: 18px; font-weight: 600;">What Happens Next?</h3>
                <div style="text-align: left; max-width: 400px; margin: 0 auto;">
                    <div style="display: flex; align-items: center; margin-bottom: 15px;">
                        <div style="width: 36px; height: 36px; background: #10b981; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 15px;"><span style="color: #ffffff; font-size: 16px; font-weight: 700; line-height: 1; width: 100%; text-align: center;">1</span></div>
                        <p style="margin: 0; color: #374151; font-size: 14px;">Our team reviews your enquiry</p>
                    </div>
                    <div style="display: flex; align-items: center; margin-bottom: 15px;">
                        <div style="width: 36px; height: 36px; background: #10b981; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 15px;"><span style="color: #ffffff; font-size: 16px; font-weight: 700; line-height: 1; width: 100%; text-align: center;">2</span></div>
                        <p style="margin: 0; color: #374151; font-size: 14px;">We prepare a personalized response</p>
                    </div>
                    <div style="display: flex; align-items: center;">
                        <div style="width: 36px; height: 36px; background: #10b981; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 15px;"><span style="color: #ffffff; font-size: 16px; font-weight: 700; line-height: 1; width: 100%; text-align: center;">3</span></div>
                        <p style="margin: 0; color: #374151; font-size: 14px;">You receive our detailed response within 24 hours</p>
                    </div>
                </div>
            </div>
        </div>

        <div style="background-color: #1f2937; padding: 30px; text-align: center;">
            <h3 style="color: #ffffff; margin: 0 0 10px 0; font-size: 20px; font-weight: 600;">Shree Bharatraj Corporation</h3>
            <p style="color: #9ca3af; margin: 0 0 20px 0; font-size: 14px;">Excellence in Business Solutions</p>
            <div style="border-top: 1px solid #374151; padding-top: 20px;">
                <p style="color: #6b7280; margin: 0; font-size: 12px; line-height: 1.5;">This is an automated acknowledgment email.<br>Please do not reply to this email address.</p>
            </div>
        </div>
    </div>
</body>
</html>
  """


@app.route('/api/send-email', methods=['POST'])
def send_email():
  try:
    data = request.get_json(silent=True) or {}
    name = data.get('name')
    email = data.get('email')
    company = data.get('company')
    phone = data.get('phone')
    message = data.get('message')

    if not name or not email or not message:
      return jsonify({ 'success': False, 'message': 'Name, email, and message are required' }), 400

    timestamp = datetime.now().astimezone().strftime('%B %d, %Y, %I:%M:%S %p')

    html = get_email_template(name, email, company, phone, message, timestamp)
    text = f"""
New Contact Form Submission

Name: {name}
Email: {email}
Company: {company or 'Not provided'}
Phone: {phone or 'Not provided'}

Message:
{message}

Received on: {timestamp}
Via Shree Bharatraj Corporation Website Contact Form
    """.strip()

    subject = f"🔔 New Contact Form Submission from {name}"
    _send_email(RECIPIENT_EMAIL, subject, html, text)

    # Fire-and-forget style (best effort) acknowledgment
    try:
      ack_subject = '✅ We received your enquiry - Shree Bharatraj Corporation'
      ack_html = get_acknowledgment_template(name, message)
      ack_text = f"""Thank you, {name}!

We have received your enquiry and will get back to you within 24 hours.

Your message:
{message}

What happens next?
1. Our team reviews your enquiry
2. We prepare a personalized response  
3. You receive our detailed response within 24 hours

---
Shree Bharatraj Corporation
Excellence in Business Solutions

This is an automated acknowledgment email.
Please do not reply to this email address."""
      _send_email(email, ack_subject, ack_html, ack_text)
    except Exception as ack_err:
      app.logger.error(f"Acknowledgement email failed: {ack_err}")

    return jsonify({ 'success': True, 'message': 'Email sent successfully' })
  except Exception as e:
    app.logger.error(f"Error sending email: {e}")
    return jsonify({ 'success': False, 'message': 'Failed to send email. Please try again later.' }), 500


@app.route('/api/health', methods=['GET'])
def health():
  return jsonify({
    'success': True,
    'message': 'Server is running',
    'timestamp': datetime.utcnow().isoformat() + 'Z',
    'smtp_configured': bool(SMTP_USER)
  })


@app.route('/api/test-email', methods=['POST'])
def test_email():
  if NODE_ENV == 'production':
    return jsonify({ 'success': False, 'message': 'Test endpoint not available in production' }), 403
  try:
    test_data = {
      'name': 'John Doe',
      'email': 'john.doe@example.com',
      'company': 'Test Company Pvt Ltd',
      'phone': '+91 98765 43210',
      'message': 'This is a test message to verify the email template design and functionality.'
    }

    timestamp = datetime.now().astimezone().strftime('%B %d, %Y, %I:%M:%S %p')
    html = get_email_template(test_data['name'], test_data['email'], test_data['company'], test_data['phone'], test_data['message'], timestamp)

    _send_email(SMTP_USER, '🧪 Test Email - Template Preview', html)

    return jsonify({
      'success': True,
      'message': 'Test email sent successfully',
      'testData': test_data
    })
  except Exception as e:
    app.logger.error(f"Error sending test email: {e}")
    return jsonify({ 'success': False, 'message': 'Failed to send test email', 'error': str(e) }), 500


def _verify_smtp_on_startup():
  try:
    with _create_smtp_client() as client:
      app.logger.info('✅ SMTP Server is ready to take our messages')
  except Exception as e:
    app.logger.error(f"SMTP Error: {e}")

@app.errorhandler(500)
def internal_error(e):
    app.logger.error("Server Error: %s", e, exc_info=True)
    return "An internal server error occurred. Check logs for details.", 500

if __name__ == '__main__':
    _verify_smtp_on_startup()

    port = int(os.environ.get('PORT', 5000))  # use port from environment if available
    host = '0.0.0.0'  # needed for deployment platforms to allow external access

    app.logger.info(f"🚀 Server running on port {port}")
    app.logger.info(f"📧 SMTP configured for: {SMTP_USER}")
    app.logger.info(f"🎯 Recipient email: {RECIPIENT_EMAIL}")
    app.logger.info(f"🌍 Environment: {NODE_ENV}")

    app.run(host=host, port=port, debug=True)


