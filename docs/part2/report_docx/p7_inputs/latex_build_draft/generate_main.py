from pathlib import Path
from docx import Document
import json,re
b=Path(r'D:\RAD\FINAL');repo=b/'SaigonBite';out=repo/'docs/part2/latex';receipt=json.loads((b/'Part2/notes/P7/latex_draft_receipt.json').read_text(encoding='utf-8'));D=Document(b/'RAD_Sem01_2627_Report_Template.docx');members=json.loads((b/'Part2/content/links.json').read_text(encoding='utf-8'))['members']
def esc(s):
 repl={'\\':r'\textbackslash{}','{':r'\{','}':r'\}','_':r'\_','%':r'\%','&':r'\&','#':r'\#','$':r'\$','~':r'\textasciitilde{}','^':r'\textasciicircum{}','—':'---','–':'--','’':"'",'“':'``','”':"''",'·':r'\ensuremath{\cdot}','§':r'\S{}'}
 return ''.join(repl.get(c,c) for c in s)
preamble=r'''\documentclass[11pt,a4paper]{article}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{lmodern}
\usepackage[margin=20mm]{geometry}
\usepackage{graphicx,longtable,booktabs,array,tabularx}
\usepackage{pdflscape,caption,xcolor,enumitem,listings,microtype}
\usepackage[hidelinks]{hyperref}
\usepackage{bookmark}
\graphicspath{{../../../}{./}}
\setlength{\LTleft}{0pt}
\setlength{\LTright}{0pt}
\lstset{basicstyle=\ttfamily\small,breaklines=true,columns=fullflexible,keepspaces=true}
\input{links}
''';(out/'preamble.tex').write_text(preamble,encoding='utf-8')
front=[r'\input{preamble}',r'\begin{document}',r'\begin{titlepage}',r'\centering',r'{\LARGE SaigonBite: Online Food Delivery Hub Platform\par}',r'\vspace{8mm}',r'{\large Requirements Analysis \& Design (RAD) -- Sem01\_2627\par}',r'\vspace{10mm}',r'By Students:\par']
for m in members:front.append(esc(m['id']+' : '+m['name'])+r'\par')
front += [r'\vfill',r'\begin{tabularx}{\linewidth}{|X|X|X|X|}\hline',r'Reference & Audience & Document version & Outcome \\ \hline',r'Team02\_BRS\_SRS\_for\_SaigonBite & Mr. Pham Thai Ky Trung & 28/10/2026 & SaigonBite \\ \hline',r'\end{tabularx}',r'\vspace{8mm}',r'\begin{tabularx}{\linewidth}{|X|}\hline',r'\textbf{Abstract} \\ \hline',r'SaigonBite connects customer ordering, kitchen decisions, delivery and operational reporting. This report records the requirements, design, implementation and evidence for the Part 2 demonstration. The online payment option is simulated and refund obligations are recorded without a payout. Recorded test and deployment results are scoped to the documented runs. \\ \hline',r'\end{tabularx}',r'\end{titlepage}',r'\section*{Intellectual Property}',r'\addcontentsline{toc}{section}{Intellectual Property}',r'\pdfbookmark[0]{Intellectual Property}{p7ip}']
for p in D.paragraphs[21:28]:
 if p.text.strip():front.append(esc(p.text.strip().replace('[year]','2026').replace('Team XX','Team 02'))+'\n')
front += [r'\section*{Table of Contents}',r'\pdfbookmark[0]{Table of Contents}{p7toc}',r'\makeatletter\@starttoc{toc}\makeatother',r'\clearpage']
for x in receipt['sections']:front.append(r'\input{'+x['file'].replace('\\','/')[:-4]+'}')
front.append(r'\end{document}');(out/'main.tex').write_text('\n'.join(front)+'\n',encoding='utf-8')
for name,num in [('contribution_statement',143),('ai_usage_log',144)]:
 (out/(name+'.tex')).write_text('\\input{preamble}\n\\begin{document}\n\\input{sections/section_'+str(num)+'}\n\\end{document}\n',encoding='utf-8')
print('main, preamble and two standalone source documents created; no compilation')
