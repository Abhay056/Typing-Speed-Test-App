import time
import random
import tkinter as tk
from tkinter import messagebox

class FrontScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Welcome to Typing Speed Test")

        # Set the position to center the window on the screen
        window_width = 900
        window_height = 400
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        x_position = (screen_width - window_width) // 2 
        y_position = (screen_height - window_height) // 2

        # Set the geometry of the window
        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        self.root.configure(bg="darkorchid")

        self.welcome_message = "\n\n\n\nWelcome to Typing Speed Test"
        self.welcome_animation_delay = 100

        self.canvas = tk.Canvas(self.root, width=600, height=50, bg="darkorchid")
        self.canvas.pack(pady=10)

        self.create_widgets()

    def animate_welcome(self):
        colors = ["red", "orange", "yellow", "cyan", "blue", "lightblue", "lime"]

        self.canvas.delete("all")
        total_width = 19 * len(self.welcome_message)
        x_position = (600 - total_width) // 2

        for letter in self.welcome_message:
            color = random.choice(colors)
            self.canvas.create_text(x_position, 25, text=letter, fill=color, font=("Candara", 20))
            x_position += 19  # Adjust the spacing between letters
        self.animation_update_id = self.root.after(self.welcome_animation_delay, self.animate_welcome)

    def create_widgets(self):
        self.animate_welcome()
        self.detail_instructions = tk.Label(self.root, text="""\n       This is a Typing Speed Test Application\n
        It will show your typing speed and Accuracy\n
        To get Started Click on the 'Start Typing Test' button below""", font=("Palatino", 14), fg="seagreen1",bg="darkorchid", )
        self.detail_instructions.pack(pady=10, fill="both", expand=True)
        start_button = tk.Button(self.root, text="Start Typing Test", font=("Palatino", 14), bg="silver", command=self.close_front_screen)
        start_button.pack(pady=20)

        self.canvas2 = tk.Label(self.root, text="Created by Abhay Bahuguna", font=("Palatino", 14), fg="cyan", bg="darkorchid")
        self.canvas2.pack(pady=20, fill="both", expand=True)

    def close_front_screen(self):
        self.root.after_cancel(self.animation_update_id)
        self.root.destroy()  # Close the front screen
        TypingSpeedTestApp(tk.Tk())  # Open the main typing test screen

class TypingSpeedTestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test")
        
        # Set the position to center the window on the screen
        window_width = 900
        window_height = 500  
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        x_position = (screen_width - window_width) // 2 
        y_position = (screen_height - window_height) // 2

        # Set the geometry of the window
        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        self.root.configure(bg="darkorchid")

        self.text_to_type = ""
        self.start_time = 0

        self.timers = {
            "15 seconds": 15,
            "30 seconds": 30,
            "60 seconds": 60
        }

        self.selected_timer = tk.StringVar(value="30 seconds")
        self.start_time = 0
        self.create_widgets()

    def get_random_text(self):
        texts = [
            "The quick brown fox jumps over the lazy dog and the lazy dog is still sleeping cause he does not care about what is going around.",
            "Python is a versatile programming language with vast number of features which can be used in performing various tasks.",
            "Coding is fun and rewarding until nd unless someone is bored from coding but one should not leave coding till the end.",
            "Practice makes a man or woman perfect practice can even make you an expert in any programming language.",
            "I dont know why I am doing this but still I want to do this because if I will not do this then I will do something else.",
            "Philosophy is a systematic study of general questions concerning topics like existence, reason, knowledge, value, mind.",
            "Artificial intelligence (AI) is the intelligence of machines or software, as opposed to the intelligence of humans or animals.",
            "Technology is the application of conceptual knowledge for achieving practical goals, especially in a reproducible way.",
            "Astronomy is a natural science that studies celestial objects and the phenomena that occur in the cosmos.",
            "Virtualisation is the act of creating a virtual version of something at the same abstraction level.",
            "When I've built up my savings, I'll be able to travel to Mexico.",
            "Wouldn't it be lovely to enjoy a week soaking up the culture?",
            "The plots failed because of some trusted friends of the king.",
            "After the death of the king, everyone wanted to be a king.",
            "War does not bring anything good to the common people.",
            "If opportunity doesn't knock, build a door."
        ]
        return random.choice(texts)

    def calculate_accuracy(self, original_text, user_input):
        original_words = original_text.split()
        user_words = user_input.split()

        correct_words = sum(1 for original, user in zip(original_words, user_words) if original == user)
        accuracy_percentage = (correct_words / len(original_words)) * 100
        return accuracy_percentage

    def start_typing_test(self):
        self.text_to_type = self.get_random_text()
        self.canvas1.config(text=f"{self.text_to_type}")
        self.start_time = time.time() 
        self.update_timer(self.start_time)
        self.user_input_entry.focus_set()

        selected_timer_value = self.timers[self.selected_timer.get()]
        self.root.after(selected_timer_value * 1000, lambda:self.finish_typing_test(self.user_input_entry.get(), stop_timer = True))

    def finish_typing_test(self, user_input, stop_timer = False):
        if stop_timer:
            self.root.after_cancel(self.timer_update_id)
        
        end_time = time.time()
        words_per_minute = 0
        accuracy_percentage = 0
        time_taken = end_time - self.start_time    
        words_per_minute = len(self.text_to_type.split()) / (time_taken / 60)

        if user_input.strip() == self.text_to_type:
            accuracy_percentage = 100.0
        else:
            accuracy_percentage = self.calculate_accuracy(self.text_to_type, user_input)

        result_message = f"\nYour typing speed: {words_per_minute:.2f} words per minute\nAccuracy: {accuracy_percentage:.2f}%"

        messagebox.showinfo("Typing Speed Test Result", result_message)
        self.user_input_entry.delete(0, tk.END)

    def on_enter_key(self, event):
        self.finish_typing_test(self.user_input_entry.get())  

    def update_timer(self, start_time):
        elapsed_time = int(time.time() - start_time)
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        self.timer_label.config(text=f"Timer: {minutes}:{seconds:02}")
        self.timer_update_id = self.root.after(1000, lambda:self.update_timer(start_time))  # Update every 1000 milliseconds (1 second)

    def create_widgets(self):
        self.canvas1 = tk.Label(self.root, text=f"Select your timer from below dropdown menu then Click Start button to start test, press Enter to end. \n", font=("Cambria",12), fg="white", bg="darkorchid")
        self.canvas1.pack(pady=20, fill="both", expand=True)

        timer_label = tk.Label(self.root, text="Select Timer:", font=("Palatino", 14), fg="yellow", bg="darkorchid")
        timer_label.pack(pady=10)

        timer_dropdown = tk.OptionMenu(self.root, self.selected_timer, *self.timers.keys())
        timer_dropdown.pack(pady=10)

        self.timer_label = tk.Label(self.root, text="Timer: 0:00", font=("Helvetica", 14), fg="white", bg="darkorchid")
        self.timer_label.pack(pady=10)

        self.start_button = tk.Button(self.root, text="Start", font=("Palatino",15), bg="silver", command=self.start_typing_test)
        self.start_button.pack(pady=20)

        self.user_input_entry = tk.Entry(self.root, width=100)
        self.user_input_entry.pack(pady=10, fill="both")
        self.user_input_entry.bind("<Return>", self.on_enter_key)

        self.canvas2 = tk.Label(self.root, text="Created by Abhay Bahuguna", font=("Palatino", 14), fg="cyan", bg="darkorchid")
        self.canvas2.pack(pady=20, fill="both", expand=True)

if __name__ == "__main__":
    front_screen_root = tk.Tk()
    front_screen = FrontScreen(front_screen_root)
    front_screen_root.mainloop()

