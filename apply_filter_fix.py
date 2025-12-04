import os

file_path = r'c:\Users\Harikrishnan S\Desktop\Cymonic project\cymonic-project-v2\Student-Management-System\client\src\app\class-teacher-dashboard\class-teacher-dashboard.component.html'

# Read the file
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Simple replacements
content = content.replace('*ngIf="marksData.length === 0"', '*ngIf="filteredMarksData.length === 0"')
content = content.replace('*ngIf="marksData.length > 0"', '*ngIf="filteredMarksData.length > 0"')
content = content.replace('*ngFor="let mark of marksData"', '*ngFor="let mark of filteredMarksData"')
content = content.replace('No marks uploaded by subject teachers yet.', 'No marks found for the selected filters.')

# Write back
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Exam marks filter implemented successfully")
