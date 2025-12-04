import os

# Read the backup or reconstruct the exam marks section
file_path = r'c:\Users\Harikrishnan S\Desktop\Cymonic project\cymonic-project-v2\Student-Management-System\client\src\app\class-teacher-dashboard\class-teacher-dashboard.component.html'

# The exam marks section that should be inserted
exam_marks_section = '''    <!-- 👉 Exams/Marks -->
    <div *ngIf="currentView === 'exams'">
      <div class="exam-overview-panel">
        <h2>Student Marks - Subject Teacher Updates</h2>

        <div class="exam-filter">
          <label>Select Subject:</label>
          <select [(ngModel)]="selectedSubjectView">
            <option *ngFor="let subj of subjectList">{{ subj }}</option>
          </select>

          <label>Select Exam:</label>
          <select [(ngModel)]="selectedExamView">
            <option *ngFor="let exam of examTypes">{{ exam }}</option>
          </select>
        </div>

        <div *ngIf="filteredMarksData.length === 0" class="no-data-message">
          <p>No marks uploaded by subject teachers yet.</p>
        </div>

        <table class="marks-table" *ngIf="filteredMarksData.length > 0">
          <thead>
            <tr>
              <th>Roll No</th>
              <th>Student Name</th>
              <th>Subject</th>
              <th>Exam Type</th>
              <th>Marks</th>
              <th>Percentage</th>
              <th>Remarks</th>
            </tr>
          </thead>
          <tbody>
            <tr *ngFor="let mark of filteredMarksData">
              <td>{{ mark.student }}</td>
              <td>{{ mark.student_name }}</td>
              <td>{{ mark.subject }}</td>
              <td>{{ mark.exam_type }}</td>
              <td>{{ mark.marks_obtained }}/{{ mark.total_marks }}</td>
              <td>{{ mark.percentage | number: '1.0-2' }}%</td>
              <td>{{ mark.remarks || '-' }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 👉 Academic -->
    <div *ngIf="currentView === 'academic'">
      <h2>Academic Overview</h2>

'''

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find where to insert the exam marks section
# Look for the events section end and academic section start
events_end = content.find('    </div>\n\n          <label>Filter:</label>')

if events_end != -1:
    # Insert the exam marks section
    before = content[:events_end + len('    </div>\n\n')]
    after = content[events_end + len('    </div>\n\n'):]
    
    # Remove the misplaced academic section start
    after = after.replace('          <label>Filter:</label>', '      <div class="filter-box">\n        <label>Filter:</label>', 1)
    
    new_content = before + exam_marks_section + after
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("Exam marks section restored successfully")
else:
    print("Could not find insertion point")
