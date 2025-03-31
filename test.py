import os
from ics import Calendar

# Get the root directory based on the location of this script
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TMP_FOLDER = os.path.join(ROOT_DIR, "tmp")

def preview_ics_files():
    if not os.path.exists(TMP_FOLDER):
        print(f"❌ 'tmp/' folder not found at {TMP_FOLDER}")
        return

    for filename in os.listdir(TMP_FOLDER):
        if filename.endswith(".ics"):
            filepath = os.path.join(TMP_FOLDER, filename)
            print(f"\n🔍 Previewing: {filename}\n{'-' * 40}")
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                    calendar = Calendar(content)
                    print(calendar.serialize())
            except Exception as e:
                print(f"❌ Error reading {filename}: {e}")

if __name__ == "__main__":
    preview_ics_files()
