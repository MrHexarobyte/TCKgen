from io import BytesIO
from pathlib import Path
from PIL import Image, UnidentifiedImageError, ImageDraw,ImageFont
import PySimpleGUI as sg

arial = ImageFont.truetype('arial.ttf', size=17, encoding="unic")
def image_to_data(im):
    """
    Image object to bytes object.
    : Parameters
      im - Image object
    : Return
      bytes object.
    """
    with BytesIO() as output:
        im.save(output, format="PNG")
        data = output.getvalue()
    return data


temp=Image.open('temp.jpg')
restemp = temp.resize((462,288))
rltemp = image_to_data(restemp)

sg.theme('DarkGrey3')

width, height = size = 462,288    
layout = [
    [sg.Text('Vesikalık Foto'),sg.Input(expand_x=True, disabled=True, key='File'), sg.Button('Browse')],
    [sg.Text('TCKN'),sg.Input(key='-TCKN-',expand_x=True)],
    [sg.Text('Soyisim'),sg.Input(key='-SISIM-',expand_x=True)],
    [sg.Text('İsim'),sg.Input(key='-ISIM-',expand_x=True)],
    [sg.Text('Doğum Tarihi'),sg.Input(key='-DT-',expand_x=True)],
    [sg.Text('Cinsiyet'),sg.Input(key='-CNS-',expand_x=True)],
    [sg.Text('Seri No (Örnek: 7505297F)'),sg.Input(key='-SRINO-',expand_x=True)],
    [sg.Text('Son Geçerlilik Tarihi'),sg.Input(key='-SGT-',expand_x=True)],
    [sg.Button(button_text='Oluştur',key='-OK-')],
    [sg.Text('', expand_x=True, key='Status')],
    [sg.Image(size=size,data=rltemp, background_color='green', key = "Image")],
]
window = sg.Window("TCK GEN", layout)

sisim = 'isimsiz nigga'
while True:

    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break

    elif event == "Browse":
        path = sg.popup_get_file("", no_window=True)
        if path == '':
            continue
        window['Status'].update('')
        window['File'].update(path)
        if not Path(path).is_file():
            window['Status'].update('Image file not found !')
            continue
        try:
            im = Image.open(path)
        except UnidentifiedImageError:
            window['Status'].update("Cannot identify image file !")
            continue
        w, h = im.size
        scale = min(width/w, height/h, 1)
        
        bg_w, bg_h = restemp.size
        img = im.resize((110,125),resample=Image.LANCZOS)
        img_w, img_h = img.size
        offset = ((bg_w - img_w) // 2-144, (bg_h - img_h) // 2+32)
        restemp.paste(img,offset)
        
        restemp.save('progress.png')
        data = image_to_data(restemp)

        window['Image'].update(data=data, size=size)
    elif event == '-OK-':
        sisim = values['-SISIM-']  
        isim = values['-ISIM-']  
        dt = values['-DT-']  
        tckn = values['-TCKN-']  
        srino = values['-SRINO-']
        cns = values['-CNS-']
        sgt = values['-SGT-']

        newimg = Image.open('progress.png')
        I1 = ImageDraw.Draw(newimg)
        I1.text((17, 90), tckn, font=arial, fill =(0, 0, 0)) #TC KIMLIK NUMARASI
        I1.text((161, 90), sisim, font=arial, fill =(0, 0, 0)) # SOYISIM
        I1.text((161, 130), isim, font=arial, fill =(0, 0, 0)) # ISIM
        I1.text((161, 170), dt, font=arial, fill =(0, 0, 0)) #DOĞUM TARIHI
        I1.text((278, 170), cns, font=arial, fill =(0, 0, 0)) #CINSIYET
        I1.text((161, 210), srino, font=arial, fill =(0, 0, 0)) #SERI NO
        I1.text((161, 250), sgt, font=arial, fill =(0, 0, 0)) #SON GECERLILIK TARIHI


        window['Image'].update(data=image_to_data(newimg), size=size,)

window.close()
