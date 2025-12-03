import os

file_path = r'c:\Users\Harikrishnan S\Desktop\Cymonic project\cymonic-project-v2\Student-Management-System\client\src\app\class-teacher-dashboard\class-teacher-dashboard.component.css'

# CSS content to append
css_content = """
.event-management-panel h2 {
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #e8e3f6; /* Ensure the line is visible and spaced */
}
"""

# Read the file
with open(file_path, 'rb') as f:
    content = f.read()

# Remove null bytes just in case
content = content.replace(b'\x00', b'')

# Decode to string (ignoring errors to be safe)
text_content = content.decode('utf-8', errors='ignore')

# Split lines and keep only up to line 1186 (before the corruption)
lines = text_content.splitlines()
clean_lines = lines[:1186]

# Join back
clean_text = '\n'.join(clean_lines)

# Append new CSS
final_content = clean_text + '\n' + css_content

# Write back to file in UTF-8
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(final_content)

print("CSS file fixed and spacing added successfully")
