from pathlib import Path
import json
base=Path(r'D:\RAD\FINAL');repo=base/'SaigonBite';values=json.loads((base/'Part2/content/links.json').read_text(encoding='utf-8'));mapping={'Repo':('github_repo','Repository'),'Release':('github_release_url','Release'),'Figma':('figma_prototype','Figma prototype'),'FigmaFile':('figma_file','Figma design'),'Deployed':('deployed_url','Deployed demonstration'),'DeployedFallback':('deployed_url_fallback','Fallback deployment'),'Video':('demo_video','Demonstration video'),'Drive':('drive_folder','Drive folder')};out=['% Generated only from Part2/content/links.json; PENDING remains visible.', r'\begingroup', r'\catcode`\%=12']
for macro,(key,label) in mapping.items():
 v=values[key]
 if v.startswith('PENDING'):
  out.append('\\gdef\\Link'+macro+'{\\textcolor{red}{\\textbf{PENDING: '+key.replace('_','\\_')+'}}}')
 else:
  out.append('\\gdef\\Target'+macro+'{\\detokenize{'+v+'}}');out.append('\\gdef\\Link'+macro+'{\\href{\\Target'+macro+'}{'+label+'}}')
out.append(r'\endgroup')
(repo/'docs/part2/latex/links.tex').write_text('\n'.join(out)+'\n',encoding='utf-8');print('links.tex generated; pending',','.join(k for k,_ in mapping.values() if values[k].startswith('PENDING')))
