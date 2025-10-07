import google.generativeai as genai
import customtkinter as ctk
import threading

# Configure the API key
genai.configure(api_key="AIzaSyDSuS-sEPDkjGjcT6zD_kGdO-mvHQYBpsQ")

class ModernChatbotGUI:
    def __init__(self):
        ctk.set_appearance_mode("Light")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("Gemini Chatbot")
        self.root.geometry("700x800")  # Fixed: use 'x' not '*'

        self.model = genai.GenerativeModel("gemini-2.0-flash")
        self.setup_ui()

    def setup_ui(self):
        # Main Frame
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Title
        title_label = ctk.CTkLabel(
            main_frame,
            text="Gemini Chatbot",
            font=("Arial", 20, "bold")
        )
        title_label.pack(pady=10)

        # Chat Display area
        self.chat_frame = ctk.CTkScrollableFrame(
            main_frame,
            height=500  # Increased height for better visibility
        )
        self.chat_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Input area
        input_frame = ctk.CTkFrame(main_frame)
        input_frame.pack(fill="x", padx=20, pady=10)
        
        self.input_field = ctk.CTkEntry(
            input_frame,
            placeholder_text="Type your message here...",
            height=40,
            font=("Arial", 14)
        )
        self.input_field.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.input_field.bind("<Return>", self.send_message)
        
        self.send_button = ctk.CTkButton(
            input_frame,
            text="Send",
            command=self.send_message,
            height=40,
            width=80
        )
        self.send_button.pack(side="right")
        
        # Add welcome message
        self.add_message("Chatbot", "Hello! I'm your Gemini assistant. How can I help you today?")
    
    def add_message(self, sender, message):
        # Create a frame for each message
        message_frame = ctk.CTkFrame(self.chat_frame, fg_color="transparent")
        
        if sender == "You":
            # User messages - align to right with blue background
            message_frame.pack(anchor="e", fill="x", pady=5)
            text_color = "white"
            bg_color = "#2b5278"  # Blue color for user
            justify = "right"
        else:
            # Bot messages - align to left with gray background
            message_frame.pack(anchor="w", fill="x", pady=5)
            text_color = "white"
            bg_color = "#3d3d3d"  # Gray color for bot
            justify = "left"
        
        message_label = ctk.CTkLabel(
            message_frame,
            text=f"{sender}: {message}",
            wraplength=400,  # Adjusted for better wrapping
            justify=justify,
            font=("Arial", 12),
            text_color=text_color,
            fg_color=bg_color,
            corner_radius=10,
            padx=15,
            pady=10
        )
        
        if sender == "You":
            message_label.pack(padx=10, pady=5, anchor="e")
        else:
            message_label.pack(padx=10, pady=5, anchor="w")
        
        # Scroll to bottom
        self.chat_frame._parent_canvas.update_idletasks()
        self.chat_frame._parent_canvas.yview_moveto(1.0)
    
    def send_message(self, event=None):
        user_input = self.input_field.get().strip()
        if not user_input:
            return
        
        self.input_field.delete(0, "end")
        self.add_message("You", user_input)
        self.send_button.configure(state="disabled")
        
        threading.Thread(target=self.get_bot_response, args=(user_input,), daemon=True).start()
    
    def get_bot_response(self, user_input):
        try:
            response = self.model.generate_content(user_input)
            bot_reply = response.text.strip()
        except Exception as e:
            bot_reply = f"Error: {str(e)}"
        
        self.root.after(0, self.update_chat, bot_reply)
    
    def update_chat(self, bot_reply):
        self.add_message("Chatbot", bot_reply)
        self.send_button.configure(state="normal")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ModernChatbotGUI()
    app.run()