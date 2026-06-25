import os
from ultralytics import YOLO
from cypy.core.config import MODEL_YOLO, FONT_MANGA
from cypy.core.translator import proses_satu_gambar, mulai_ritual_pdf
from cypy.core.utils import create_shortcut_if_first_run


def main():
    # Automatically create desktop shortcut on first run (Windows only)
    create_shortcut_if_first_run()

    print("CYPY - Manga Translator")
    print("Ready to translate~ (✿◠‿◠)")

    # Check and request API Key if missing or empty
    import cypy.core.config as config
    if not config.GEMINI_API_KEY:
        print("\n[!] Google Gemini API Key is missing or empty!")
        print("You can get a free API Key from: https://aistudio.google.com/")
        user_key = input("Please paste your Gemini API Key here: ").strip()
        
        while not user_key:
            user_key = input("API Key cannot be empty. Please paste your Gemini API Key: ").strip()
            
        # Save to .env file in ROOT_DIR
        env_path = os.path.join(config.ROOT_DIR, ".env")
        try:
            with open(env_path, "w", encoding="utf-8") as f:
                f.write(f"GEMINI_API_KEY={user_key}\n")
                f.write("MODEL_GEMINI=gemini-3.1-flash-lite-preview\n")
            print(f"[+] API Key and default model successfully saved to: {env_path} (✿◠‿◠)")
            
            # Update running configuration in memory
            config.GEMINI_API_KEY = user_key
            os.environ["GEMINI_API_KEY"] = user_key
            
            # Dynamically update the imported key in the translator namespace
            import cypy.core.translator as translator
            translator.GEMINI_API_KEY = user_key
        except Exception as e:
            print(f"[!] Warning: Failed to save API Key to .env file: {e}")
            # Still update in memory so they can run this session
            config.GEMINI_API_KEY = user_key
            os.environ["GEMINI_API_KEY"] = user_key
            import cypy.core.translator as translator
            translator.GEMINI_API_KEY = user_key

    if not os.path.exists(MODEL_YOLO):
        print("[!] Model file not found.")
        raise SystemExit

    if not os.path.exists(FONT_MANGA):
        print("[!] Font file not found (will fallback to default).")

    yolo_model = YOLO(MODEL_YOLO)

    while True:
        try:
            raw_input = input("\nDrag-and-drop image/PDF here (or 'stop'): ")
            input_file = raw_input.strip("\"'& ")

            if input_file.lower() == "stop":
                print("Goodbye~ ♪")
                break

            if not input_file:
                continue

            if os.path.exists(input_file):
                if input_file.lower().endswith(".pdf"):
                    mulai_ritual_pdf(input_file, yolo_model)

                elif input_file.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
                    hasil = proses_satu_gambar(input_file, yolo_model)

                    if hasil:
                        print(f"Done! Saved at: {hasil}")

                else:
                    print("[!] Unsupported format. Please give me PNG, JPG, JPEG, WEBP, or PDF~")

            else:
                print("[!] File not found.")

        except Exception as e:
            print(f"[!] An error occurred: {e}")


if __name__ == "__main__":
    main()
