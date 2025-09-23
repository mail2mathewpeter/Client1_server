const express = require('express');
const nodemailer = require('nodemailer');
const cors = require('cors');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(express.json());

// SMTP Configuration
const transporter = nodemailer.createTransport({
  host: process.env.SMTP_HOST || 'smtp.gmail.com',
  port: process.env.SMTP_PORT || 587,
  secure: false, // true for 465, false for other ports
  auth: {
    user: process.env.SMTP_USER, // your email
    pass: process.env.SMTP_PASS  // your email password or app password
  }
});

// Verify SMTP connection
transporter.verify((error, success) => {
  if (error) {
    console.log('SMTP Error:', error);
  } else {
    console.log('✅ SMTP Server is ready to take our messages');
  }
});

// Professional Email Template Function
function getEmailTemplate(name, email, company, phone, message, timestamp) {
  return `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>New Contact Enquiry</title>
</head>
<body style="margin: 0; padding: 20px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f5f7fa;">
    
    <!-- Main Container -->
    <div style="max-width: 650px; margin: 0 auto; background-color: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.08);">
        
        <!-- Header Section -->
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 30px; text-align: center;">
            <div style="background-color: rgba(255,255,255,0.15); display: inline-block; padding: 12px 24px; border-radius: 25px; margin-bottom: 20px;">
                <h1 style="color: #ffffff; margin: 0; font-size: 24px; font-weight: 600; letter-spacing: 0.5px;">
                    📧 New Contact Enquiry
                </h1>
            </div>
            <p style="color: rgba(255,255,255,0.9); margin: 0; font-size: 16px; font-weight: 300;">
                Shree Bharatraj Corporation
            </p>
        </div>

        <!-- Contact Information Card -->
        <div style="padding: 30px;">
            <div style="background: linear-gradient(135deg, #f8faff 0%, #f0f4ff 100%); border: 1px solid #e1e8ff; border-radius: 10px; padding: 25px; margin-bottom: 25px; position: relative;">
                <div style="position: absolute; top: -10px; left: 25px; background-color: #667eea; color: white; padding: 5px 15px; border-radius: 15px; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">
                    Contact Details
                </div>
                
                <div style="margin-top: 10px;">
                    <div style="display: flex; align-items: center; margin-bottom: 15px;">
                        <div style="width: 40px; height: 40px; background: linear-gradient(135deg, #667eea, #764ba2); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 15px;">
                            <span style="color: #ffffff; font-size: 18px; display: flex; align-items: center; justify-content: center; width: 100%; height: 100%; line-height: 1;">👤</span>
                        </div>
                        <div>
                            <p style="margin: 0; color: #6b7280; font-size: 13px; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px;">Full Name</p>
                            <p style="margin: 0; color: #1f2937; font-size: 16px; font-weight: 600;">${name}</p>
                        </div>
                    </div>

                    <div style="display: flex; align-items: center; margin-bottom: 15px;">
                        <div style="width: 40px; height: 40px; background: linear-gradient(135deg, #10b981, #059669); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 15px;">
                            <span style="color: #ffffff; font-size: 18px; display: flex; align-items: center; justify-content: center; width: 100%; height: 100%; line-height: 1;">✉️</span>
                        </div>
                        <div>
                            <p style="margin: 0; color: #6b7280; font-size: 13px; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px;">Email Address</p>
                            <p style="margin: 0; color: #1f2937; font-size: 16px; font-weight: 600;">${email}</p>
                        </div>
                    </div>

                    <div style="display: flex; align-items: center; margin-bottom: 15px;">
                        <div style="width: 40px; height: 40px; background: linear-gradient(135deg, #f59e0b, #d97706); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 15px;">
                            <span style="color: #ffffff; font-size: 18px; display: flex; align-items: center; justify-content: center; width: 100%; height: 100%; line-height: 1;">🏢</span>
                        </div>
                        <div>
                            <p style="margin: 0; color: #6b7280; font-size: 13px; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px;">Company</p>
                            <p style="margin: 0; color: #1f2937; font-size: 16px; font-weight: 600;">${company || 'Not provided'}</p>
                        </div>
                    </div>

                    <div style="display: flex; align-items: center;">
                        <div style="width: 40px; height: 40px; background: linear-gradient(135deg, #8b5cf6, #7c3aed); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 15px;">
                            <span style="color: #ffffff; font-size: 18px; display: flex; align-items: center; justify-content: center; width: 100%; height: 100%; line-height: 1;">📱</span>
                        </div>
                        <div>
                            <p style="margin: 0; color: #6b7280; font-size: 13px; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px;">Phone Number</p>
                            <p style="margin: 0; color: #1f2937; font-size: 16px; font-weight: 600;">${phone || 'Not provided'}</p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Message Section -->
            <div style="background-color: #ffffff; border: 2px solid #e5e7eb; border-radius: 10px; padding: 25px; position: relative;">
                <div style="position: absolute; top: -10px; left: 25px; background-color: #1f2937; color: white; padding: 5px 15px; border-radius: 15px; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">
                    Message Content
                </div>
                
                <div style="margin-top: 15px;">
                    <div style="background-color: #f9fafb; padding: 20px; border-radius: 8px; border-left: 4px solid #667eea;">
                        <p style="margin: 0; color: #374151; font-size: 15px; line-height: 1.7;">${message.replace(/\n/g, '<br>')}</p>
                    </div>
                </div>
            </div>

            <!-- Action Buttons -->
            <div style="text-align: center; margin: 30px 0;">
                <a href="mailto:${email}" style="display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; text-decoration: none; padding: 12px 30px; border-radius: 25px; font-weight: 600; font-size: 14px; margin: 0 10px 10px 0;">
                    📧 Reply to ${name}
                </a>
                ${phone ? `<a href="tel:${phone}" style="display: inline-block; background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; text-decoration: none; padding: 12px 30px; border-radius: 25px; font-weight: 600; font-size: 14px; margin: 0 10px 10px 0;">
                    📞 Call Now
                </a>` : ''}
            </div>

            <!-- Timestamp -->
            <div style="text-align: center; padding: 20px; background-color: #f8fafc; border-radius: 8px; border: 1px dashed #d1d5db;">
                <p style="margin: 0; color: #6b7280; font-size: 13px; font-weight: 500;">
                    <span style="display: inline-block; margin-right: 10px;">🕐</span>
                    Received on: ${timestamp}
                </p>
                <p style="margin: 5px 0 0 0; color: #9ca3af; font-size: 11px;">
                    Via Shree Bharatraj Corporation Website Contact Form
                </p>
            </div>
        </div>

        <!-- Footer -->
        <div style="background-color: #1f2937; padding: 25px; text-align: center;">
            <div style="margin-bottom: 15px;">
                <h3 style="color: #ffffff; margin: 0 0 10px 0; font-size: 18px; font-weight: 600;">
                    Shree Bharatraj Corporation
                </h3>
                <p style="color: #9ca3af; margin: 0; font-size: 14px; line-height: 1.5;">
                    Excellence in Business Solutions
                </p>
            </div>
            
            <div style="border-top: 1px solid #374151; padding-top: 15px;">
                <p style="color: #6b7280; margin: 0; font-size: 12px;">
                    This email was automatically generated from your website contact form.
                    <br>
                    Please respond to this enquiry at your earliest convenience.
                </p>
            </div>
        </div>
    </div>
</body>
</html>
  `;
}

// Acknowledgment Email Template
function getAcknowledgmentTemplate(name, message) {
  return `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Thank You - Shree Bharatraj Corporation</title>
</head>
<body style="margin: 0; padding: 20px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f5f7fa;">
    
    <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.08);">
        
        <!-- Header -->
        <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); padding: 40px 30px; text-align: center;">
            <h1 style="color: #ffffff; margin: 0; font-size: 28px; font-weight: 600;">
                ✅ Thank You, ${name}!
            </h1>
            <p style="color: rgba(255,255,255,0.9); margin: 15px 0 0 0; font-size: 16px;">
                We've received your enquiry
            </p>
        </div>

        <!-- Content -->
        <div style="padding: 40px 30px;">
            <div style="text-align: center; margin-bottom: 30px;">
                <div style="width: 80px; height: 80px; background: linear-gradient(135deg, #10b981, #059669); border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; margin-bottom: 20px;">
                    <span style="color: white; font-size: 32px;">📨</span>
                </div>
                <h2 style="color: #1f2937; margin: 0 0 15px 0; font-size: 24px; font-weight: 600;">
                    Your Message Has Been Received
                </h2>
                <p style="color: #6b7280; margin: 0; font-size: 16px; line-height: 1.6;">
                    Thank you for contacting us. Our team will review your enquiry and get back to you within 24 hours.
                </p>
            </div>

            <!-- Message Summary -->
            <div style="background-color: #f0fdfa; border: 1px solid #a7f3d0; border-radius: 10px; padding: 25px; margin: 25px 0;">
                <h3 style="color: #065f46; margin: 0 0 15px 0; font-size: 16px; font-weight: 600;">
                    📝 Your Message Summary:
                </h3>
                <div style="background-color: #ffffff; padding: 20px; border-radius: 8px; border-left: 4px solid #10b981;">
                    <p style="margin: 0; color: #374151; font-size: 14px; line-height: 1.7;">${message.replace(/\n/g, '<br>')}</p>
                </div>
            </div>

            <!-- What's Next -->
            <div style="background-color: #f8fafc; border-radius: 10px; padding: 25px; text-align: center;">
                <h3 style="color: #1f2937; margin: 0 0 15px 0; font-size: 18px; font-weight: 600;">
                    What Happens Next?
                </h3>
                <div style="text-align: left; max-width: 400px; margin: 0 auto;">
                    <div style="display: flex; align-items: center; margin-bottom: 15px;">
                        <div style="width: 36px; height: 36px; background: #10b981; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 15px;">
                            <span style="color: #ffffff; font-size: 16px; font-weight: 700; line-height: 1; width: 100%; text-align: center;">1</span>
                        </div>
                        <p style="margin: 0; color: #374151; font-size: 14px;">Our team reviews your enquiry</p>
                    </div>
                    <div style="display: flex; align-items: center; margin-bottom: 15px;">
                        <div style="width: 36px; height: 36px; background: #10b981; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 15px;">
                            <span style="color: #ffffff; font-size: 16px; font-weight: 700; line-height: 1; width: 100%; text-align: center;">2</span>
                        </div>
                        <p style="margin: 0; color: #374151; font-size: 14px;">We prepare a personalized response</p>
                    </div>
                    <div style="display: flex; align-items: center;">
                        <div style="width: 36px; height: 36px; background: #10b981; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 15px;">
                            <span style="color: #ffffff; font-size: 16px; font-weight: 700; line-height: 1; width: 100%; text-align: center;">3</span>
                        </div>
                        <p style="margin: 0; color: #374151; font-size: 14px;">You receive our detailed response within 24 hours</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Footer -->
        <div style="background-color: #1f2937; padding: 30px; text-align: center;">
            <h3 style="color: #ffffff; margin: 0 0 10px 0; font-size: 20px; font-weight: 600;">
                Shree Bharatraj Corporation
            </h3>
            <p style="color: #9ca3af; margin: 0 0 20px 0; font-size: 14px;">
                Excellence in Business Solutions
            </p>
            <div style="border-top: 1px solid #374151; padding-top: 20px;">
                <p style="color: #6b7280; margin: 0; font-size: 12px; line-height: 1.5;">
                    This is an automated acknowledgment email.<br>
                    Please do not reply to this email address.
                </p>
            </div>
        </div>
    </div>
</body>
</html>
  `;
}

// Email sending endpoint
app.post('/api/send-email', async (req, res) => {
  try {
    const { name, email, company, phone, message } = req.body;

    // Validate required fields
    if (!name || !email || !message) {
      return res.status(400).json({ 
        success: false, 
        message: 'Name, email, and message are required' 
      });
    }

    const timestamp = new Date().toLocaleString('en-IN', { 
      timeZone: 'Asia/Kolkata',
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });

    // Email content using the professional template
    const mailOptions = {
      from: process.env.SMTP_USER,
      to: process.env.RECIPIENT_EMAIL,
      subject: `🔔 New Contact Form Submission from ${name}`,
      html: getEmailTemplate(name, email, company, phone, message, timestamp),
      text: `
New Contact Form Submission

Name: ${name}
Email: ${email}
Company: ${company || 'Not provided'}
Phone: ${phone || 'Not provided'}

Message:
${message}

Received on: ${timestamp}
Via Shree Bharatraj Corporation Website Contact Form
      `
    };

    // Send email to site recipient
    const info = await transporter.sendMail(mailOptions);
    console.log('✅ Email sent successfully to recipient:', info.messageId);

    // Fire-and-forget acknowledgement to the user
    const ackMail = {
      from: process.env.SMTP_USER,
      to: email,
      subject: '✅ We received your enquiry - Shree Bharatraj Corporation',
      html: getAcknowledgmentTemplate(name, message),
      text: `Thank you, ${name}!

We have received your enquiry and will get back to you within 24 hours.

Your message:
${message}

What happens next?
1. Our team reviews your enquiry
2. We prepare a personalized response  
3. You receive our detailed response within 24 hours

---
Shree Bharatraj Corporation
Excellence in Business Solutions

This is an automated acknowledgment email.
Please do not reply to this email address.`
    };

    transporter.sendMail(ackMail).catch(err => {
      console.error('❌ Acknowledgement email failed:', err?.message || err);
    });

    res.json({
      success: true,
      message: 'Email sent successfully',
      messageId: info.messageId
    });

  } catch (error) {
    console.error('❌ Error sending email:', error);
    res.status(500).json({ 
      success: false, 
      message: 'Failed to send email. Please try again later.' 
    });
  }
});

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.json({ 
    success: true, 
    message: 'Server is running',
    timestamp: new Date().toISOString(),
    smtp_configured: !!process.env.SMTP_USER
  });
});

// Test email endpoint (for development)
app.post('/api/test-email', async (req, res) => {
  if (process.env.NODE_ENV === 'production') {
    return res.status(403).json({ 
      success: false, 
      message: 'Test endpoint not available in production' 
    });
  }

  try {
    const testData = {
      name: 'John Doe',
      email: 'john.doe@example.com',
      company: 'Test Company Pvt Ltd',
      phone: '+91 98765 43210',
      message: 'This is a test message to verify the email template design and functionality.'
    };

    const timestamp = new Date().toLocaleString('en-IN', { 
      timeZone: 'Asia/Kolkata',
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });

    const mailOptions = {
      from: process.env.SMTP_USER,
      to: process.env.SMTP_USER, // Send to yourself for testing
      subject: '🧪 Test Email - Template Preview',
      html: getEmailTemplate(testData.name, testData.email, testData.company, testData.phone, testData.message, timestamp)
    };

    const info = await transporter.sendMail(mailOptions);
    
    res.json({
      success: true,
      message: 'Test email sent successfully',
      messageId: info.messageId,
      testData
    });

  } catch (error) {
    console.error('❌ Error sending test email:', error);
    res.status(500).json({ 
      success: false, 
      message: 'Failed to send test email',
      error: error.message
    });
  }
});

app.listen(PORT, () => {
  console.log(`🚀 Server running on port ${PORT}`);
  console.log(`📧 SMTP configured for: ${process.env.SMTP_USER}`);
  console.log(`🎯 Recipient email: ${process.env.RECIPIENT_EMAIL}`);
  console.log(`🌍 Environment: ${process.env.NODE_ENV || 'development'}`);
});