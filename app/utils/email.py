import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from ..config import settings

def send_budget_exceeded_email(to_email: str, category_name: str, budget_amount: float, spent_amount: float):
    subject = f"🚨 Budget Alert: {category_name} Budget Exceeded"
    
    exceeded_by = spent_amount - budget_amount
    percentage = (spent_amount / budget_amount * 100) if budget_amount > 0 else 0
    
    body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                margin: 0;
                padding: 0;
                background-color: #f4f4f7;
            }}
            .container {{
                max-width: 600px;
                margin: 40px auto;
                background-color: #ffffff;
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }}
            .header {{
                background: linear-gradient(135deg, #dc2626 0%, #991b1b 100%);
                color: white;
                padding: 40px 30px;
                text-align: center;
            }}
            .header-icon {{
                font-size: 48px;
                margin-bottom: 10px;
            }}
            .header h1 {{
                margin: 0;
                font-size: 28px;
                font-weight: 600;
            }}
            .content {{
                padding: 40px 30px;
            }}
            .alert-box {{
                background-color: #fef2f2;
                border-left: 4px solid #dc2626;
                padding: 20px;
                margin-bottom: 30px;
                border-radius: 8px;
            }}
            .alert-box p {{
                margin: 0;
                color: #991b1b;
                font-size: 16px;
                font-weight: 500;
            }}
            .stats-grid {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
                margin: 30px 0;
            }}
            .stat-card {{
                background-color: #f9fafb;
                padding: 20px;
                border-radius: 8px;
                border: 1px solid #e5e7eb;
            }}
            .stat-label {{
                font-size: 12px;
                text-transform: uppercase;
                color: #6b7280;
                margin-bottom: 8px;
                font-weight: 600;
                letter-spacing: 0.5px;
            }}
            .stat-value {{
                font-size: 24px;
                font-weight: 700;
                color: #1f2937;
            }}
            .stat-value.exceeded {{
                color: #dc2626;
            }}
            .progress-bar {{
                width: 100%;
                height: 12px;
                background-color: #e5e7eb;
                border-radius: 6px;
                overflow: hidden;
                margin: 20px 0;
            }}
            .progress-fill {{
                height: 100%;
                background: linear-gradient(90deg, #dc2626 0%, #991b1b 100%);
                border-radius: 6px;
                transition: width 0.3s ease;
                width: {min(percentage, 100)}%;
            }}
            .progress-label {{
                text-align: center;
                font-size: 14px;
                color: #6b7280;
                margin-top: 8px;
            }}
            .cta-button {{
                display: inline-block;
                background: linear-gradient(135deg, #dc2626 0%, #991b1b 100%);
                color: white;
                padding: 14px 32px;
                text-decoration: none;
                border-radius: 8px;
                font-weight: 600;
                text-align: center;
                margin: 20px 0;
                box-shadow: 0 4px 6px rgba(220, 38, 38, 0.2);
            }}
            .footer {{
                background-color: #f9fafb;
                padding: 30px;
                text-align: center;
                border-top: 1px solid #e5e7eb;
            }}
            .footer p {{
                margin: 5px 0;
                color: #6b7280;
                font-size: 14px;
            }}
            .divider {{
                height: 1px;
                background-color: #e5e7eb;
                margin: 30px 0;
            }}
            @media only screen and (max-width: 600px) {{
                .container {{
                    margin: 20px;
                    border-radius: 8px;
                }}
                .header {{
                    padding: 30px 20px;
                }}
                .content {{
                    padding: 30px 20px;
                }}
                .stats-grid {{
                    grid-template-columns: 1fr;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="header-icon">🚨</div>
                <h1>Budget Exceeded</h1>
            </div>
            
            <div class="content">
                <div class="alert-box">
                    <p>Your spending in <strong>{category_name}</strong> has exceeded your budget!</p>
                </div>
                
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-label">Budget Amount</div>
                        <div class="stat-value">₹{budget_amount:,.2f}</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">Total Spent</div>
                        <div class="stat-value exceeded">₹{spent_amount:,.2f}</div>
                    </div>
                </div>
                
                <div class="stat-card" style="margin-top: 20px;">
                    <div class="stat-label">Exceeded By</div>
                    <div class="stat-value exceeded">₹{exceeded_by:,.2f}</div>
                </div>
                
                <div class="progress-bar">
                    <div class="progress-fill"></div>
                </div>
                <div class="progress-label">
                    <strong>{percentage:.0f}%</strong> of budget used
                </div>
                
                <div class="divider"></div>
                
                <p style="color: #6b7280; font-size: 15px; line-height: 1.6;">
                    It looks like your expenses in <strong>{category_name}</strong> have gone over your planned budget. 
                    Consider reviewing your recent transactions and adjusting your spending habits.
                </p>
                
                <center>
                    <a href="#" class="cta-button">View Expenses</a>
                </center>
            </div>
            
            <div class="footer">
                <p><strong>Money Manager</strong></p>
                <p>Helping you stay on top of your finances</p>
                <p style="font-size: 12px; color: #9ca3af; margin-top: 15px;">
                    You're receiving this because you set up budget alerts for your account.
                </p>
            </div>
        </div>
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
        print(f"✅ Budget exceeded email sent successfully to {to_email}")
        return True
    except Exception as e:
        print(f"❌ Failed to send email: {str(e)}")
        return False

def send_budget_warning_email(to_email: str, category_name: str, budget_amount: float, spent_amount: float):
    """Send warning when spending reaches 80% of budget"""
    percentage = (spent_amount / budget_amount) * 100 if budget_amount > 0 else 0
    remaining = budget_amount - spent_amount
    
    subject = f"⚠️ Budget Warning: {category_name} at {percentage:.0f}%"
    
    body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                margin: 0;
                padding: 0;
                background-color: #f4f4f7;
            }}
            .container {{
                max-width: 600px;
                margin: 40px auto;
                background-color: #ffffff;
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }}
            .header {{
                background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
                color: white;
                padding: 40px 30px;
                text-align: center;
            }}
            .header-icon {{
                font-size: 48px;
                margin-bottom: 10px;
            }}
            .header h1 {{
                margin: 0;
                font-size: 28px;
                font-weight: 600;
            }}
            .content {{
                padding: 40px 30px;
            }}
            .warning-box {{
                background-color: #fffbeb;
                border-left: 4px solid #f59e0b;
                padding: 20px;
                margin-bottom: 30px;
                border-radius: 8px;
            }}
            .warning-box p {{
                margin: 0;
                color: #92400e;
                font-size: 16px;
                font-weight: 500;
            }}
            .stats-grid {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
                margin: 30px 0;
            }}
            .stat-card {{
                background-color: #f9fafb;
                padding: 20px;
                border-radius: 8px;
                border: 1px solid #e5e7eb;
            }}
            .stat-label {{
                font-size: 12px;
                text-transform: uppercase;
                color: #6b7280;
                margin-bottom: 8px;
                font-weight: 600;
                letter-spacing: 0.5px;
            }}
            .stat-value {{
                font-size: 24px;
                font-weight: 700;
                color: #1f2937;
            }}
            .stat-value.warning {{
                color: #f59e0b;
            }}
            .stat-value.remaining {{
                color: #059669;
            }}
            .progress-bar {{
                width: 100%;
                height: 12px;
                background-color: #e5e7eb;
                border-radius: 6px;
                overflow: hidden;
                margin: 20px 0;
                position: relative;
            }}
            .progress-fill {{
                height: 100%;
                background: linear-gradient(90deg, #f59e0b 0%, #d97706 100%);
                border-radius: 6px;
                transition: width 0.3s ease;
                width: {percentage}%;
            }}
            .progress-label {{
                text-align: center;
                font-size: 14px;
                color: #6b7280;
                margin-top: 8px;
            }}
            .tips-box {{
                background-color: #f0fdf4;
                border: 1px solid #86efac;
                border-radius: 8px;
                padding: 20px;
                margin: 30px 0;
            }}
            .tips-box h3 {{
                margin: 0 0 15px 0;
                color: #065f46;
                font-size: 16px;
                display: flex;
                align-items: center;
            }}
            .tips-box ul {{
                margin: 0;
                padding-left: 20px;
                color: #047857;
            }}
            .tips-box li {{
                margin: 8px 0;
            }}
            .cta-button {{
                display: inline-block;
                background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
                color: white;
                padding: 14px 32px;
                text-decoration: none;
                border-radius: 8px;
                font-weight: 600;
                text-align: center;
                margin: 20px 0;
                box-shadow: 0 4px 6px rgba(245, 158, 11, 0.2);
            }}
            .footer {{
                background-color: #f9fafb;
                padding: 30px;
                text-align: center;
                border-top: 1px solid #e5e7eb;
            }}
            .footer p {{
                margin: 5px 0;
                color: #6b7280;
                font-size: 14px;
            }}
            .divider {{
                height: 1px;
                background-color: #e5e7eb;
                margin: 30px 0;
            }}
            @media only screen and (max-width: 600px) {{
                .container {{
                    margin: 20px;
                    border-radius: 8px;
                }}
                .header {{
                    padding: 30px 20px;
                }}
                .content {{
                    padding: 30px 20px;
                }}
                .stats-grid {{
                    grid-template-columns: 1fr;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="header-icon">⚠️</div>
                <h1>Budget Warning</h1>
            </div>
            
            <div class="content">
                <div class="warning-box">
                    <p>You've used <strong>{percentage:.0f}%</strong> of your <strong>{category_name}</strong> budget</p>
                </div>
                
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-label">Budget Amount</div>
                        <div class="stat-value">₹{budget_amount:,.2f}</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">Spent So Far</div>
                        <div class="stat-value warning">₹{spent_amount:,.2f}</div>
                    </div>
                </div>
                
                <div class="stat-card" style="margin-top: 20px;">
                    <div class="stat-label">Remaining Budget</div>
                    <div class="stat-value remaining">₹{remaining:,.2f}</div>
                </div>
                
                <div class="progress-bar">
                    <div class="progress-fill"></div>
                </div>
                <div class="progress-label">
                    <strong>{percentage:.0f}%</strong> of budget used • <strong>₹{remaining:,.2f}</strong> remaining
                </div>
                
                <div class="tips-box">
                    <h3>💡 Tips to Stay Within Budget</h3>
                    <ul>
                        <li>Review your recent {category_name} expenses</li>
                        <li>Look for non-essential items you can postpone</li>
                        <li>Consider alternatives to reduce costs</li>
                        <li>Set up daily spending limits for this category</li>
                    </ul>
                </div>
                
                <div class="divider"></div>
                
                <p style="color: #6b7280; font-size: 15px; line-height: 1.6;">
                    You're doing great tracking your finances! This is just a friendly reminder that you're approaching 
                    your budget limit for <strong>{category_name}</strong>. Small adjustments now can help you stay on track.
                </p>
                
                <center>
                    <a href="#" class="cta-button">Review Expenses</a>
                </center>
            </div>
            
            <div class="footer">
                <p><strong>Money Manager</strong></p>
                <p>Helping you stay on top of your finances</p>
                <p style="font-size: 12px; color: #9ca3af; margin-top: 15px;">
                    You're receiving this because you set up budget alerts for your account.
                </p>
            </div>
        </div>
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
        print(f"✅ Budget warning email sent successfully to {to_email}")
        return True
    except Exception as e:
        print(f"❌ Failed to send warning email: {str(e)}")
        return False

def send_welcome_email(to_email: str, username: str):
    """Send welcome email when user registers"""
    subject = "🎉 Welcome to Money Manager!"
    
    body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                margin: 0;
                padding: 0;
                background-color: #f4f4f7;
            }}
            .container {{
                max-width: 600px;
                margin: 40px auto;
                background-color: #ffffff;
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }}
            .header {{
                background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
                color: white;
                padding: 40px 30px;
                text-align: center;
            }}
            .header-icon {{
                font-size: 48px;
                margin-bottom: 10px;
            }}
            .header h1 {{
                margin: 0;
                font-size: 28px;
                font-weight: 600;
            }}
            .content {{
                padding: 40px 30px;
            }}
            .welcome-text {{
                font-size: 18px;
                color: #1f2937;
                margin-bottom: 20px;
            }}
            .feature-grid {{
                display: grid;
                gap: 20px;
                margin: 30px 0;
            }}
            .feature-card {{
                background-color: #f9fafb;
                padding: 20px;
                border-radius: 8px;
                border-left: 4px solid #3b82f6;
            }}
            .feature-card h3 {{
                margin: 0 0 10px 0;
                color: #1f2937;
                font-size: 16px;
            }}
            .feature-card p {{
                margin: 0;
                color: #6b7280;
                font-size: 14px;
            }}
            .cta-button {{
                display: inline-block;
                background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
                color: white;
                padding: 14px 32px;
                text-decoration: none;
                border-radius: 8px;
                font-weight: 600;
                text-align: center;
                margin: 20px 0;
                box-shadow: 0 4px 6px rgba(59, 130, 246, 0.2);
            }}
            .footer {{
                background-color: #f9fafb;
                padding: 30px;
                text-align: center;
                border-top: 1px solid #e5e7eb;
            }}
            .footer p {{
                margin: 5px 0;
                color: #6b7280;
                font-size: 14px;
            }}
            @media only screen and (max-width: 600px) {{
                .container {{
                    margin: 20px;
                }}
                .header, .content {{
                    padding: 30px 20px;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="header-icon">🎉</div>
                <h1>Welcome to Money Manager!</h1>
            </div>
            
            <div class="content">
                <p class="welcome-text">
                    Hi <strong>{username}</strong>,
                </p>
                <p class="welcome-text">
                    Welcome aboard! We're excited to help you take control of your finances and achieve your financial goals.
                </p>
                
                <div class="feature-grid">
                    <div class="feature-card">
                        <h3>📊 Track Your Expenses</h3>
                        <p>Easily categorize and monitor all your spending in one place</p>
                    </div>
                    <div class="feature-card">
                        <h3>💰 Set Budgets</h3>
                        <p>Create budgets for different categories and stay within your limits</p>
                    </div>
                    <div class="feature-card">
                        <h3>📧 Smart Alerts</h3>
                        <p>Get notified when you're approaching or exceeding your budgets</p>
                    </div>
                    <div class="feature-card">
                        <h3>📈 Monthly Reports</h3>
                        <p>View detailed reports to understand your spending patterns</p>
                    </div>
                </div>
                
                <center>
                    <a href="#" class="cta-button">Get Started</a>
                </center>
                
                <p style="color: #6b7280; font-size: 14px; margin-top: 30px; text-align: center;">
                    Need help getting started? Check out our quick start guide or reach out to our support team.
                </p>
            </div>
            
            <div class="footer">
                <p><strong>Money Manager</strong></p>
                <p>Your partner in financial wellness</p>
            </div>
        </div>
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
        print(f"✅ Welcome email sent successfully to {to_email}")
        return True
    except Exception as e:
        print(f"❌ Failed to send welcome email: {str(e)}")
        return False
