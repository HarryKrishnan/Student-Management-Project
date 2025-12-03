import os

file_path = r'c:\Users\Harikrishnan S\Desktop\Cymonic project\cymonic-project-v2\Student-Management-System\client\src\app\class-teacher-dashboard\class-teacher-dashboard.component.css'

# CSS content to append
css_content = """
/* ========== Global Heading Styling ========== */
.teacher-content-area h2 {
  text-align: center;
  padding-bottom: 1rem;
  margin-bottom: 2rem; /* Increased spacing */
  color: #8a63d2;
  border-bottom: 2px solid #e8e3f6;
  width: 100%; /* Ensure full width for centering */
}

/* Ensure subtitle is also centered if present */
.subtitle {
  text-align: center;
  margin-top: -1.5rem; /* Pull closer to the heading */
  margin-bottom: 2rem;
  display: block;
}
"""

# Read the file
with open(file_path, 'rb') as f:
    content = f.read()

# Remove null bytes just in case
content = content.replace(b'\x00', b'')

# Decode to string (ignoring errors to be safe)
text_content = content.decode('utf-8', errors='ignore')

# Append new CSS
final_content = text_content + '\n' + css_content

# Write back to file in UTF-8
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(final_content)

print("Headings centered and spaced successfully")
