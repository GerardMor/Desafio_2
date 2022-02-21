from cgitb import text
from email.mime import base
import imaplib
import email
from turtle import color
import pymysql
from tkinter import *
from cv2 import GeneralizedHoughBallard
from tkinter import filedialog as fd
from tkinter import scrolledtext as st
#from tkinter import ttk
#from tkinter import messagebox as mb


def ventana_inicial():
    global principal
    color ="DarkGrey"
    principal = Tk()
    principal.geometry("700x400")
    principal.title("Correos Gmail")
    Label(text="Correos Gmail", bg="Yellow", width="300", height="6", font=("Arial", 13)).pack()
    Label(text="").pack()
    Button(text="Obtener mail", height="2", width="30", bg=color, command=get_emailinfo).pack() #BOTÓN para obtener los mails
    Label(text="").pack()
    Button(text="Crear Base de datos", height="2", width="30", bg=color, command=crear_db).pack() #BOTÓN para obtener los mails
    Label(text="").pack()
    Label(text="Bienvenidos al ADN MELI", bg="Blue", width="300", height="6", font=("Arial black", 13)).pack()
    
    

    principal.mainloop()

def crear_db():
    iConexion = pymysql.connect( host='localhost', user= 'root', passwd='', db='Desafio2' )
    cur = iConexion.cursor()
    cur.execute('''CREATE TABLE IF NOT EXIST correos (fecha DATE NTO NULL, origen VARCHAR(255) NOT NULL, tema VARCHAR(500) NOT NULL)''')
    cur.execute('''INSERT INTO correos VALUES('','','')''')
    iConexion.close()


def get_body(tmsg):    
    body = ""
    if tmsg.is_multipart():        
        for part in tmsg.walk():
            ctype = part.get_content_type()
            cdispo = str(part.get('Content-Disposition'))    
            # skip any text/plain (txt) attachments
            if ctype == 'text/plain' and 'attachment' not in cdispo:
                body = str(part.get_payload(decode=True))  # decode
                body=body.replace("\\r\\n","\n")                
                break
    # not multipart - i.e. plain text, no attachments, keeping fingers crossed
    else:
        body = str(tmsg.get_payload(decode=True))
    return body

def get_emailinfo(id, data, bshowbody=False):

    for contenido in data:
        # comprueba que 'contenido' sea una tupla, si es así continua
        if isinstance(contenido, tuple):                    
            # recuperamos información del email:                    
            msg = email.message_from_string(contenido[1].decode())
            # mostramos resultados:
            print ("%d - *** %s ***" % (id, msg['subject'].upper()))
            print ("enviado por %s" % msg['from'])
            print ("para %s" % msg['to'])
            if(bshowbody):
                print(text="---                                                   ---")
                print(get_body(msg))
                print (text="=========================================================")
            return True
            
    # si no hay info
    return False

def get_emails(gmailsmtpsvr, gmailusr, gmailpwd, bshowbody):
    try:
        # Conectamos a nuestro servidor, gmail necesita un ssl socket (encriptado) por lo que utilizamos 
        # la subclase IMAP4_SSL
        # Parámetros: host='', port=IMAP4_SSL_PORT, keyfile=None, certfile=None, ssl_context=None
        # El puerto por defecto IMAP4_SSL_PORT es el 993, en el caso de gmail lo dejamos como está, el resto de 
        # parámetros tampoco son necesarios en este caso.
        # Únicamente es necesario pasar como parámetro el servidor stmp de gmail 
        mail = imaplib.IMAP4_SSL(gmailsmtpsvr)
        # logamos:
        mail.login(gmailusr, gmailpwd)
        # seleccionamos bandeja de entrada 'inbox'
        mail.select("inbox")
        # recuperamos lista de emails, es posible filtrar la consulta
        # ALL devuelve todos los emails
        # Ejemplo de filtro: '(FROM "altaruru" SUBJECT "ejemplo python")'        
        result, data = mail.search(None, 'SUBJECT DevOps')
        strids = data[0] # coge lista de ids encontrados
        lstids = strids.split()
        # recuperamos valores para bucle
        firstid = int(lstids[0])
        lastid = int(lstids[-1])
        countid = 0
        # mostramos datos de los ids encontrados
        print("primer id: %d\nultimo id: %d\n..." % (firstid, lastid))
        # recorremos lista de mayor a menor (mas recientes primero)
        for id in range(lastid, firstid-1, -1):            
            typ, data = mail.fetch(str(id), '(RFC822)' ) # el parámetro id esperado es tipo cadena
            if (get_emailinfo(id, data, bshowbody)):
                countid+=1
        # fin, si llegamos aqui todo es correcto
        print("emails listados %d" % countid)
    except Exception as e:
        print("Error: %s" % (e))
        return ""
    except:
        print("Error desconocido")
        return ""


#----------------------------
def test(): 
    get_emails("smtp.gmail.com", "gerardbrowncorp@gmail.com", "water1996", True)
test()

ventana_inicial() 


























