import os

file_path = r'c:\Users\Harikrishnan S\Desktop\Cymonic project\cymonic-project-v2\Student-Management-System\client\src\app\class-teacher-dashboard\class-teacher-dashboard.component.css'

# CSS content to append
css_content = """
/* ========== Status Badges ========== */
.status-badge {
  display: inline-block;
  padding: 0.4rem 0.9rem;
  border-radius: 20px;
  font-weight: 600;
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.status-pending {
  background: #fff3cd;
  color: #856404;
  border: 1px solid #ffeaa7;
}

.status-approved {
  background: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.status-rejected {
  background: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

/* ========== Events Management Styling ========== */
.subtitle {
  color: #7b7a92;
  font-size: 0.95rem;
  margin-bottom: 1.5rem;
}

.event-form-card {
  background: #faf9ff;
  border-radius: 16px;
  padding: 1.8rem;
  margin-bottom: 2rem;
  border: 1px solid #e8e3f6;
}

.event-form-card h3 {
  color: #8a63d2;
  font-size: 1.2rem;
  margin-bottom: 1.2rem;
  margin-top: 0;
}

.event-form {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.2rem;
}

.event-form .form-group {
  display: flex;
  flex-direction: column;
}

.event-form .form-group label {
  font-weight: 600;
  color: #4a4762;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

.event-form .form-group input {
  padding: 0.8rem 1rem;
  border-radius: 10px;
  border: 1px solid #d1c7f3;
  background: #ffffff;
  transition: all 0.3s ease;
}

.event-form .form-group input:focus {
  border-color: #8a63d2;
  box-shadow: 0 0 0 3px rgba(138, 99, 210, 0.15);
  outline: none;
}

.add-event-btn {
  grid-column: 1 / -1;
  background: linear-gradient(135deg, #8a63d2 0%, #a47ee8 100%);
  color: white;
  border: none;
  border-radius: 12px;
  padding: 0.9rem 1.5rem;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(138, 99, 210, 0.3);
}

.add-event-btn:hover {
  background: linear-gradient(135deg, #714dbf 0%, #8a63d2 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(138, 99, 210, 0.4);
}

.events-list-card {
  background: #ffffff;
  border-radius: 16px;
  padding: 1.8rem;
  border: 1px solid #e8e3f6;
}

.events-list-card h3 {
  color: #8a63d2;
  font-size: 1.2rem;
  margin-bottom: 1.2rem;
  margin-top: 0;
}

.events-table {
  width: 100%;
  border-collapse: collapse;
}

.events-table th,
.events-table td {
  padding: 14px 12px;
  border-bottom: 1px solid #eee;
  text-align: left;
}

.events-table th {
  color: #8a63d2;
  font-weight: 600;
  background-color: #faf9ff;
}

.events-table tr:hover td {
  background-color: #f9f7ff;
}

.delete-event-btn {
  background: linear-gradient(135deg, #e57373 0%, #f48fb1 100%);
  color: white;
  border: none;
  border-radius: 8px;
  padding: 0.6rem 1rem;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(229, 115, 115, 0.3);
}

.delete-event-btn:hover {
  background: linear-gradient(135deg, #d85c5c 0%, #e57373 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(229, 115, 115, 0.4);
}

.empty-message {
  text-align: center;
  padding: 2.5rem;
  color: #9e9eb9;
  font-style: italic;
  background: #f9f7ff;
  border-radius: 12px;
  border: 1px dashed #d1c7f3;
}
"""

# Read the file
with open(file_path, 'rb') as f:
    content = f.read()

# Remove null bytes just in case
content = content.replace(b'\x00', b'')

# Decode to string (ignoring errors to be safe)
text_content = content.decode('utf-8', errors='ignore')

# Split lines and keep only up to line 1010
lines = text_content.splitlines()
clean_lines = lines[:1010]

# Join back
clean_text = '\n'.join(clean_lines)

# Append new CSS
final_content = clean_text + '\n' + css_content

# Write back to file in UTF-8
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(final_content)

print("CSS file fixed and appended successfully")
