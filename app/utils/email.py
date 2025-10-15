import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from ..config import settings

def send_budget_exceeded_email(to_email: str, category_name: str, budget_amount: float, spent_amount: float):
    subject = f"Budget Exceeded Alert: {category_name}"
    
    body = f"""
    <html>
        <body>
            <h2>🚨 Budget Exceeded Alert!</h2>
            <p>Your budget for <strong>{category_name}</strong> has been exceeded.</p>
            <ul>
                <li>Budget Amount: ₹{budget_amount:.2f}</li>
                <li>Spent Amount: ₹{spent_amount:.2f}</li>
                <li>Exceeded By: ₹{(spent_amount - budget_amount):.2f}</li>
            </ul>
            <p>Please review your expenses.</p>
        </body>
    </html>
    """
    
    message = MIMEMultipart()
    message["From"] = settings.EMAIL_FROM
    message["To"] = to_email
    message["Subject"] = subject
    
    message.attach(MIMEText(body, "html"))
    
    try:
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(message)
        print(f"Email sent successfully to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")

def send_budget_warning_email(to_email: str, category_name: str, budget_amount: float, spent_amount: float):
    """Send warning when spending reaches 80% of budget"""
    percentage = (spent_amount / budget_amount) * 100
    
    subject = f"Budget Warning: {category_name} - {percentage:.0f}% Used"
    
    body = f"""
    <html>
        <body>
            <h2>⚠️ Budget Warning</h2>
            <p>You've used <strong>{percentage:.0f}%</strong> of your budget for <strong>{category_name}</strong>.</p>
            <ul>
                <li>Budget Amount: ₹{budget_amount:.2f}</li>
                <li>Spent Amount: ₹{spent_amount:.2f}</li>
                <li>Remaining: ₹{(budget_amount - spent_amount):.2f}</li>
            </ul>
            <p>Consider reviewing your spending to stay within budget.</p>
        </body>
    </html>
    """
    
    message = MIMEMultipart()
    message["From"] = settings.EMAIL_FROM
    message["To"] = to_email
    message["Subject"] = subject
    
    message.attach(MIMEText(body, "html"))
    
    try:
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(message)
        print(f"Warning email sent successfully to {to_email}")
    except Exception as e:
        print(f"Failed to send warning email: {str(e)}")
