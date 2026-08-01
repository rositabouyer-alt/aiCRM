import xlsxwriter
import io
from sqlalchemy.orm import Session
from app import models

def export_leads_excel(db: Session):
    leads = db.query(models.Lead).all()
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet('Leads')
    
    headers = ['ID', 'Name', 'Phone', 'Email', 'Telegram', 'WhatsApp', 'Status', 'Score', 'Created']
    for col, header in enumerate(headers):
        worksheet.write(0, col, header)
    
    for row, lead in enumerate(leads, 1):
        worksheet.write(row, 0, lead.id)
        worksheet.write(row, 1, lead.full_name)
        worksheet.write(row, 2, lead.phone)
        worksheet.write(row, 3, lead.email or "")
        worksheet.write(row, 4, lead.telegram_username or "")
        worksheet.write(row, 5, lead.whatsapp or "")
        worksheet.write(row, 6, lead.status)
        worksheet.write(row, 7, lead.lead_score)
        worksheet.write(row, 8, str(lead.created_at))
    
    workbook.close()
    output.seek(0)
    return output.getvalue()
