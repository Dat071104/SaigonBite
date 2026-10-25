"""Internal A4 two-page proof for the shared design brief (not a deliverable)."""
from pathlib import Path
from html import escape
import re
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader
import pypdfium2 as pdfium

ROOT=Path(r'D:\RAD\FINAL'); DOC=ROOT/'SaigonBite/docs/part2'
OUT=ROOT/'Part2/notes/P3-root'; OUT.mkdir(parents=True,exist_ok=True)
pdfmetrics.registerFont(TTFont('Arial',r'C:\Windows\Fonts\arial.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Bold',r'C:\Windows\Fonts\arialbd.ttf'))
styles=getSampleStyleSheet()
body=ParagraphStyle('brief',fontName='Arial',fontSize=9.5,leading=11.5,spaceAfter=4)
head=ParagraphStyle('head',parent=body,fontName='Arial-Bold',fontSize=10.5,spaceBefore=5,spaceAfter=4)
story=[]
for line in (DOC/'_agent_reports/P3-brief.md').read_text(encoding='utf-8').splitlines():
    if not line.strip() or re.match(r'^\|[-| ]+\|$',line): continue
    value=re.sub(r'`([^`]+)`',r'\1',line).strip('| ')
    value=re.sub(r'\*\*([^*]+)\*\*',r'\1',value)
    style=head if value.startswith('#') else body
    story.append(Paragraph(escape(value.lstrip('# ')),style))
target=OUT/'P3_brief_A4.pdf'
SimpleDocTemplate(str(target),pagesize=A4,leftMargin=42,rightMargin=42,topMargin=36,bottomMargin=36).build(story)
count=len(PdfReader(target).pages)
assert count<=2, f'Shared brief exceeds 2 pages: {count}'
pdf=pdfium.PdfDocument(str(target))
for i,p in enumerate(pdf): p.render(scale=1.3).to_pil().save(OUT/f'P3_brief_A4_{i+1}.png')
print('Shared brief:',count,'A4 pages, 9.5 pt body; proof in',OUT)
