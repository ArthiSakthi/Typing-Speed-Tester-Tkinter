import tkinter as tk
import ctypes
import random

ctypes.windll.shcore.SetProcessDpiAwareness(1)
storage = tk.Tk()
storage.title('Typing Speed Test')
storage.geometry('1400x700')
storage.option_add("*Label.Font", "consolas 30")
storage.option_add("*Button.Font", "consolas 30")
retry_button = None
text = ""
accuracy_label = None
secondsLeft = None

def handlingLabels():
    global text, secondsLeft
    random_selection = [
        'Biryani is prepared from basmati rice mixed with several spices and cooked in a special way. Chicken Biryani, Mutton Biryani and Veg Biryani are some of the variants of this delicious dish. This dish is my favourite because it has a lip-smacking flavour, and I love to eat it at least once a week.',
        'Noodles are usually cooked in boiling water, sometimes with cooking oil or salt added. They are often pan-fried or deep-fried. Noodles are often served with an accompanying sauce or in a soup. Noodles can be refrigerated for short-term storage or dried and stored for future use.',
        'Fried rice is a popular component of East Asian, Southeast Asian and certain South Asian cuisines, as well as a staple national dish of Indonesia. As a homemade dish, fried rice is typically made with ingredients left over from other dishes, leading to countless variations.',
        'Pasta is often noodles. It is usually eaten in sauce, fried or in soup. Pasta is usually made from either wheat flour or rice flour, but it can be made with other types of flour. Pasta sometimes has eggs in it.'
    ]
    text = random.choice(random_selection).lower()
    splitPoint = 0
    global nameLabelLeft, nameLabelRight, currentAlphabetLabel, writeAble, timer_started, secondsPassed
    nameLabelLeft = tk.Label(storage, text=text[0:splitPoint], fg='green')
    nameLabelLeft.place(relx=0.5, rely=0.5, anchor='e')
    nameLabelRight = tk.Label(storage, text=text[splitPoint:])
    nameLabelRight.place(relx=0.5, rely=0.5, anchor='w')
    currentAlphabetLabel = tk.Label(storage, text=text[splitPoint], fg='grey')
    currentAlphabetLabel.place(relx=0.5, rely=0.6, anchor='n')
    headingLabel = tk.Label(storage, text='Typing Speed Test', fg='dark blue')
    headingLabel.place(relx=0.5, rely=0.2, anchor='s')
    secondsLeft = tk.Label(storage, text='0 Seconds', fg='red')
    secondsLeft.place(relx=0.5, rely=0.4, anchor='s')
    writeAble = False
    timer_started = False
    storage.bind('<Key>', handlekeyPress)
    secondsPassed = 0
    storage.after(60000, stopGame)
    storage.after(1000, timeAddition)

def stopGame():
    global writeAble, text, accuracy_label
    writeAble = False
    typed_text = nameLabelLeft.cget('text')
    correct_characters = sum([1 for typed, original in zip(typed_text, text) if typed.lower() == original])
    total_characters = len(text)
    accuracy = (correct_characters / total_characters) * 100

    amountWords = len(nameLabelLeft.cget('text').split(' '))
    nameLabelLeft.config(text='')
    nameLabelRight.config(text='')
    currentAlphabetLabel.config(text='')
    secondsLeft.config(text=f'Words per Minute (WPM): {amountWords}', fg='green')
    storage.after(6000, destroyResult)
    global accuracy_label
    accuracy_label = tk.Label(storage, text=f'Accuracy: {accuracy:.2f}%', fg='green')
    accuracy_label.place(relx=0.5, rely=0.5, anchor='center')
    storage.after(6000, destroyResult)

def destroyResult():
    secondsLeft.config(text='')
    global accuracy_label, retry_button
    if accuracy_label:
        accuracy_label.destroy()
    if retry_button:
        retry_button.destroy()
    retry_button = tk.Button(storage, text='Retry', command=restartGame, fg='green')
    retry_button.place(relx=0.5, rely=0.4, anchor='center')

def restartGame():
    global secondsPassed, writeAble, timer_started, retry_button, accuracy_label
    secondsPassed = 0
    writeAble = False
    timer_started = False
    if retry_button:
        retry_button.destroy()
    if accuracy_label:
        accuracy_label.destroy()
    handlingLabels()

def timeAddition():
    global secondsPassed, writeAble, secondsLeft
    if writeAble:
        secondsPassed += 1
        if secondsLeft:
            secondsLeft.config(text=f'{secondsPassed} Seconds')
        storage.after(1000, timeAddition)

def handlekeyPress(event=None):
    global timer_started, writeAble
    if not timer_started:
        timer_started = True
        writeAble = True
        storage.after(1000, timeAddition)
    try:
        right_text = nameLabelRight.cget('text')
        if right_text and event.char.lower() == right_text[0].lower():
            nameLabelRight.config(text=right_text[1:])
            nameLabelLeft.config(text=nameLabelLeft.cget('text') + event.char.lower())
            currentAlphabetLabel.config(text=right_text[0])
    except tk.TclError:
        pass

handlingLabels()
storage.mainloop()

