import smtplib  #AUTOMATION OF EMAIL
import random
import time
import os.path
import mysql.connector 
from datetime import datetime
from tkinter import *
from tkinter import filedialog, messagebox, ttk
import tkinter.font
import pygame
from pygame import mixer        #FOR MUSIC
from PIL import ImageTk, Image  #FOR USING IMAGES

print('Folder path: ',os.path.dirname(__file__).replace('\\','/'))

#**************ENTER USER AND PASSWORD FOR MYSQL**************
db = mysql.connector.connect(host='localhost', user='',passwd='')
c = db.cursor()

#FUNCTION TO CREATE DATABASE
def create_database():
    com = '''CREATE DATABASE IF NOT EXISTS Music_Player'''
    c.execute(com)
    db.commit()

create_database()

#FUNCTION TO CREATE A NEW TABLE
def create_table():
    c.execute('USE Music_Player')
    com = '''CREATE TABLE IF NOT EXISTS accounts
            (Date VARCHAR(12),
            Username VARCHAR(20),
            Email VARCHAR(100),
            Password VARCHAR(20),
            Time VARCHAR(12)
            
            )'''
    c.execute(com)
    db.commit()

create_table()

#WINDOW1 - LOGIN WINDOW
root = Tk()
root.geometry('800x700') #800x800
root.title('Login')

#BACKGROUND + DESIGNS
back = Frame(root,
             width = 600,
             height = 600,
             bg = 'Lavender') #gray78

back.place(relx = 0.125, rely = 0.1)

des1 = Frame(back, width = 600, height = 65, bg = 'indigo') #gray18
des1.place(relx = 0, rely = 0)

des2 = Frame(back, width = 10, height = 600, bg = 'indigo')
des2.place(relx = 0, rely = 0.1)

des3 = Frame(back, width = 10, height = 600, bg = 'indigo')
des3.place(relx = 0.983, rely = 0.1)

des4 = Frame(back, width = 600, height = 65, bg = 'indigo')
des4.place(relx = 0, rely = 0.98)

im1 = Image.open(os.path.dirname(__file__).replace('\\','/')+'/PICS/Background/selected 1.png')
im_re = im1.resize((100,100))
im = ImageTk.PhotoImage(im_re)

im_frame = Label(back, image = im,bg='lavender')
im_frame.place(relx = 0.7, rely = 0.7)

im2 = Image.open(os.path.dirname(__file__).replace('\\','/')+'/PICS/Background/selected 2.png')
im_re2 = im2.resize((100,100))
im2 = ImageTk.PhotoImage(im_re2)

im2_frame = Label(back, image = im2,bg='lavender')
im2_frame.place(relx = 0.15, rely = 0.7)

#DETAILS INPUT
#HEADER
log = Label(back, font = ('caladea',20,'bold'),text = 'Login Details',fg = 'cyan', bg = 'indigo')
log.place(relx = 0.35, rely = 0.03)

#LABELS AND ENTRIES
un_label = Label(back, font = ('caladea',17,'bold'),text = 'Username:',fg='indigo',bg = 'lavender')
un_label.place(relx = 0.14, rely = 0.18)

tv1 = StringVar(back) #TEXT VARIABLE FOR USERNAME
un = Entry(back, textvariable = tv1, width = 40, justify=LEFT)
un.place(relx = 0.43, rely = 0.195)

email_label = Label(back, font = ('caladea',17,'bold'),text = 'Email Id:',fg='indigo',bg = 'lavender')
email_label.place(relx = 0.16, rely = 0.28)

tv2 = StringVar(back) #TEXT VARIABLE FOR EMAIL
email = Entry(back, textvariable = tv2, width = 40, justify=LEFT)
email.place(relx = 0.43, rely = 0.295)

passw_label = Label(back, font = ('caladea',17,'bold'),text = 'Password:',fg='indigo',bg = 'lavender')
passw_label.place(relx = 0.14, rely = 0.38)

tv3 = StringVar(back) #TEXT VARIABLE FOR PASSWORD
passw = Entry(back, textvariable = tv3, width = 40, justify=LEFT)
passw.place(relx = 0.43, rely = 0.395)

pass_re_label = Label(back, font = ('caladea',17,'bold'),text = 'Confirm Password:',fg='indigo', bg = 'lavender')
pass_re_label.place(relx = 0.07, rely = 0.48)

tv4 = StringVar(back) #TEXT VARIABLE FOR PASSWORD RE-ENTER
pass_re = Entry(back, textvariable = tv4, width = 40, justify=LEFT)
pass_re.place(relx = 0.43, rely = 0.495)

print(tv1.get(),tv2.get(), tv3.get(), tv4.get())

def login():
    #CHECKING USERNAME
    if len(tv1.get()) >= 19:
        messagebox.showwarning('Change Username',
                               'Username too long'+
                               '\nMust be less than 20 Characters.')
        return
    c.execute('SELECT Username FROM accounts')
    if (tv1.get(),) in c.fetchall():
        messagebox.showwarning('Change Username','Username already taken.')
        return

    #CHECKING EMAIL
    if '@gmail.com' not in tv2.get():
        if tv2.get() == '':
            messagebox.showwarning('Data Incomplete','Please Enter your email id.')
        else:
            messagebox.showwarning('Incorrect Email ','Please Enter email with @gmail.com as domain.')

    #CHEKING REGISTERED MAIL
    c.execute('SELECT Email FROM accounts')
    
    if (tv2.get(),) in c.fetchall():
        def new_accounts():
            global new_user
            global newu
            
            #NEW ACCOUNTS CHECK
            new = Toplevel(root)
            new.geometry('800x250')
            new.title('Email Detected')

            new_label = Label(new,text = 'This Email has already been registered.'+
                                         ' Click YES to continue with the registered one and enter the following details'+
                                         ' or EXIT to create new accounts.')
            new_label.place(relx = 0.025, rely = 0.05)

            newul = Label(new, text = 'Username')
            newul.place(relx = 0.2, rely = 0.2)
            
            newu = StringVar()
            new_user = Entry(new, textvariable = newu, width=40)
            new_user.place(relx = 0.3, rely = 0.2)
            
            newpl = Label(new, text = 'Password')
            newpl.place(relx = 0.2, rely = 0.3)
            
            newp = StringVar()
            new_pass = Entry(new, textvariable = newp, width=40)
            new_pass.place(relx = 0.3, rely = 0.3)
            
            def yes(): #FUNCTION FOR 'Yes' BUTTON
                l = []
                c.execute("select Username from accounts")
                for y in c.fetchall():
                    for y1 in y:
                        l.append(y1)
                if new_user.get() not in l:
                    messagebox.showwarning('User error','Username not found')
                    return
                
                c.execute("select Password from accounts "+
                          "where Username = "+"'"+new_user.get()+"'"+"and Email="+"'"+tv2.get()+"'")
                for x in c.fetchall():
                    for z in x:
                        if z == newp.get():
                            messagebox.showinfo('Correct Password','Welcome '+new_user.get()+'.')
                            new.destroy()
                            time.sleep(1)
                            root.destroy()
                            
                        else:
                            messagebox.showwarning('Incorrect Password','Incorrect password')
                     
            b1 = Button(new,text = 'Yes', command = yes)
            b1.place(relx = 0.5, rely = 0.4)

            def no():
                new.destroy()
            
            b2 = Button(new,text = 'Exit', command = no)
            b2.place(relx = 0.5, rely = 0.55)
        new_accounts()
    
    #CHECKING PASSWORDS
    p = tv3.get() == '' and tv4.get() == ''

    if len(tv3.get()) >=19 or len(tv4.get()) >= 19:
        messagebox.showwarning('Change Password',
                               'Password too long.'+
                               '\nMust be less than 20 Characters')
        
    if p == True:
        messagebox.showwarning('Incorrect Password',"Passwords can't be blank.")
    q = tv3.get() != tv4.get()
    if q == True:
        messagebox.showwarning('Incorrect Password','Please check your password again.')
        
    if (p == False) and (q == False) and ('@gmail.com' in tv2.get()):
        print('\nEmail Using Get method: ',tv2.get())
    
    #OTP SYSTEM    
        otp = random.randint(100000,999999)

        server = smtplib.SMTP('smtp.gmail.com',587)  #PORTAL FOR SMTP LIBRARY, 587 = PORT NUMBER FOR @gmail.com emails
        server.starttls()

        msg = 'Thanks for logging in our Music Player. '+'\nThis is your One Time Password (OTP): '+str(otp)+'\nHave a good day.'

        #**************ENTER EMAIL ID AND PASSWORD**************
        server.login('<email>','<passwd>')
        server.sendmail('<emailid>',tv2.get(),msg)
        print("OTP: ",otp)

        messagebox.showinfo('OTP VERIFICATION ','OTP SENT TO '+ tv2.get())

        #OTP VERIFICATION
        winotp = Toplevel(root)
        winotp.geometry('150x150')
        winotp.title('OTP')

        tv_otp = IntVar(winotp)
        otp_l = Label(winotp, text = 'Enter OTP: ')
        otp_l.pack(expand=True)
        
        otp_e = Entry(winotp, textvariable = tv_otp, width = 40)
        otp_e.pack(expand=True)

        def otp_checking():
            if tv_otp.get() == otp:
                messagebox.showinfo('Successful Login',
                                    'The OTP you have entered is correct.'+
                                    '\nYour accounts has been created successfully.')

                #INSERTING INTO TABLE
                user_t = tv1.get()
                email_t = tv2.get()
                pass_t = tv4.get()
                date_now = time.strftime('%d/%m/%Y')
                time_now = time.strftime('%H:%M:%S')

                inserting = "INSERT INTO accounts(Date,Username,Email,Password,Time) value(%s,%s,%s,%s,%s)"
                vals = (date_now, user_t, email_t, pass_t, time_now)
        
                c.execute(inserting,vals)
                db.commit()
                                    
                winotp.destroy()
                time.sleep(0.8)
                root.destroy()
                                
            if tv_otp.get() != otp:
                messagebox.showwarning('Incorrect OTP','Please Re-enter OTP.')
        
        check = Button(winotp, text='Check', command=otp_checking)
        check.pack(expand=True)

#LOGIN WINDOW BUTTONS AND COMMANDS
otp_button = Button(back, text = 'Get OTP',width = 10, height=2, command = login)
otp_button.place(relx = 0.45, rely = 0.66)

guest = Label(back,font = ('caladea',11), text = 'Or Continue as Guest?', bg='lavender')
guest.place(relx = 0.39, rely = 0.77)

def gd():
    root.destroy()
    
guest_button = Button(back, text = 'Guest',width = 10, height=1, command = gd)
guest_button.place(relx = 0.45, rely = 0.82)

root.resizable(False,False)
root.mainloop()

#WINDOW2 - MUSIC PLAYER
win2 = Tk()
win2.geometry('1100x500')
win2.title('Music Player')

#BACKGROUND
background = Frame(win2, bg='cornflower blue', width = 1080)
background.place(relx = 0.00869, rely = 0.13, height=360)

#INSERTING LOGIN DATA IN A FILE
def filedata():
    global tv1
    global tv2
    global tv3
    global gd

    f = open('Music_Player_Account_Details.txt','a+')

    f.write('\n*****LOGIN DETAILS*****')
    f.write('\n\nDate: '+str(time.strftime('%d/%m/%Y')))
    f.write('\nTime: '+str(time.strftime('%H:%M:%S')))
    f.write('\nUsername: '+str(tv1.get()))
    f.write('\nEmail Id: '+str(tv2.get()))
    f.write('\nPassword: '+str(tv4.get()))
    f.write('\n\n------------------------------------------------')
    f.close()
    
filedata()

pygame.init()
mixer.init()

#HORI TOP + TOP LABEL
des1 = Frame(win2, width = 1100, height = 65, bg = 'gray18')
des1.place(relx = 0, rely = 0)
lab1 = Label(des1,font = ('',32), text='Music Player',fg = background['bg'], bg = 'gray18')
lab1.place(relx = 0.39, rely = 0.12)

#VERT LEFT
des2 = Frame(win2, width = 10, height = 1100, bg = 'gray18')
des2.place(relx = 0, rely = 0.1)

#VERT RIGHT
des3 = Frame(win2, width = 10, height = 1100, bg = 'gray18')
des3.place(relx = 0.991, rely = 0.1)

#HORI BOTTOM
des4 = Frame(win2, width = 1100, height = 76, bg = 'gray18')
des4.place(relx = 0, rely = 0.85)

intdir = '\Music'.replace('\\','//')

curr_playing = Label(background, text = '', width = 98, height = 3, justify = CENTER)
curr_playing.place(relx = 0, rely = 0.75)
curr_playing.config(font = ('',14), bg = background['bg'])

#FUNCTION FOR LOADING A TRACK
def load_play():
    global curr_playing
    f = filedialog.askopenfilename(title = 'Choose your track',
                                   initialdir = intdir,
                                   filetype = (('mp3 files', '*.mp3'),('wav files','*.wav')))

    #CURRENTLY PLAYING - LOAD TRACK
    l = f.split('/')
    curr_play_f_text = l[-1][-5::-1][::-1]
    lst_cp_f = []
    lst_cp_f.append(curr_play_f_text)
    #print(curr_play_f_text)
    #print(lst_cp_f, '\n')

    #CURRENTLY PLAYING - LABEL - LOAD TRACK
    t_loadtrack = 'Currently Playing: ' + curr_play_f_text

    if curr_play_f_text == '':
        pass
    else:
        #print(f)
        curr_playing.config(font = ('',14), bg = background['bg'],text = t_loadtrack)

        playB['text'] = 'PLAY'
        playB['image'] = pi
    
        mixer.music.load(f)
        mixer.music.play(1)

#FUNCTION FOR PAUSE AND PLAY
def pause_play():
    if playB['text'] == 'PLAY':
        playB['text'] = 'PAUSE'
        playB['image'] = pi2
        mixer.music.pause()
        
    else:
        playB['text'] = 'PLAY'
        playB['image'] = pi
        mixer.music.unpause()

#FUNCTION FOR REPLAYING TRACK
def prev():
    mixer.music.rewind()

#FUNCTION FOR ADDING A TRACK IN QUEUE
def queue():
    global f2
    f2 = filedialog.askopenfilename(title = 'Add to queue',
                                   initialdir = intdir,
                                   filetype = (('mp3 files', '*.mp3'),('wav files','*.wav')))
    if f2 == '':
        pass
    else:
        print('\nQueue: ',f2)
        mixer.music.queue(f2)

#FUNCTION FOR NEXT TRACK
def next_song():
    try:
        f2
    except NameError:
        messagebox.showwarning('Empty Queue','Please add a song to queue')
    else:
        #CURRENTLY PLAYING - NEXT TRACK
        l = f2.split('/')
        curr_play_f2_text = l[-1][-5::-1][::-1]
        lst_cp_f2 = []
        lst_cp_f2.append(curr_play_f2_text)
        #print(curr_play_f2_text)
        #print(lst_cp_f2, '\n')

        #CURRENTLY PLAYING - LABEL - NEXT TRACK
        t_nexttrack = 'Currently Playing: ' + curr_play_f2_text

        if len(curr_play_f2_text) == 0:
            messagebox.showwarning('Empty Queue','Please add a song to queue')
            pass

        else:
            curr_playing.config(font = ('',14), bg = background['bg'],text = t_nexttrack)

            playB['text'] = 'PLAY'
            playB['image'] = pi
        
            mixer.music.stop()
            mixer.music.load(f2)
            mixer.music.play(1)

#FUNCTION FOR SHUFFLE
def shuffle():
    f2 = ''
    p =  os.path.dirname(__file__).replace('\\','/')+'/Music_MP3/'
    l1 = []
    l2 = []
    l3 = []

    #PATH FOR SHUFFLE
    for x in os.listdir(p):
        l1.append(x)

    p2 = p+random.choice(l1)+'/'
    for y in os.listdir(p2):
        l2.append(y)

    p3 = p2+random.choice(l2)+'/'
    for z in os.listdir(p3):
        l3.append(z)

    song = p3+random.choice(l3)
    #print('\n', song)

    #CURRENTLY PLAYING - SHUFFLE
    l = song.split('/')
    curr_play_shuf_text = l[-1][-5::-1][::-1]
    lst_cp_shuf = []
    lst_cp_shuf.append(curr_play_shuf_text)
    #print(curr_play_shuf_text)
    #print(lst_cp_shuf, '\n')

    #CURRENTLY PLAYING - LABEL - SHUFFLE
    t_shuf = 'Currently Playing: ' + curr_play_shuf_text
    curr_playing.config(font = ('',14), bg = background['bg'],text = t_shuf)

    playB['text'] = 'PLAY'
    playB['image'] = pi
    
    mixer.music.load(song)
    mixer.music.play(1)

#FUNCTION FOR VOLUME SLIDER
def volume(x):
    mixer.init()
    mixer.music.set_volume(vol.get())

#FUNCTION FOR PLAYLIST - ENGLISH
def playlist_eng():
    eng_path = os.path.dirname(__file__).replace('\\','/')+'/Music_MP3/English/'
    
    playlist1 = Toplevel(win2)
    playlist1.geometry('500x300')
    playlist1.title('English Playlist')

    eng_gen = []
    gen_songs = []

    song_frame = Listbox(playlist1,width=200,bg = 'gray78')
    song_frame.pack(padx = 10, pady=10, fill = BOTH)
    
    for genre in os.listdir(eng_path): #GETS A LIST OF GENRE
        eng_gen.append(genre)
        
        def genre_path(x = genre):
            song = eng_path + x + '/'
            
            for songs in os.listdir(song): #GETS A LIST OF SONGS
                gen_songs.append(songs)
                
                for j in range(len(gen_songs)):
                    n = gen_songs[j]
                    name = n+'_button'
                    
                def song_path(x=name[:-7]): #LIST OF SONG PATH
                    songpath = song + x
                    #song_path.songname = songpath
                    #print('Songpath: ',songpath)
                    mixer.music.load(songpath)
                    mixer.music.play(1)

                    #CURRENTLY PLAYING - ENGLISH
                    l = songpath.split('/')
                    curr_play_eng_text = l[-1][-5::-1][::-1]
                    lst_cp_eng = []
                    lst_cp_eng.append(curr_play_eng_text)
                    #print(curr_play_eng_text)
                    #print(lst_cp_eng, '\n')

                    #CURRENTLY PLAYING - LABEL - ENGLISH
                    t_eng = 'Currently Playing: ' + curr_play_eng_text
                    curr_playing.config(font = ('',14), bg = background['bg'],text = t_eng)

                    playB['text'] = 'PLAY'
                    playB['image'] = pi
                       
                name = Button(song_frame,bg = 'gray78', text=songs[:-4], relief = FLAT, command = song_path)
                name.pack(side=TOP)

        for i in range(len(eng_gen)):
            name2 = eng_gen[i]+'_button'
        name2 = Button(playlist1, text=' '+genre+' ', command = genre_path)
        name2.pack()
    
    
#FUNCTION FOR PLAYLIST - HINDI
def playlist_hin():
    hin_path = os.path.dirname(__file__).replace('\\','/')+'/Music_MP3/Hindi/'

    playlist2 = Toplevel(win2)
    playlist2.geometry('500x300')
    playlist2.title('Hindi Playlist')

    hin_gen = []
    gen_songs2 = []

    song_frame2 = Listbox(playlist2,width=200,bg = 'gray78')
    song_frame2.pack(padx = 10, pady=10, fill = BOTH)

    for genre in os.listdir(hin_path): #GETS A LIST OF GENRE
        hin_gen.append(genre)

        def genre_path(x = genre):
            song = hin_path + x + '/'

            for songs in os.listdir(song): #GETS A LIST OF SONGS
                gen_songs2.append(songs)
                
                for j in range(len(gen_songs2)):
                    n3 = gen_songs2[j]
                    name3 = n3+'_button'

                def song_path(x = name3[:-7]): #LIST OF SONG PATH
                    songpath2 = song + x
                    #song_path.songname2 = songpath2
                    #print('Songpath: ',songpath2)
                    mixer.music.load(songpath2)
                    mixer.music.play(1)

                    #CURRENTLY PLAYING - HINDI
                    l2 = songpath2.split('/')
                    curr_play_hin_text = l2[-1][-5::-1][::-1]
                    lst_cp_hin = []
                    lst_cp_hin.append(curr_play_hin_text)
                    #print(curr_play_hin_text)
                    #print(lst_cp_hin,'\n')

                    #CURRENTLY PLAYING - LABEL - HINDI
                    t_hindi = 'Currently Playing: ' + curr_play_hin_text
                    curr_playing.config(font = ('',14),bg = background['bg'],text = t_hindi)

                    playB['text'] = 'PLAY'
                    playB['image'] = pi

                name3 = Button(song_frame2 ,bg = 'gray78', text=songs[:-4], relief = FLAT, command = song_path)
                name3.pack(side=TOP)
        
        for i in range(len(hin_gen)):
            name4 = hin_gen[i]+'_button'
        name4 = Button(playlist2, text=' '+genre+' ', command = genre_path)
        name4.pack()

#FUNCTION FOR "WELCOME" LABEL
def textlb(): 
    global tv1
    global newu
    global new_user
    
    try:
        newu.get()
    except NameError:
        guest_no = str(random.randint(1000,9999))
        textlb.xc = 0.41
        textlb.text_lb = 'Welcome Guest_'+ guest_no
    else:
        if (tv1.get() != newu.get()) or (len(tv1.get()) == 0):
            textlb.xc = 0.39999
            c.execute("SELECT Username FROM accounts")
            for v in c.fetchall():
                if v == (newu.get(),):
                    textlb.text_lb = 'Welcome ' + newu.get()
                    break
                if v == (tv1.get(),):
                    textlb.text_lb = 'Welcome ' + tv1.get()
                    break


#FUNCTION FOR THEME CHANGE
def theme():
    global background
    global backg_label
    global lab1

    color_file = open(os.path.dirname(__file__).replace('\\','/')+'/Colors.txt', 'r')
    colors = []

    for x in  color_file.readlines():
        colors.append(x[0:-1])
    r = random.choice(colors)

    background['bg'] = backg_label['bg'] = lab1['fg'] = r
    curr_playing.config(bg = r)
    
    color_file.close()
    colors.clear()

textlb()
txt = textlb.text_lb
xc = textlb.xc

#LABEL ON TOP OF BACKGROUND
backg_label = Label(background,font = ('',15), bg = background['bg'], text = txt, justify = CENTER)
backg_label.place(relx = xc, rely = 0.04)

#ENG PLAYLIST
eng_playlist = Button(win2, text = 'English',font = ('',25), bg='gray78',relief = SUNKEN, command = playlist_eng)
eng_playlist.place(relx = 0.2, rely = 0.25, width = 200, height = 200)

#HIN PLAYLIST
hin_playlist = Button(win2, text = 'Hindi',font = ('',25), bg='gray78',relief = SUNKEN, command = playlist_hin)
hin_playlist.place(relx = 0.6, rely = 0.25, width = 200, height = 200)

#BUTTON IMAGE - LOAD TRACK
ltrack = Image.open(os.path.dirname(__file__).replace('\\','/')+'/PICS/Load Track.png')
ltrack_image = ltrack.resize((50,50))
lti = ImageTk.PhotoImage(ltrack_image)

#BUTTON IMAGE - PLAY BUTTON
play = Image.open(os.path.dirname(__file__).replace('\\','/')+'/PICS/play-button.png')
play_image = play.resize((40,40))
pi = ImageTk.PhotoImage(play_image)

#BUTTON IMAGE - PAUSE BUTTON
pause = Image.open(os.path.dirname(__file__).replace('\\','/')+'/PICS/pause-button.png')
pause_image = pause.resize((40,40))
pi2 = ImageTk.PhotoImage(pause_image)

#BUTTON IMAGE - REPLAY SONG BUTTON
re = Image.open(os.path.dirname(__file__).replace('\\','/')+'/PICS/backward.png')
re_image = re.resize((40,40))
rei = ImageTk.PhotoImage(re_image)

#BUTTON IMAGE - NEXT SONG BUTTON
Next = Image.open(os.path.dirname(__file__).replace('\\','/')+'/PICS/next.png')
ne_image = Next.resize((40,40))
nei = ImageTk.PhotoImage(ne_image)

#BUTTON IMAGE - QUEUE BUTTON
qu = Image.open(os.path.dirname(__file__).replace('\\','/')+'/PICS/queue.png')
qu_image = qu.resize((40,40))
qui = ImageTk.PhotoImage(qu_image)

#BUTTON IMAGE - SHUFFLE BUTTON
sh = Image.open(os.path.dirname(__file__).replace('\\','/')+'/PICS/shuffle.png')
sh_image = sh.resize((30,30))
shi = ImageTk.PhotoImage(sh_image)

#LOAD TRACK BUTTON
loadB = Button(win2,image=lti, text = 'LOAD', bg = 'gray78', command = load_play)
loadB.place(relx = 0.0087, rely = 0.878, width = 100, height = 50)

#REPLAY BUTTON
reB = Button(win2, image=rei, text = 'PREV', bg = 'gray78', command = prev)
reB.place(relx = 0.332, rely = 0.878, width = 100, height = 50)

#PLAY BUTTON
playB = Button(win2, image=pi, text='PLAY', bg = 'gray78', command = pause_play)
playB.place(relx = 0.452, rely = 0.878, width = 100, height = 50)

#NEXT BUTTON
neB = Button(win2, image=nei, text = 'NEXT', bg = 'gray78', command = next_song)
neB.place(relx = 0.572, rely = 0.878, width = 100, height = 50)

#QUEUE BUTTON
queueB = Button(win2, image=qui, text = 'QUEUE', bg = 'gray78', command = queue)
queueB.place(relx = 0.7287, rely = 0.878, width = 100, height = 50)

#SHUFFLE BUTTON
shuffleB = Button(win2, image=shi, text = 'SHUFFLE', bg = 'gray78', command = shuffle)
shuffleB.place(relx = 0.887, rely = 0.878, width = 70, height = 50)

#THEME BUTTON
themeB = Button(win2, text = 'THEME', bg = 'gray78', command = theme)
themeB.place(relx = 0.916, rely = 0.15, width = 70, height = 50)

#VOLUME SLIDER
vol = ttk.Scale(win2, from_=0, to=1, orient = HORIZONTAL, value=1, command = volume)
vol.place(relx = 0.1687, rely = 0.896)

win2.resizable(False,False)
win2.mainloop()

#END OF PROJECT
