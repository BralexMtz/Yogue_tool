from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
def webScrapBBVA(my_url):

    uClient = uReq(my_url)
    page_html= uClient.read()
    uClient.close()
    page_soup = soup(page_html,"html.parser")
    title=page_soup.select("h1.headermarquee__title, h1.producttitlesubtitlemarquee__title ")
    title=title[0].text

    textos=page_soup.findAll("div",{"itemprop":"text"})

    final_text=[]
    for item in textos:
        hijos=list(item.children)
        if len(hijos) > 0:
            for child in hijos:
                if "h" in str(child.name):
                    text=" "
                    text="<"+str(child.name)+">"+str(child.string)+"</"+str(child.name)+">"
                    final_text.append(text)
                if "None" not in str(child.name):
                    final_text.append(child.get_text())
                    
    
    # for item in textos:
    #     final_text.append(item.get_text())

    #for al in final_text:
    #    print(al)
    return title,final_text
#title,content=webScrapBBVA("https://www.bbva.mx/educacion-financiera/ahorro/como-hacer-rendir-el-dinero.html")
#print(content[0])