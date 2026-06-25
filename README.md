# cypy

<p align="center">
  <img src="assets/favicon.png" width="128" alt="cypy Logo" />
</p>

cypy is a lightweight, high-performance command-line (CLI) manga translator. It uses YOLOv8 to locate speech bubbles and the Google Gemini API to translate Japanese/foreign text into Indonesian while keeping the artwork clean and text typography perfectly fitted.

---

## ⚡ Key Highlights (v0.2502)

- **Zero-Setup Startup:** No need to manually configure files. If `.env` is missing or empty, `cypy` prompts you for your Gemini API key directly in the CLI and generates the `.env` file automatically.
- **Auto Desktop Shortcut:** Double-clicking the compiled `cypy.exe` automatically places a custom-rounded desktop shortcut on your Windows desktop on the first run.
- **Dynamic Model Switching:** Switch Gemini models (e.g., to `gemini-2.5-pro` or stable releases) directly via the `.env` file without recompiling the application.
- **Instant Startup (`--onedir`):** Built as a portable directory package. Opens instantly, saves RAM/CPU, and prevents SSD wear by avoiding background temp extraction.

---

## 📸 Comparison

| Before (Original Chinese / Japanese / Other) | After (Translated Indonesian) |
| :---: | :---: |
| ![Original Manga Page](assets/before.jpg) | ![Translated Indonesian Manga Page](assets/after.png) |

---

## 🛠️ Installation & Usage

### Method 1: Standalone Release (For Users)

1. Download and extract the latest `.zip` from [Releases](https://github.com/indravoyager/cypy/releases).
2. Run the executable:
   - **Windows:** Double-click `cypy.exe` (a desktop shortcut will be created automatically).
   - **Linux / macOS:** Run `chmod +x cypy && ./cypy`.
3. If it's your first run, paste your Gemini API key in the terminal when prompted.

### Method 2: From Source (For Developers)

1. Clone the repository and navigate inside:
   ```bash
   git clone https://github.com/indravoyager/cypy.git && cd cypy
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux / macOS
   source venv/bin/activate
   ```
3. Install the package in editable mode:
   ```bash
   pip install -e .
   ```
4. Run the translator:
   ```bash
   cypy
   ```

---

## ⚙️ Configuration (`.env`)

You can customize your translation settings inside the `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key_here
MODEL_GEMINI=gemini-3.1-flash-lite-preview
```

- **`GEMINI_API_KEY`**: Your Google AI Studio API key.
- **`MODEL_GEMINI`**: The Gemini model used for translation. Switch this to any valid model (like `gemini-2.5-pro`) to change behavior instantly.

*Note: More advanced layout settings (margins, font scales) can be adjusted inside [cypy/core/config.py](cypy/core/config.py).*

---

## 📂 Project Structure

```text
cypy/
├── assets/              # Model weights (eyecyre.pt), font, and favicon icons
├── cypy/                # Main Python package
│   ├── app.py           # Entrypoint loop & CLI logic
│   ├── __main__.py      # Package executor
│   └── core/            # Engine modules
│       ├── config.py    # Paths and image processing configs
│       ├── translator.py# YOLO detection & Gemini orchestration
│       └── utils.py     # Image filtering, masking, and shortcut creator
├── cypy_cache/          # Stale/temporary drafts cache (Git ignored)
├── pyproject.toml       # Python package configuration
└── README.md
```

---

## 📄 License

Distributed under the [MIT License](LICENSE).
