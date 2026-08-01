from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
import io
import xlsxwriter

router = APIRouter(prefix="/export", tags=["export"])

@router.get("/excel/leads")
def export_leads_excel(db: Session = Depends(get_db)):
    leads = db.query(models.Lead).all()
    
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet('Leads')
    
    # Headers
    headers = ['ID', 'Name', 'Phone', 'Platform', 'Status', 'Budget', 'Created']
    for col, header in enumerate(headers):
        worksheet.write(0, col, header)
    
    # Data
    for row, lead in enumerate(leads, 1):
        worksheet.write(row, 0, lead.id)
        worksheet.write(row, 1, lead.full_name)
        worksheet.write(row, 2, lead.phone)
        worksheet.write(row, 3, str(lead.platform))
        worksheet.write(row, 4, str(lead.status))
        worksheet.write(row, 5, lead.budget or 0)
        worksheet.write(row, 6, str(lead.created_at))
    
    workbook.close()
    output.seek(0)
    
    return output.getvalue()

@router.get("/excel/conversations")
def export_conversations_excel(db: Session = Depends(get_db)):
    convs = db.query(models.Conversation).all()
    
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet('Conversations')
    
    # Headers
    headers = ['ID', 'Lead Name', 'Platform', 'Messages', 'Created']
    for col, header in enumerate(headers):
        worksheet.write(0, col, header)
    
    # Data
    for row, conv in enumerate(convs, 1):
        worksheet.write(row, 0, conv.id)
        worksheet.write(row, 1, conv.lead.full_name if conv.lead else "Unknown")
        worksheet.write(row, 2, str(conv.platform))
        worksheet.write(row, 3, len(conv.messages))
        worksheet.write(row, 4, str(conv.created_at))
    
    workbook.close()
    output.seek(0)
    
    return output.getvalue()
