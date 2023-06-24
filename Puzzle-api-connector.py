import tkinter as tk
from tkinter import filedialog
import requests
from tkinter import messagebox

def select_image():
    root = tk.Tk()
    root.withdraw()

    # Wybieranie pliku obrazka za pomocą okna dialogowego
    image_file = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    
    if image_file:
        url = 'http://localhost:5000/puzzle'  # Adres URL Twojego serwera Flask

        # Wczytanie obrazka do przesłania
        files = {'image': open(image_file, 'rb')}

        # Wysłanie żądania POST z obrazkiem
        response = requests.post(url, files=files)

        # Odczytanie odpowiedzi serwera
        data = response.json()
        if 'error' in data:
            messagebox.showerror('Błąd', data['error'])
        else:
            message = f"Układanka została utworzona. Nazwa przetworzonego obrazka: {data['processed_image']}"
            messagebox.showinfo('Sukces', message)

select_image()
