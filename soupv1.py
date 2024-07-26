import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
import os

def yeah(lower,upper):
    main_row=[['Heading','Weakness ID','Vulnerability Mapping','Abstraction','Description','Extended Description','Alternate Terms',
               'Potential Mitigation','Modes of Introduction','Platform Language','Platform Technology','Likelihood of Exploit',
               'Observed Examples','Detection Method']]
    for i in range(lower,upper):
        temp_row=[]
        page = requests.get(f'https://cwe.mitre.org/data/definitions/{i}')
        soup = BeautifulSoup(page.content, "html.parser")
        target_style='display:inline; margin:0px 0px 2px 0px; vertical-align: text-bottom'
        element = soup.find("h2", {"style": target_style})
        temp_row.append(element.text)                                     #title print
        stuffs = soup.find_all("div", class_="title")

        if stuffs:
            for stuff in stuffs:
                weakness=stuff.find("div", style="font-weight:bold", string=lambda t: t and "Weakness ID:" in t)
                if weakness:
                    temp_row.append(weakness.text.split("Weakness ID:")[-1].strip())
                else:
                    temp_row.append('Weakness id not found')                                #weakness print
                vulnmap= soup.find_all('span',class_='tool')
                if vulnmap: 
                    for vuln in vulnmap[:2]:
                        if vuln:
                            first_child_span = vuln.find('span')
                            temp_row.append(first_child_span.text) 
                        else:
                            temp_row.append('Not found')    
                else:
                     temp_row.append('Not found')  
                     temp_row.append('Not found') 
        Description=soup.find('div',id='Description')  
        if Description:
            indent_div=Description.find('div',class_='indent')
            temp_row.append(indent_div.text) 
        else:
            temp_row.append('description not found')                                           #desc print
        ext_desc=soup.find('div',id='Extended_Description')  
        if ext_desc:
            indent_div1=ext_desc.find('div',class_='indent')
            temp_row.append(indent_div1.text) 
        else:
            temp_row.append('extended description not found') 
        alt_terms=soup.find('div',id='Alternate_Terms') 
        temp_alt=[]
        if alt_terms:
            tr_element = alt_terms.find_all('tr')
            for i in tr_element:
                th=i.find('th')
                temp_alt.append(th.text)
            tempaltstring="\n".join(temp_alt)    
            temp_row.append(tempaltstring)        
        else:
            temp_row.append('alternate terms not found')  

        mitigations=soup.find('div',id='Potential_Mitigations') 
        temp_mit=[]
        if mitigations:
            tr_element = mitigations.find_all('tr')
            for i in tr_element:
                p=i.find('p')
                if p:
                    temp_mit.append(p.text)         
            mitasstring="\n".join(temp_mit)    
            temp_row.append(mitasstring)    
        else:
            temp_row.append('mitigation terms not found')  

        intro=soup.find('div',id='Modes_Of_Introduction')
        if intro:
            temp_intro=[]
            div2=intro.find('div',class_='expandblock')
            div3=div2.find('div',class_='tabledetail')
            indent=div3.find('div',class_='indent')
            table=indent.find('table',id='Detail')
            th_elements = []
            for tr in table:
                for th in tr:           
                    th_elements.append(th.string)
            lastfour=th_elements[2::2] 
            for a in lastfour:
                if a:
                    temp_intro.append(a) 
            introstring="\n".join(temp_intro)          
            temp_row.append(introstring)          
        else:temp_row.append('Modes of introduction not found')
        langtech=soup.find('div',id='Applicable_Platforms')                         #platform lang,tech
        if langtech:
            temp_lang=[]
            temp_tech=[]
            expandblock=langtech.find('div',class_='expandblock')
            if expandblock:    
             detail=expandblock.find('div',class_='detail')
             if detail:    
                ind=detail.find('div',class_='indent')
                if ind: 
                    foundlang=False
                    foundtech=False   
                    subheadings = ind.find_all('p', class_='subheading')
                    if subheadings:
                        for subheading in subheadings:
                            if subheading.text == 'Languages':
                                foundlang=True
                                next_sibling = subheading.find_next_sibling()
                                while next_sibling and next_sibling.name == 'div' and 'indent' in next_sibling.get('class', []):
                                    temp_lang.append(next_sibling.text)
                                    next_sibling = next_sibling.find_next_sibling()
                                langstring="\n".join(temp_lang)          
                                temp_row.append(langstring)    
                            elif subheading.text == 'Technologies':
                                foundtech=True
                                next_sibling = subheading.find_next_sibling()
                                while next_sibling and next_sibling.name == 'div' and 'indent' in next_sibling.get('class', []):
                                    temp_tech.append(next_sibling.text)
                                    next_sibling = next_sibling.find_next_sibling() 
                                techstring="\n".join(temp_tech)          
                                temp_row.append(techstring)
                        if not foundlang:temp_row.append('Not found') 
                        if not foundtech:temp_row.append('Not found')
                    else:
                          temp_row.append('Not found') 
                          temp_row.append('Not found')                  
            else:
                temp_row.append('Not found') 
                temp_row.append('Not found')
        else:
            temp_row.append('Not found')
            temp_row.append('Not found')
        likelihood=soup.find('div',id='Likelihood_Of_Exploit')                         
        if likelihood:
            expandblock2=likelihood.find('div',class_='expandblock')
            if expandblock2:
                detail_div=expandblock2.find('div',class_='detail')  
                if detail_div:
                    whatwewant=detail_div.find('div')
                    if whatwewant:
                        temp_row.append(whatwewant.text)                                       
        else:temp_row.append('Likelihood of exploit not found')
        obeservedex=soup.find('div',id='Observed_Examples')                      
        if obeservedex: 
            temp_ex=[] 
            expandblock3=obeservedex.find('div',class_='expandblock')
            if expandblock3:   
                tabledetail=expandblock3.find('div',class_='tabledetail')  
                if tabledetail:
                    indent_div2=tabledetail.find('div',class_='indent')
                    if indent_div2:
                        div4=indent_div2.find('div')
                        table2=div4.find('table')
                        tr1=table2.find_all('tr')
                        for a in tr1:
                            td1=a.find('td')
                            if td1:
                                div5=td1.find('div')
                                temp_ex.append(div5.text)
            exstring="\n".join(temp_ex)                    
            temp_row.append(exstring)                    
        else:temp_row.append('Observed Examples not found')                           

        detectionmethod=soup.find('div',id='Detection_Methods')                      
        if detectionmethod:  
            temp_meth=[]
            expandblock4=detectionmethod.find('div',class_='expandblock')
            if expandblock4:   
                div6=expandblock4.find('div',class_='detail')
                if div6:
                    indent_div3=div6.find('div',class_='indent')
                    if indent_div3:
                        grouped=indent_div3.find('div',id='Grouped')
                        if grouped:
                            tabledetail2=grouped.find('table')
                            for tr6 in tabledetail2.find_all('tr'):             #??????????????
                                td2=tr6.find('td')
                                if td2:
                                    p2=td2.find('p',class_='subheading')
                                    temp_meth.append(p2.text)
            methstring="\n".join(temp_meth)                        
            temp_row.append(methstring)                        
        else:temp_row.append('Detection Methods not found')

        main_row.append(temp_row)
    return main_row



def save_to_excel(rows,output):
    workbook=Workbook()
    sheet=workbook.active
    sheet.title='Empty Cells'
    for row in rows:
        sheet.append(row)
    workbook.save(output)  
    print(f'Data saved to {output}')
   
    
save_to_excel(yeah(1,1427),os.path.join('E:\\pythonvenv\\venv\\data mine', "mined_stuff.xlsx"))    