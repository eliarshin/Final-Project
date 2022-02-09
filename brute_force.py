import random
import pyautogui

chars = "abcdefghijklmnopqrstuvwxyz0123456789"
char_list = list(chars)

pw = pyautogui.password("Enter a password:")
guess =""

while(guess != pw):
    guess = random.choices(char_list, k =len(pw))
    print("<======"+str(guess)+"======>")

    if(guess == list(pw)):
        print("your password is : "+ "".join(guess))
        break
