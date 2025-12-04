import os

file_path = r'c:\Users\Harikrishnan S\Desktop\Cymonic project\cymonic-project-v2\Student-Management-System\client\src\app\student-dashboard\student-dashboard.component.html'

# Exact block to remove
block_to_remove = """    <!-- Teacher Contact Widget -->
    <div class="widget teacher-contact" *ngIf="displayedTeacherContact">
      <h3>{{ displayedTeacherContact.title }}</h3>
      <div class="contact-card">
        <div class="contact-icon">👨‍🏫</div>
        <div class="contact-details">
          <h4>{{ displayedTeacherContact.name }}</h4>
          <p><span class="icon">✉️</span> <a [href]="'mailto:' + displayedTeacherContact.email">{{
              displayedTeacherContact.email }}</a></p>
          <p><span class="icon">📞</span> <a [href]="'tel:' + displayedTeacherContact.mobile">{{
              displayedTeacherContact.mobile }}</a></p>
        </div>
      </div>
    </div>
"""

# Read the file
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace
if block_to_remove in content:
    content = content.replace(block_to_remove, '')
    print("Block removed successfully")
else:
    # Try with different line endings or whitespace if exact match fails
    # But since I copied from view_file, it should match if view_file is accurate.
    # Let's try to normalize newlines just in case.
    print("Exact match failed, trying normalized match")
    
    # Normalize content and block
    # This is complex without regex.
    # Let's try to just find the start and end.
    start_marker = '<!-- Teacher Contact Widget -->'
    end_marker = '</div>\n    </div>' # The last closing divs
    
    start_idx = content.find(start_marker)
    if start_idx != -1:
        # Find the end of the widget
        # It ends with </div> (indent 4) </div> (indent 4) ?
        # No, indent 4 for widget div.
        # Line 191:     </div>
        # Line 192: 
        
        # Let's look for the next widget start "<!-- Events List -->"
        next_widget_idx = content.find('<!-- Events List -->', start_idx)
        
        if next_widget_idx != -1:
            # Remove everything between start_marker and next_widget_idx
            # But keep one newline maybe?
            # The structure is:
            # ...
            # </div>
            # 
            # <!-- Teacher Contact Widget -->
            # ...
            # </div>
            # 
            # <!-- Events List -->
            
            # We want to remove from start_marker up to (but not including) <!-- Events List -->
            # And maybe the preceding newline if we want to be clean.
            
            # Let's just remove from start_marker to next_widget_idx
            content = content[:start_idx] + content[next_widget_idx:]
            print("Block removed using markers")
        else:
            print("Could not find next widget marker")
    else:
        print("Could not find start marker")

# Write back
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
