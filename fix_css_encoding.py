import os

file_path = r'c:\Users\Harikrishnan S\Desktop\Cymonic project\cymonic-project-v2\Student-Management-System\client\src\app\student-dashboard\student-dashboard.component.css'

# CSS content to restore/append
css_content = """
/* ========== Expandable Assignment Cards ========== */
.assignment-card {
  cursor: pointer;
  transition: all 0.3s ease;
}

.assignment-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(138, 99, 210, 0.15);
}

.assignment-header {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.expand-icon {
  margin-left: auto;
  color: #8a63d2;
  font-size: 0.8rem;
  transition: transform 0.3s ease;
}

.assignment-card.expanded .expand-icon {
  transform: rotate(90deg);
}

.assignment-description {
  margin-top: 1rem;
  padding: 1rem;
  background: #f9f7ff;
  border-radius: 8px;
  border-left: 3px solid #8a63d2;
  animation: slideDown 0.3s ease;
}

.assignment-description p {
  margin: 0;
  color: #5a5a7d;
  line-height: 1.6;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
"""

# Read the file
with open(file_path, 'rb') as f:
    content = f.read()

# Remove null bytes
content = content.replace(b'\x00', b'')

# Decode
text_content = content.decode('utf-8', errors='ignore')

# Find where the corruption likely started (the comment I added)
# "/* ========== Expandable Assignment Cards ========== */"
# Or just look for the end of the valid content.
# The valid content ended around line 1533 before I appended.
# Let's just strip everything after the last closing brace of the previous section and append fresh.

# Find the last closing brace before my addition
# The previous section ended with:
# .resource-list {
#   grid-template-columns: 1fr;
# }
# }

# Let's try to find "grid-template-columns: 1fr;" and the closing braces
marker = "grid-template-columns: 1fr;"
idx = text_content.rfind(marker)

if idx != -1:
    # Find the next two closing braces
    end_idx = text_content.find('}', idx)
    end_idx = text_content.find('}', end_idx + 1)
    
    if end_idx != -1:
        # Keep content up to the second closing brace
        clean_text = text_content[:end_idx + 1]
        
        # Append new CSS
        final_content = clean_text + '\n' + css_content
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(final_content)
        
        print("CSS file fixed successfully")
    else:
        print("Could not find end of valid content")
else:
    # Fallback: just remove null bytes and write back, assuming that fixes it
    # But the appended content might be duplicated or messy
    # Let's try to just write the cleaned content if we can't find the marker
    # But better to be safe.
    
    # Let's just write the cleaned content for now, it should be valid CSS if nulls are removed
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(text_content)
    print("CSS file cleaned (null bytes removed)")
