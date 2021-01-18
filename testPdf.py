from bidi import algorithm as bidialg
from xhtml2pdf import pisa

HTMLINPUT = """
            <!DOCTYPE html>
            <html>
            <head>
               <meta http-equiv="content-type" content="text/html; charset=utf-8">
               <style>
                  @page {
                      size: a4;
                      margin: 1cm;
                  }

                  @font-face {
                      font-family: DejaVu;
                      src: url(fonts/gishabd.ttf);
                  }

                  html {
                      font-family: DejaVu;
                      font-size: 11pt;
                  }
               </style>
            </head>
            <body>
               <div>Something in English - משהו בעברית</div>
               <h1>HTML To PDF</h1>
    <h3><a href="{% url 'test' %}">שלום</a></h3>
     <b>אני מנסה פה משהו


         אחר
</b>
            </body>
            </html>
            """
with open("test.html", "r") as f:
    html = f.read()
f = open('mypdf.pdf', 'wb')
# pisa.pisaDocument(cStringIO.StringIO(a).encode('utf-8'),f)
pisa.pisaDocument(bidialg.get_display(html, base_dir="L"), f)
f.close()
# pdf = pisa.CreatePDF(bidialg.get_display(HTMLINPUT, base_dir="L"), "outpufile.pdf")
