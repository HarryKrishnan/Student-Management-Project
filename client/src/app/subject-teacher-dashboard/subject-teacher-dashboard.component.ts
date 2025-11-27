import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { ApiService } from '../services/api.service';

@Component({
  selector: 'app-subject-teacher-dashboard',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './subject-teacher-dashboard.component.html',
  styleUrls: ['./subject-teacher-dashboard.component.css']
})
export class SubjectTeacherDashboardComponent implements OnInit {

  constructor(
    private router: Router,
    private apiService: ApiService
  ) { }

  isLoading = false;
  errorMessage = '';
  teacherId: number | null = null;

  /* Teacher Info */
  teacherName = '';
  subjectName = '';
  teacherProfile: any = {};

  /* Class Switching */
  classList: any[] = [];
  currentClass: any = null;
  currentClassId: number | null = null;

  /* KPI */
  totalStudents = 0;
  pendingAssignments = 0;
  averageMarks = 0;

  /* Exam Dropdown */
  examTypes = ['Unit Test 1', 'Unit Test 2', 'Mid Term', 'Unit Test 3', 'Final Exam'];
  selectedExam = 'Unit Test 1';
  isDropdownOpen = false;

  /* Students Marks */
  students: any[] = [];

  /* Assignments */
  newAssignment: any = { title: '', dueDate: '', description: '' };
  assignments: any[] = [];

  /* Resources */
  newResource: any = { title: '', link: '' };
  resources: any[] = [];

  ngOnInit() {
    const userStr = localStorage.getItem('user');
    if (userStr) {
      const user = JSON.parse(userStr);
      this.teacherId = user.id;
      this.teacherName = user.name;
      this.loadDashboardData();
    } else {
      this.router.navigate(['/login']);
    }
  }

  loadDashboardData(classId?: number) {
    if (!this.teacherId) return;

    this.isLoading = true;
    this.errorMessage = '';

    this.apiService.getSubjectTeacherDashboard(this.teacherId, classId).subscribe({
      next: (data) => {
        this.teacherProfile = data.teacher;
        this.teacherName = data.teacher.name;
        this.classList = data.classes;

        if (data.current_class) {
          this.currentClass = data.current_class;
          this.currentClassId = data.current_class.id;
          this.subjectName = data.current_class.subject;

          // Map students and merge with marks
          this.processStudentsAndMarks(data.students, data.marks);
        } else {
          this.currentClass = null;
          this.students = [];
        }

        this.isLoading = false;
      },
      error: (err) => {
        console.error('Error loading dashboard:', err);
        this.errorMessage = 'Failed to load dashboard data. Please try again.';
        this.isLoading = false;
      }
    });
  }

  processStudentsAndMarks(students: any[], marks: any[]) {
    this.students = students.map(student => {
      // Find marks for this student and current exam
      const studentMark = marks.find(m =>
        m.student === student.id &&
        m.exam_type === this.selectedExam
      );

      return {
        id: student.id,
        rollNo: student.id, // Using ID as roll no for now
        name: student.name,
        email: student.email,
        examMarks: studentMark ? studentMark.marks_obtained : null,
        markId: studentMark ? studentMark.id : null,
        assignmentMarks: 0 // Placeholder as we don't have assignment marks in DB yet
      };
    });

    this.totalStudents = this.students.length;

    // Calculate average
    const marksList = this.students
      .filter(s => s.examMarks !== null)
      .map(s => s.examMarks);

    if (marksList.length > 0) {
      this.averageMarks = Math.round(marksList.reduce((a, b) => a + b, 0) / marksList.length);
    } else {
      this.averageMarks = 0;
    }
  }

  /* ✅ Top Right Logout */
  logout() {
    localStorage.clear();
    sessionStorage.clear();
    this.router.navigate(['/login']);
  }

  /* ✅ View Control */
  currentView = 'overview';
  setView(view: string) { this.currentView = view; }

  /* ✅ Class Switching */
  switchClass(classId: any) {
    // Handle both object (from ngValue) and string/number (from value)
    const id = typeof classId === 'object' ? classId.id : classId;
    this.loadDashboardData(id);
  }

  toggleDropdown() { this.isDropdownOpen = !this.isDropdownOpen; }

  selectExam(exam: string) {
    this.selectedExam = exam;
    this.isDropdownOpen = false;
    // Reload data to refresh marks for selected exam
    if (this.currentClassId) {
      this.loadDashboardData(this.currentClassId);
    }
  }

  updateMarks(student: any) {
    if (student.examMarks === null || student.examMarks === undefined) return;

    const marksData = {
      student: student.id,
      teacher: this.teacherId,
      subject: this.subjectName,
      class_name: this.currentClass.class_number,
      division: this.currentClass.division,
      exam_type: this.selectedExam,
      marks_obtained: student.examMarks,
      total_marks: 100
    };

    if (student.markId) {
      // Update existing mark
      this.apiService.updateMarks(student.markId, marksData).subscribe({
        next: (res) => {
          alert(`✅ Marks updated for ${student.name}`);
        },
        error: (err) => {
          console.error('Error updating marks:', err);
          alert('❌ Failed to update marks');
        }
      });
    } else {
      // Create new mark
      this.apiService.createMarks(marksData).subscribe({
        next: (res) => {
          student.markId = res.id; // Save the new mark ID
          alert(`✅ Marks saved for ${student.name}`);
        },
        error: (err) => {
          console.error('Error saving marks:', err);
          alert('❌ Failed to save marks');
        }
      });
    }
  }

  /* Assignments - Placeholder for now as backend doesn't have Assignment model fully integrated yet */
  addAssignment() {
    if (!this.newAssignment.title) return;
    this.assignments.push({ ...this.newAssignment, status: 'Pending' });
    this.newAssignment = { title: '', dueDate: '', description: '' };
  }

  editAssignment(a: any) {
    alert('✏️ Assignment editing coming soon!');
  }

  deleteAssignment(a: any) {
    this.assignments = this.assignments.filter(x => x !== a);
  }

  /* Resources - Placeholder */
  addResource() {
    if (!this.newResource.title || !this.newResource.link) return;
    this.resources.push({ ...this.newResource });
    this.newResource = { title: '', link: '' };
  }
}
