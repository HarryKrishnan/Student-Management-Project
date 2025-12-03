import os

file_path = r'c:\Users\Harikrishnan S\Desktop\Cymonic project\cymonic-project-v2\Student-Management-System\client\src\app\class-teacher-dashboard\class-teacher-dashboard.component.css'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the content to add box-sizing
new_content = content.replace(
    '.roster-search input {\n  width: 100%;\n  padding: 1rem 1.2rem;',
    '.roster-search input {\n  width: 100%;\n  box-sizing: border-box; /* Fix overflow */\n  padding: 1rem 1.2rem;'
)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Search bar alignment fixed successfully")
