import tkinter as tk

#settings
mode = None
crntScreen = None
screens = {}
visitedScreens = []

# Colors and styles
BG_COLOR = "#2E2E2E"  # Dark grey
FG_COLOR = "#FFFFFF"  # White
BUTTON_COLOR = "#404040"  # Slightly lighter grey for buttons
TEXT_COLOR = "#FFFFFF"  # White text for text area and input field

BUTTON_STYLE = {
    "bg": BUTTON_COLOR,  # Background color
    "fg": FG_COLOR,  # Text color
    "activebackground": "#505050",  # Background color when clicked
    "activeforeground": FG_COLOR,  # Text color when clicked
}

#screens
def show_screen(screen_name):
    global crntScreen

    #If switching to a new screen add previous to visitedScreens
    if crntScreen and (not visitedScreens or visitedScreens[-1] != crntScreen):
        visitedScreens.append(crntScreen)

    #Hide old screen
    if crntScreen:
        for widget in screens[crntScreen]:
            if hasattr(widget, "pack_info"):
                widget.pack_forget()
            else:
                widget.grid_forget()

    #Display new screen
    crntScreen = screen_name
    for widget in screens[crntScreen]:
        if crntScreen == "main":
            widget.pack(expand=True, fill="both")
        else:
            widget.grid(row=0, column=0, sticky="nsew")

def go_back():
    if visitedScreens:
        lastScreen = visitedScreens.pop() 
        show_screen(lastScreen)

def set_mode(modeType):
    global mode
    mode = modeType
    print(f"Mode set to: {mode}")
    show_screen("terminalDiagnostics")

#window innit
window = tk.Tk()
window.geometry("800x600") #why are there numbers in strings >:(
window.title("SSH_Debuger")
window.config(bg=BG_COLOR)

window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

# --- Define Screens --- #
#main
btnClient = tk.Button(window, text="Using Server (Linux)", font=('Arial', 18), **BUTTON_STYLE, command=lambda: set_mode("server"))
btnServer = tk.Button(window, text="Using Client (Windows)", font=('Arial', 18), **BUTTON_STYLE, command=lambda: set_mode("client"))
btnClient.pack(pady=10)
btnServer.pack(pady=10)
screens["main"] = [btnClient, btnServer]

#terminal and buttons
terminalFrame = tk.Frame(window, bg=BG_COLOR)
# Configure frame grid layout
terminalFrame.grid_rowconfigure(0, weight=1)
terminalFrame.grid_rowconfigure(1, weight=1)
terminalFrame.grid_rowconfigure(2, weight=0)
terminalFrame.grid_columnconfigure(0, weight=0)
terminalFrame.grid_columnconfigure(1, weight=1)

btn1 = tk.Button(terminalFrame, text="Run Command", font=('Arial', 14), **BUTTON_STYLE)
btn2 = tk.Button(terminalFrame, text="Clear", font=('Arial', 14), **BUTTON_STYLE)
btn3 = tk.Button(terminalFrame, text="Exit", font=('Arial', 14), **BUTTON_STYLE,command=go_back)
text_area = tk.Text(terminalFrame, font=('Arial', 12), bg=BG_COLOR, fg=FG_COLOR, insertbackground=FG_COLOR)
input_field = tk.Entry(terminalFrame, font=('Arial', 12), bg=BG_COLOR, fg=FG_COLOR, insertbackground=FG_COLOR)

text_area.config(state="disabled")
btn1.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
btn2.grid(row=1, column=0, sticky="nsew", padx=2, pady=2)
btn3.grid(row=2, column=0, sticky="nsew", padx=2, pady=2)
text_area.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=5, pady=5)
input_field.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

screens["terminalDiagnostics"] = [terminalFrame]
# --- Define Screens --- #

# Start with Main Screen
show_screen("main")

window.mainloop()