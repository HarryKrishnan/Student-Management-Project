import os

file_path = r'c:\Users\Harikrishnan S\Desktop\Cymonic project\cymonic-project-v2\Student-Management-System\client\src\app\subject-teacher-dashboard\subject-teacher-dashboard.component.css'

# CSS content to append
css_content = """
/* ===============================
   PROFILE STYLES
=============================== */
.sidebar-footer {
  padding: 1rem;
  border-top: 1px solid #f0eefc;
  margin-top: auto;
}

.profile-link {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 0.9rem 1.2rem;
  background: #f8f6ff;
  color: #8a63d2;
  font-weight: 600;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
  border: 1px solid #e8e3f6;
}

.profile-link:hover,
.profile-link.active {
  background: #8a63d2;
  color: white;
  box-shadow: 0 4px 12px rgba(138, 99, 210, 0.3);
  transform: translateY(-2px);
}

.profile-panel {
  background: #ffffff;
  border-radius: 20px;
  padding: 2.5rem;
  box-shadow: 0 4px 20px rgba(138, 99, 210, 0.08);
  border: 1px solid #f0eefc;
  max-width: 600px;
  margin: 0 auto;
  animation: fadeIn 0.4s ease-in;
}

.profile-panel h2 {
  color: #8a63d2;
  font-size: 1.8rem;
  margin-bottom: 2rem;
  border-bottom: 2px solid #f0eefc;
  padding-bottom: 1rem;
  text-align: center;
}

.profile-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 0;
  border-bottom: 1px solid #f9f7ff;
  font-size: 1.05rem;
}

.profile-row:last-child {
  border-bottom: none;
}

.profile-row strong {
  color: #5a5a7d;
  font-weight: 600;
  width: 150px;
}
"""

# Read the file
with open(file_path, 'rb') as f:
    content = f.read()

# Remove null bytes just in case
content = content.replace(b'\x00', b'')

# Decode to string (ignoring errors to be safe)
text_content = content.decode('utf-8', errors='ignore')

# Split lines and keep only up to line 454 (before the corruption)
lines = text_content.splitlines()
clean_lines = lines[:454]

# Join back
clean_text = '\n'.join(clean_lines)

# Append new CSS
final_content = clean_text + '\n' + css_content

# Write back to file in UTF-8
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(final_content)

print("Subject teacher CSS fixed and profile styles added successfully")
