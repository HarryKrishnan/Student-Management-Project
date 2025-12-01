import { Component, OnInit, AfterViewInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Chart, registerables } from 'chart.js/auto';
import { ApiService } from '../services/api.service';
import { interval, Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';

Chart.register(...registerables);

@Component({
  selector: 'app-student-dashboard',
  templateUrl: './student-dashboard.component.html',
  styleUrls: ['./student-dashboard.component.css'],
  standalone: true,
  imports: [CommonModule, FormsModule],
})
export class StudentDashboardComponent implements OnInit, AfterViewInit, OnDestroy {
  profile: any = null;
  attendance: any;
  allHomeworks: any[] = [];
  allMarks: any[] = [];
  allExams: any[] = [];
  examTypes: string[] = ['All', 'Unit Test 1', 'Unit Test 2', 'Mid Term', 'Unit Test 3', 'Final Exam'];
  selectedExam: string = 'All';
  displayedHomeworks: any[] = [];
  displayedMarks: any[] = [];
  displayedExams: any[] = [];
  displayedTeacherContact: any;
  subjectTeachers: any[] = [];
  classAdvisor: any;
  pastLeaveRequests: any[] = [];
  isLeaveModalOpen = false;
  isProfileModalOpen = false;
  attendanceChart: any;
  gradesChart: any;
  averageGrade = 0;
  schoolNews = 'Our vision is to foster a learning environment where every student can achieve their full potential. *** Upcoming: Parent-Teacher meetings next Tuesday. ***';

  leaveRequest = {
    reason: '',
    startDate: '',
    endDate: '',
    details: '',
  };

  private destroy$ = new Subject<void>();
  private refreshInterval = 10000; // ✅ REAL-TIME: Refresh every 10 seconds

  constructor(private api: ApiService) { }

  ngOnInit() {
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    if (!user?.id) return;

    // Load profile and basic data
    this.api.getStudentProfile(user.id).subscribe({
      next: (res) => {
        this.profile = {
          name: res.name,
          class: res.className,
          division: res.division,
          rollNo: res.id,
        };
      },
      error: (err) => console.error('❌ Profile API Error:', err),
    });



    // Load marks
    this.loadMarks(user.id);

    // Load leave requests with real-time polling
    this.loadLeaveHistory(user.id);

    this.loadStudentEvents(user.id);

    // Default mock data
    this.attendance = { present: 120, absent: 5 };
    this.classAdvisor = {
      title: 'Class Advisor',
      name: 'Mrs. Anita Sharma',
      email: 'anita.sharma@school.edu',
      mobile: '9876543210',
    };

    this.subjectTeachers = [
      { subject: 'Math', title: 'Math Teacher', name: 'Mr. Rajesh Kumar', email: 'rajesh.k@school.edu', mobile: '9876543211' },
      { subject: 'Science', title: 'Science Teacher', name: 'Ms. Priya Singh', email: 'priya.s@school.edu', mobile: '9876543212' },
      { subject: 'History', title: 'History Teacher', name: 'Mr. David Lee', email: 'david.l@school.edu', mobile: '9876543213' },
      { subject: 'English', title: 'English Teacher', name: 'Ms. Emily White', email: 'emily.w@school.edu', mobile: '9876543214' }
    ];

    this.displayedTeacherContact = this.classAdvisor;
    this.allHomeworks = [
      { subject: 'Math', title: 'Algebra II Worksheet', dueDate: '2025-11-01' },
      { subject: 'Science', title: 'Biology Lab Report', dueDate: '2025-11-05' },
      { subject: 'History', title: 'Renaissance Essay', dueDate: '2025-11-08' },
      { subject: 'Math', title: 'Geometry Proofs', dueDate: '2025-11-10' },
      { subject: 'English', title: 'To Kill a Mockingbird Quiz', dueDate: '2025-11-12' }
    ];

    // this.allMarks = [
    //   { subject: 'Math', score: 88 },
    //   { subject: 'Science', score: 92 },
    //   { subject: 'History', score: 78 },
    //   { subject: 'English', score: 85 }
    // ];

    this.filterDashboard();
    this.calculateAverageGrade();

    // 🔄 REAL-TIME POLLING: Auto-refresh leave requests and events every 10 seconds
    interval(this.refreshInterval)
      .pipe(takeUntil(this.destroy$))
      .subscribe(() => {
        console.log('🔄 Real-time sync: Refreshing data...');
        this.loadLeaveHistory(user.id);
        this.loadStudentEvents(user.id);
        this.loadMarks(user.id);
      });
  }

  loadMarks(studentId: number) {
    this.api.getMarksByStudent(studentId).subscribe({
      next: (res: any) => {
        // Handle paginated response or array
        const marks = Array.isArray(res) ? res : (res.results || []);

        this.allMarks = marks.map((m: any) => ({
          subject: m.subject,
          score: m.marks_obtained,
          examType: m.exam_type,
          total: m.total_marks,
          percentage: m.percentage
        }));

        console.log('✅ Marks loaded:', this.allMarks);
        this.filterDashboard();
      },
      error: (err) => console.error('❌ Marks load error:', err)
    });
  }

  loadLeaveHistory(studentId: number) {
    this.api.getLeaveHistory(studentId).subscribe({
      next: (res) => {
        this.pastLeaveRequests = Array.isArray(res) ? res : (res?.results || []);
        console.log('✅ Leave requests updated:', this.pastLeaveRequests);
      },
      error: (err) => console.error('❌ Leave load error', err),
    });
  }

  private loadStudentEvents(studentId: number) {
    // Load all events that are for 'ALL' audience (public events)
    this.api.getAllEvents().subscribe({
      next: (events) => {
        // Filter for public events or events specific to the student's class
        if (Array.isArray(events)) {
          this.allExams = events.map((e: any) => ({
            subject: 'Event',
            title: e.title,
            date: e.date,
            description: e.description || '',
            audience: e.audience
          }));
        } else {
          this.allExams = [];
        }
        console.log('✅ Events loaded:', this.allExams);
        this.filterDashboard();
      },
      error: (err) => {
        console.error("❌ Events load error:", err);
        this.allExams = [];
      }
    });
  }

  ngAfterViewInit() {
    this.createAttendanceChart();
    // Don't create grades chart here - it will be created after data loads in filterDashboard()
  }

  filterDashboard() {
    this.displayedHomeworks = this.allHomeworks;

    // Filter marks by Exam Type only
    this.displayedMarks = this.allMarks.filter((m) => {
      const examMatch = this.selectedExam === 'All' || m.examType === this.selectedExam;
      return examMatch;
    });

    this.displayedExams = [...this.allExams];
    // Always show Class Advisor since subject filter is removed
    this.displayedTeacherContact = this.classAdvisor;

    this.calculateAverageGrade();

    // Always recreate chart with filtered data
    this.createGradesChart(this.displayedMarks);
  }

  submitLeaveRequest() {
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    if (!user?.id) return;

    // Validate form
    if (!this.leaveRequest.reason || !this.leaveRequest.startDate || !this.leaveRequest.endDate) {
      alert('❌ Please fill in all required fields');
      return;
    }

    // Format the leave request payload
    const leavePayload = {
      student: user.id,
      reason: this.leaveRequest.reason,
      start_date: this.leaveRequest.startDate,
      end_date: this.leaveRequest.endDate,
      details: this.leaveRequest.details,
      status: 'Pending'
    };

    this.api.createLeave(leavePayload).subscribe({
      next: (response) => {
        alert('✅ Leave request submitted successfully');
        this.loadLeaveHistory(user.id);
        this.closeLeaveModal();
        this.leaveRequest = { reason: '', startDate: '', endDate: '', details: '' };
      },
      error: (err) => {
        console.error('❌ Error submitting leave:', err);
        alert('❌ Error submitting leave request. Please try again.');
      }
    });
  }

  openLeaveModal() { this.isLeaveModalOpen = true; }
  closeLeaveModal() { this.isLeaveModalOpen = false; }
  toggleProfileModal() { this.isProfileModalOpen = !this.isProfileModalOpen; }

  logout() {
    localStorage.removeItem('user');
    window.location.href = '/login';
  }

  calculateAverageGrade() {
    if (!this.displayedMarks.length) return;
    const sum = this.displayedMarks.reduce((a, b) => a + b.score, 0);
    this.averageGrade = sum / this.displayedMarks.length;
  }

  createAttendanceChart() {
    if (!this.attendance) return;
    const ctx = document.getElementById('attendancePieChart') as HTMLCanvasElement;
    if (!ctx) return;
    if (this.attendanceChart) this.attendanceChart.destroy();

    this.attendanceChart = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: ['Present', 'Absent'],
        datasets: [{
          data: [this.attendance.present, this.attendance.absent],
          backgroundColor: ['#68d3b1', '#fde8e8'],
          borderColor: '#ffffff',
          borderWidth: 4,
        }]
      },
      options: { responsive: true, maintainAspectRatio: false },
    });
  }

  createGradesChart(data: any[]) {
    console.log('📊 Creating grades chart with data:', data);

    if (!data || data.length === 0) {
      console.warn('⚠️ No data available for chart');
      return;
    }

    const ctx = document.getElementById('gradesBarChart') as HTMLCanvasElement;
    if (!ctx) {
      console.error('❌ Chart canvas element not found');
      return;
    }

    if (this.gradesChart) this.gradesChart.destroy();

    // Generate dynamic colors for each subject
    const generateColor = (index: number) => {
      const colors = [
        'rgba(138, 99, 210, 0.7)',   // Purple
        'rgba(104, 211, 177, 0.7)',  // Teal
        'rgba(255, 179, 102, 0.7)',  // Orange
        'rgba(130, 177, 255, 0.7)',  // Blue
        'rgba(255, 107, 129, 0.7)',  // Pink
        'rgba(255, 206, 84, 0.7)',   // Yellow
        'rgba(75, 192, 192, 0.7)',   // Cyan
        'rgba(153, 102, 255, 0.7)',  // Violet
      ];
      return colors[index % colors.length];
    };

    this.gradesChart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: data.map((m) => m.subject),
        datasets: [{
          label: 'Marks Obtained',
          data: data.map((m) => m.score),
          backgroundColor: data.map((_, index) => generateColor(index)),
          borderColor: data.map((_, index) => generateColor(index).replace('0.7', '1')),
          borderWidth: 2,
        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: true,
            position: 'top',
          },
          tooltip: {
            callbacks: {
              label: (context) => {
                const mark = data[context.dataIndex];
                return `Score: ${mark.score}/${mark.total || 100} (${mark.percentage?.toFixed(1) || ((mark.score / (mark.total || 100)) * 100).toFixed(1)}%)`;
              }
            }
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            max: 100,
            title: {
              display: true,
              text: 'Marks'
            }
          },
          x: {
            title: {
              display: true,
              text: 'Subjects'
            }
          }
        },
      }
    });

    console.log('✅ Chart created successfully');
  }

  ngOnDestroy() {
    this.destroy$.next();
    this.destroy$.complete();
  }
}
