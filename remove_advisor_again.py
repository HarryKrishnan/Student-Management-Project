import re

file_path = r'c:\Users\Harikrishnan S\Desktop\Cymonic project\cymonic-project-v2\Student-Management-System\client\src\app\student-dashboard\student-dashboard.component.html'

# Read the file
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Regex to remove the Teacher Contact Widget block
# It starts with <!-- Teacher Contact Widget --> and ends with the closing div of the widget (line 191)
# The block looks like:
#     <!-- Teacher Contact Widget -->
#     <div class="widget teacher-contact" *ngIf="displayedTeacherContact">
#       ...
#     </div>

pattern = r'<!-- Teacher Contact Widget -->\s*<div class="widget teacher-contact" \*ngIf="displayedTeacherContact">.*?</div>\s*</div>\s*</div>'
# Wait, the closing div is indented.
# Let's use a simpler string replacement if possible, or a more robust regex.
# Since I know the exact lines from view_file, I can construct the string to replace.

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
    </div>"""

# Normalize line endings and whitespace for matching
# But exact string match is risky if whitespace differs slightly.
# Let's use regex with DOTALL.

pattern = r'<!-- Teacher Contact Widget -->\s*<div class="widget teacher-contact".*?</div>\s*</div>\s*</div>'
# The last div closes .contact-card, then .widget teacher-contact.
# Wait, structure:
# <div class="widget teacher-contact">
#   <h3>...</h3>
#   <div class="contact-card">
#     ...
#   </div>
# </div>

# So it ends with </div> </div> (two closing divs after content).
# My regex: .*?</div>\s*</div> matches until the first </div> then another </div>.
# This should work if non-greedy matches the inner content.

pattern = r'<!-- Teacher Contact Widget -->\s*<div class="widget teacher-contact".*?</div>\s*</div>'
# This matches:
# <div class="widget teacher-contact"> ... </div> (inner) ... </div> (outer)
# Wait, regex is tricky with nested divs.
# Let's use the line range if I can trust it won't change.
# But I'll use a slightly more specific regex.

pattern = r'<!-- Teacher Contact Widget -->\s*<div class="widget teacher-contact" \*ngIf="displayedTeacherContact">[\s\S]*?</div>\s*</div>'
# [\s\S]*? matches any character including newlines, non-greedy.
# It will stop at the first </div>\s*</div> sequence.
# Inside:
#   <div class="contact-card"> ... </div>
# So we have one </div> inside.
# The regex will match until the FIRST occurrence of </div>\s*</div>.
# "</div>\n    </div>" matches the end of contact-card and end of widget?
# No, contact-card ends with </div>. Then widget ends with </div>.
# So yes, it should match the end of the widget.

content = re.sub(pattern, '', content)

# Write back
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Class Advisor block removed successfully")
