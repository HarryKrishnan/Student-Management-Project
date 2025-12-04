import re

file_path = r'c:\Users\Harikrishnan S\Desktop\Cymonic project\cymonic-project-v2\Student-Management-System\client\src\app\student-dashboard\student-dashboard.component.html'

# Read the file
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the assignment card section
old_pattern = r'<div class="assignment-list" \*ngIf="displayedHomeworks\.length > 0; else noHomework">\s*<div class="assignment-card" \*ngFor="let hw of displayedHomeworks">\s*<div class="icon-folder">📁</div>\s*<div class="assignment-details">\s*<h4>{{ hw\.title }}</h4>\s*<p>Due: <span>{{ hw\.dueDate \| date }}</span></p>\s*</div>\s*<span class="status-badge">To-Do</span>\s*</div>\s*</div>'

new_content = '''      <div class="assignment-list" *ngIf="displayedHomeworks.length > 0; else noHomework">
        <div class="assignment-card" *ngFor="let hw of displayedHomeworks" 
             (click)="toggleAssignmentDescription(hw.id)"
             [class.expanded]="expandedAssignmentId === hw.id">
          <div class="assignment-header">
            <div class="icon-folder">📁</div>
            <div class="assignment-details">
              <h4>{{ hw.title }}</h4>
              <p>Due: <span>{{ hw.dueDate | date }}</span></p>
            </div>
            <span class="status-badge">To-Do</span>
            <span class="expand-icon">{{ expandedAssignmentId === hw.id ? '▼' : '▶' }}</span>
          </div>
          <div class="assignment-description" *ngIf="expandedAssignmentId === hw.id && hw.description">
            <p>{{ hw.description }}</p>
          </div>
        </div>
      </div>'''

# Use regex to find and replace
content = re.sub(old_pattern, new_content, content, flags=re.DOTALL)

# Write back
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Assignment expandable description feature added successfully")
