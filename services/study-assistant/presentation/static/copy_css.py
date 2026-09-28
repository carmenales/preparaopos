import shutil
import os

src = r"c:\repositories\preparaopos\apps\studyassistant\assets\styles.css"
dst_dir = r"c:\repositories\preparaopos\services\study-assistant\presentation\static\css"
dst = os.path.join(dst_dir, "styles.css")

os.makedirs(dst_dir, exist_ok=True)
shutil.copy2(src, dst)
print("CSS copied successfully.")
