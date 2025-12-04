import os

file_path = r'c:\Users\Harikrishnan S\Desktop\Cymonic project\cymonic-project-v2\Student-Management-System\client\src\app\student-dashboard\student-dashboard.component.html'

# Read the file
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Remove lines 170-183 (0-indexed: 169-182)
new_lines = lines[:169] + lines[183:]

# Write back
with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Class Advisor block removed successfully")
