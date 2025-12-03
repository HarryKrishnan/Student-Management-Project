import codecs

# Read the file and remove null bytes
with open(r'c:\Users\Harikrishnan S\Desktop\Cymonic project\cymonic-project-v2\Student-Management-System\client\src\app\class-teacher-dashboard\class-teacher-dashboard.component.css', 'rb') as f:
    content = f.read()

# Remove null bytes
clean_content = content.replace(b'\x00', b'')

# Find where the corruption starts (after line 1010)
lines = clean_content.split(b'\r\n')
clean_lines = lines[:1010]  # Keep only first 1010 lines

# Write back clean content
with open(r'c:\Users\Harikrishnan S\Desktop\Cymonic project\cymonic-project-v2\Student-Management-System\client\src\app\class-teacher-dashboard\class-teacher-dashboard.component.css', 'wb') as f:
    f.write(b'\r\n'.join(clean_lines))

print("CSS file cleaned successfully")
