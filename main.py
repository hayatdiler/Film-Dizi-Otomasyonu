from tkinter import *
from tkinter import ttk, messagebox, filedialog
import json

from tkinter import Tk, Frame, Listbox, Label, Entry, Button, Scrollbar, RIGHT, LEFT, Y, BOTH, END
from tkinter import ttk
from PIL import Image, ImageTk # type: ignore


class MediaPlayer():
    def __init__(self):

        # Ana pencere
        self.root = Tk()
        self.root.title("Marun Watch List")
        self.root.geometry("800x720+320+150")  # Daha kare pencere
        self.root.configure(bg="#121212")  # Koyu arka plan

        # ttk teması (dark mode renkleri - koyu mavi tonlar)
        style = ttk.Style(self.root)
        style.theme_use('clam')
        style.configure('TButton', font=('Arial', 12), padding=6, background='#0d0d5e', foreground='white')
        style.map('TButton', background=[('active', '#070738')])
        style.configure('TEntry', font=('Arial', 12), padding=4, fieldbackground='#1e1e1e', foreground='white')
        style.configure('TLabel', font=('Arial', 12), background='#121212', foreground='gray')
        style.configure('TFrame', background='#121212')

        # Sol üst köşeye logo ve yeni isim
        top_frame = Frame(self.root, bg="#121212")
        top_frame.place(x=10, y=10)
        try:
            img = Image.open("logo.png")
            img = img.resize((80, 50))  # Daha dikdörtgen boyut
            self.logo_img = ImageTk.PhotoImage(img)
            logo_label = Label(top_frame, image=self.logo_img, bg="#121212")
            logo_label.pack(side=LEFT, padx=(0,5))
        except Exception as e:
            print("Logo yüklenemedi:", e)
        site_adi = Label(top_frame, text="MarunWatchList", font=('Arial', 14, 'bold'), fg="gray", bg="#121212")
        site_adi.pack(side=LEFT)

        # Sol çerçeve
        self.frameSol = ttk.Frame(self.root)
        self.frameSol.pack(side=LEFT, fill=BOTH, expand=False, padx=10, pady=60)

        # Arama bölümü
        arama_frame = ttk.Frame(self.frameSol)
        arama_frame.pack(fill='x', pady=(0,10))
        self.aramaCubugu = ttk.Entry(arama_frame)
        self.aramaCubugu.pack(side=LEFT, fill='x', expand=True)
        self.araButon = ttk.Button(arama_frame, text="Ara", command=self.ara)
        self.araButon.pack(side=LEFT, padx=(5,0))
        self.filtreButon = ttk.Button(arama_frame, text="Filtrele", command=self.filtrele)
        self.filtreButon.pack(side=LEFT, padx=(5,0))

        # Liste ve kaydırma çubuğu
        liste_frame = ttk.Frame(self.frameSol)
        liste_frame.pack(fill=BOTH, expand=True)
        scrollbar = Scrollbar(liste_frame)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.liste = Listbox(liste_frame, font=('Arial', 12), yscrollcommand=scrollbar.set, bd=1, highlightthickness=0, 
                             bg="#1e1e1e", fg="white", selectbackground="#0d0d5e", selectforeground="white")
        self.liste.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.config(command=self.liste.yview)
        self.liste.bind("<ButtonRelease-1>", self.bilgi_goster)
        
        # Alt düğmeler
        buton_frame = ttk.Frame(self.frameSol)
        buton_frame.pack(fill='x', pady=(10,0))
        self.ekleButon = ttk.Button(buton_frame, text="Ekle", command=self.ekle)
        self.ekleButon.pack(fill='x', pady=2)
        self.silButon = ttk.Button(buton_frame, text="Sil", command=self.sil)
        self.silButon.pack(fill='x', pady=2)
        self.duzenleButon = ttk.Button(buton_frame, text="Düzenle", command=self.duzenle)
        self.duzenleButon.pack(fill='x', pady=2)

        # Sağda video alanı
        self.video_frame = ttk.Frame(self.root, width=340, height=500, relief='sunken')
        self.video_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=(0,10), pady=60)
        self.video_frame.pack_propagate(False)

        # Video bilgilerini göstermek için mevcut bilgilerLabel etiketi burada tanımlanmalı
        self.bilgilerLabel = ttk.Label(self.video_frame, anchor='nw', justify='left', width=36,
                                background='#1e1e1e', foreground='white', font=("Arial", 11))
        self.bilgilerLabel.pack(fill='both', expand=True, padx=10, pady=10)
        

        # Liste güncellemesi
        self.guncelle()
        self.root.mainloop()


    def bilgi_goster(self, event):
        veriler=self.loadfromJSON()
        secili_indeks=self.liste.curselection()[0]

        for index, i in enumerate(veriler):
            if i["ad"]==self.liste.get(secili_indeks):
                self.bilgilerLabel.config(text=f"Ad: {i['ad']}\nTür: {i['tur']}\nDurum: {i['durum']}\nYıldız: {i['yildiz']}\nNot: {i['not']}")

    def filtrele(self):
        self.filtrele_root=Toplevel()
        self.filtrele_root.geometry("590x280+710+300")

        spinbox_var=StringVar()
        spinbox_var.set("")
        
        self.filtreleAdEntry=Entry(self.filtrele_root)
        self.filtreleTurCombobox=ttk.Combobox(self.filtrele_root, values=["Dizi", "Film"])
        self.filtreleDurumCombobox=ttk.Combobox(self.filtrele_root, values=["İzlendi", "İzleniyor", "İzlenecek"])
        self.filtreleYildizSpinbox=Spinbox(self.filtrele_root, from_=1, to=5, textvariable=spinbox_var)
        self.filtreleYildizSpinbox.delete(0, "end")
        self.filtreleNotEntry=Entry(self.filtrele_root)

        adLabel=Label(self.filtrele_root, text="Ad:", font=("Airal", 20), width=20)
        turLabel=Label(self.filtrele_root, text="Tür:", font=("Airal", 20), width=20)
        durumLabel=Label(self.filtrele_root, text="Durum:", font=("Airal", 20), width=20)
        yildizLabel=Label(self.filtrele_root, text="Yıldız:", font=("Airal", 20), width=20)
        notLabel=Label(self.filtrele_root, text="Not:", font=("Airal", 20), width=20)

        filtreleButon=Button(self.filtrele_root, text="Filtrele", command=self.filtrele_islemi)
        

        adLabel.grid(row=0, column=0)
        self.filtreleAdEntry.grid(row=0, column=1)
        
        turLabel.grid(row=1, column=0)
        self.filtreleTurCombobox.grid(row=1, column=1)

        durumLabel.grid(row=2, column=0)
        self.filtreleDurumCombobox.grid(row=2, column=1)

        yildizLabel.grid(row=3, column=0)
        self.filtreleYildizSpinbox.grid(row=3, column=1)

        notLabel.grid(row=4, column=0)
        self.filtreleNotEntry.grid(row=4, column=1)

        filtreleButon.grid(row=5, column=0, sticky="e")
        

    def filtrele_islemi(self):
        
        ad=self.filtreleAdEntry.get() if self.filtreleAdEntry.get()!="" else None
        tur=self.filtreleTurCombobox.get() if self.filtreleTurCombobox.get()!="" else None
        durum=self.filtreleDurumCombobox.get() if self.filtreleDurumCombobox.get()!="" else None
        yildiz=self.filtreleYildizSpinbox.get() if self.filtreleYildizSpinbox.get()!="" else None
        note=self.filtreleNotEntry.get() if self.filtreleNotEntry.get()!="" else None

        veriler=self.loadfromJSON()
        liste=list()
        
        

        for i in veriler:
            if ((ad==None or ad in i["ad"]) and 
                (tur==None or i["tur"]==tur) and 
                (durum==None or i["durum"]==durum) and 
                (yildiz==None or i["yildiz"]==yildiz) and 
                (note==None or i["not"]==note)):

                liste.append(i)

        self.liste.delete(0, END)

        if liste:
            for i in liste:
                self.liste.insert(END, i["ad"])
        
        self.filtrele_root.destroy()

    def ara(self):
        if self.aramaCubugu.get()!="":
            ad=self.aramaCubugu.get()
            veriler=self.loadfromJSON()
            videolar=list()
            for i in veriler:
                if ad in i["ad"]:
                    videolar.append(i)
                    
            self.liste.delete(0, END)
            for i in videolar:
                self.liste.insert(END, i["ad"])  
                      

        else:
            self.guncelle()

    def duzenle(self):
        secili_indeks=self.liste.curselection()
        if secili_indeks:
            self.duzenle_popup()

    def duzenle_popup(self):
        self.duzenlePopup_root=Toplevel()
        self.duzenlePopup_root.geometry("500x250+710+300")

        spinbox_var=StringVar()
        spinbox_var.set("")

        self.duzenleAdEntry=Entry(self.duzenlePopup_root)
        self.duzenleTurCombobox=ttk.Combobox(self.duzenlePopup_root, values=["Dizi", "Film"])
        self.duzenleDurumCombobox=ttk.Combobox(self.duzenlePopup_root, values=["İzlendi", "İzleniyor", "İzlenecek"])
        self.duzenleYildizSpinbox=Spinbox(self.duzenlePopup_root, from_=1, to=5)
        self.duzenleYildizSpinbox.delete(0, "end")
        self.duzenleNotEntry=Entry(self.duzenlePopup_root)

        adLabel=Label(self.duzenlePopup_root, text="Ad:", font=("Airal", 20), width=20)
        turLabel=Label(self.duzenlePopup_root, text="Tür:", font=("Airal", 20), width=20)
        durumLabel=Label(self.duzenlePopup_root, text="Durum:", font=("Airal", 20), width=20)
        yildizLabel=Label(self.duzenlePopup_root, text="Yıldız:", font=("Airal", 20), width=20)
        notLabel=Label(self.duzenlePopup_root, text="Not:", font=("Airal", 20), width=20)

        kaydetButon=Button(self.duzenlePopup_root, text="Kaydet", command=self.duzenle_islemi)

        adLabel.grid(row=0, column=0)
        self.duzenleAdEntry.grid(row=0, column=1)
        
        turLabel.grid(row=1, column=0)
        self.duzenleTurCombobox.grid(row=1, column=1)

        durumLabel.grid(row=2, column=0)
        self.duzenleDurumCombobox.grid(row=2, column=1)

        yildizLabel.grid(row=3, column=0)
        self.duzenleYildizSpinbox.grid(row=3, column=1)

        notLabel.grid(row=4, column=0)
        self.duzenleNotEntry.grid(row=4, column=1)

        kaydetButon.grid(row=5, column=0, columnspan=2)
        
    def duzenle_islemi(self):
    
        secili_indeks=self.liste.curselection()[0]
        veriler=self.loadfromJSON()
        
        

        for i in veriler:
            if i["ad"]==self.liste.get(secili_indeks):
                currentVideo=i
        
        currentVideo["ad"]=currentVideo["ad"] if self.duzenleAdEntry.get()=="" else self.duzenleAdEntry.get()
        currentVideo["tur"]=currentVideo["tur"] if self.duzenleTurCombobox.get()=="" else self.duzenleTurCombobox.get()
        currentVideo["durum"]=currentVideo["durum"] if self.duzenleDurumCombobox.get()=="" else self.duzenleDurumCombobox.get()
        currentVideo["yildiz"]=currentVideo["yildiz"] if self.duzenleYildizSpinbox.get()=="" else self.duzenleYildizSpinbox.get()
        currentVideo["not"]=currentVideo["not"] if self.duzenleNotEntry.get()=="" else self.duzenleNotEntry.get()

        self.savetoJSON(veriler)
        self.duzenlePopup_root.destroy()
        self.guncelle()


    def guncelle(self):
        self.liste.delete(0, END)


        with open("veriler.json", "r", encoding="utf-8") as file:
            veriler=json.load(file)

        for i in veriler:
            self.liste.insert(END, i["ad"])

    
    def ekle(self):
        self.ekle_root=Toplevel(self.root)
        self.ekle_root.geometry("500x280+710+300")

        self.adEntry=Entry(self.ekle_root)
        self.turCombobox=ttk.Combobox(self.ekle_root, values=["Dizi", "Film"])
        self.durumCombobox=ttk.Combobox(self.ekle_root, values=["İzlendi", "İzleniyor", "İzlenecek"])
        self.yildizSpinbox=Spinbox(self.ekle_root, from_=1, to=5)
        self.notEntry=Entry(self.ekle_root)

        adLabel=Label(self.ekle_root, text="Ad:", font=("Airal", 20), width=20)
        turLabel=Label(self.ekle_root, text="Tür:", font=("Airal", 20), width=20)
        durumLabel=Label(self.ekle_root, text="Durum:", font=("Airal", 20), width=20)
        yildizLabel=Label(self.ekle_root, text="Yıldız:", font=("Airal", 20), width=20)
        notLabel=Label(self.ekle_root, text="Not:", font=("Airal", 20), width=20)


        ekleButon=Button(self.ekle_root, text="Ekle", command=self.check, font=("Airal", 15))

        adLabel.grid(row=0, column=0)
        self.adEntry.grid(row=0, column=1)

        turLabel.grid(row=1, column=0)
        self.turCombobox.grid(row=1, column=1)

        durumLabel.grid(row=2, column=0)
        self.durumCombobox.grid(row=2, column=1)

        yildizLabel.grid(row=3, column=0)
        self.yildizSpinbox.grid(row=3, column=1)

        notLabel.grid(row=4, column=0)
        self.notEntry.grid(row=4, column=1)

        
        ekleButon.grid(row=6, column=0, columnspan=2)



    def sil(self):
        secili_indeks=self.liste.curselection()
        if secili_indeks:
            self.sil_pupop()
            


    def sil_pupop(self):
        self.silPupop_root=Toplevel()
        self.silPupop_root.geometry("300x100+830+350")
        bilgiLabel=Label(self.silPupop_root, text="Bu videoyu listeden silmek istediğinize emin misiniz?")
        yesButton=Button(self.silPupop_root, text="Evet", command=self.sil_islemi)
        noButton=Button(self.silPupop_root, text="Hayır", command=self.silPupop_root.destroy)

        bilgiLabel.grid(row=0, column=0, columnspan=2)
        yesButton.grid(row=1, column=0, pady=20)
        noButton.grid(row=1,column=1, pady=20)

    def sil_islemi(self):
            
            veriler=self.loadfromJSON()
            secili_indeks=self.liste.curselection()[0]
            
            for index, i in enumerate(veriler):
                if i["ad"]==self.liste.get(secili_indeks):
                    veriler.pop(index)
            
            


            
            self.savetoJSON(veriler)
            self.guncelle()
            self.silPupop_root.destroy()
            self.bilgilerLabel.config(text="")
            





    def ekle_2(self):
        ad=self.adEntry.get()
        tur=self.turCombobox.get()
        durum=self.durumCombobox.get()
        yildiz=self.yildizSpinbox.get()
        note=self.notEntry.get()
        
        

        data={
            "ad": ad,
            "tur": tur,
            "durum": durum,
            "yildiz": yildiz,
            "not": note
        }

        veriler=self.loadfromJSON()
        veriler.append(data)
        self.savetoJSON(veriler)

        self.popup_root.destroy()
        self.ekle_root.destroy()
        
        self.guncelle()






    def check(self):
        if self.adEntry.get()!="" and self.turCombobox.get()!="" and self.durumCombobox.get()!="":
            self.popup_eminMisin()
        else:
            self.ekle_root.destroy()
            messagebox.showerror("Hata", "Alanları Doldurunuz!")

    def popup_eminMisin(self):
        self.popup_root=Toplevel()
        self.popup_root.geometry("200x100+855+350")
        bilgiLabel=Label(self.popup_root, text="Kaydetmek istediğinize emin misiniz?")
        yesButton=Button(self.popup_root, text="Evet", command=self.ekle_2, width=5)
        noButton=Button(self.popup_root, text="Hayır", width=5)        

        bilgiLabel.grid(row=0, column=0, columnspan=2)
        yesButton.grid(row=1, column=0)
        noButton.grid(row=1, column=1)

    def savetoJSON(self, data, filename="veriler.json"):
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def loadfromJSON(self, filename="veriler.json"):
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
        
    






app=MediaPlayer()