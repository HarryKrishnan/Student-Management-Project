import os

file_path = r'c:\Users\Harikrishnan S\Desktop\Cymonic project\cymonic-project-v2\Student-Management-System\client\src\app\class-teacher-dashboard\class-teacher-dashboard.component.css'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the content
new_content = content.replace(
    '.teacher-dashboard-layout {\n  display: flex;\n  gap: 2rem;',
    '.teacher-dashboard-layout {\n  display: flex;\n  gap: 2rem;\n  padding: 2rem;'
)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Padding added successfully")
