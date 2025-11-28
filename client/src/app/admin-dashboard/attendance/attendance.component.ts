import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-attendance',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './attendance.component.html',
  styleUrls: ['./attendance.component.css']
})
export class AttendanceComponent implements OnInit {

  allClasses: any[] = [];
  selectedClassId: number | null = null;
  selectedDate: string = new Date().toISOString().split('T')[0];

  classStudents: any[] = [];
  attendanceMap: { [studentId: number]: 'Present' | 'Absent' } = {};
  existingAttendance: any[] = [];

  // History
  attendanceHistory: any[] = [];
  historyDateFrom: string = '';
  historyDateTo: string = '';

  constructor(private api: ApiService) { }

  ngOnInit(): void {
    this.loadClasses();
  }

  loadClasses() {
    this.api.getAllClasses().subscribe({
      next: (res: any) => {
        this.allClasses = Array.isArray(res) ? res : (res.results || res.classes || []);
        console.log('Classes loaded:', this.allClasses.length);
      },
      error: (err) => console.error('Error loading classes:', err)
    });
  }

  onClassChange() {
    if (this.selectedClassId) {
      this.loadStudentsForClass();
      this.loadAttendanceForDate();
    }
  }

  loadStudentsForClass() {
    if (!this.selectedClassId) return;

    const selectedClass = this.allClasses.find(c => c.id === this.selectedClassId);
    if (!selectedClass) return;

    const className = `${selectedClass.class_number || selectedClass.classNumber}`;
    const division = selectedClass.division;

    this.api.getUsersByClass(className, division).subscribe({
      next: (res: any) => {
        this.classStudents = Array.isArray(res) ? res : (res.results || res.users || []);
        console.log('Students loaded:', this.classStudents.length);

        // Initialize attendance map with default "Present"
        this.attendanceMap = {};
        this.classStudents.forEach(student => {
          this.attendanceMap[student.id] = 'Present';
        });
      },
      error: (err) => console.error('Error loading students:', err)
    });
  }

  loadAttendanceForDate() {
    if (!this.selectedClassId || !this.selectedDate) return;

    const selectedClass = this.allClasses.find(c => c.id === this.selectedClassId);
    if (!selectedClass) return;

    const className = `${selectedClass.class_number || selectedClass.classNumber}${selectedClass.division}`;

    // Load existing attendance for this class and date
    this.api.getAllAttendance().subscribe({
      next: (res: any) => {
        const allAttendance = Array.isArray(res) ? res : (res.results || []);

        // Filter for selected class and date
        this.existingAttendance = allAttendance.filter((a: any) => {
          const attendanceDate = a.date.split('T')[0]; // Get date part only
          const attendanceClass = a.class_name || a.className;
          return attendanceDate === this.selectedDate && attendanceClass === className;
        });

        console.log('Existing attendance loaded:', this.existingAttendance.length);

        // Update attendance map with existing data
        this.existingAttendance.forEach(record => {
          if (record.student) {
            this.attendanceMap[record.student] = record.status;
          }
        });
      },
      error: (err) => console.error('Error loading attendance:', err)
    });
  }

  saveAllAttendance() {
    if (!this.selectedClassId || !this.selectedDate) {
      alert('Please select a class and date');
      return;
    }

    const selectedClass = this.allClasses.find(c => c.id === this.selectedClassId);
    if (!selectedClass) return;

    const className = `${selectedClass.class_number || selectedClass.classNumber}${selectedClass.division}`;

    // Prepare bulk attendance data
    const attendanceRecords = this.classStudents.map(student => ({
      student: student.id,
      date: this.selectedDate,
      status: this.attendanceMap[student.id] || 'Present',
      class_name: className,
      division: selectedClass.division,
      teacher: 1, // Admin user ID
      marked_by: 'Admin'
    }));

    console.log('Saving attendance records:', attendanceRecords);

    // Use bulk mark endpoint
    this.api.markAttendance({ records: attendanceRecords }).subscribe({
      next: () => {
        alert('✅ Attendance saved successfully for all students!');
        this.loadAttendanceForDate();
      },
      error: (err) => {
        console.error('Error saving attendance:', err);
        alert('Error saving attendance. Check console for details.');
      }
    });
  }

  loadAttendanceHistory() {
    if (!this.selectedClassId) {
      alert('Please select a class first');
      return;
    }

    const selectedClass = this.allClasses.find(c => c.id === this.selectedClassId);
    if (!selectedClass) return;

    const className = `${selectedClass.class_number || selectedClass.classNumber}${selectedClass.division}`;

    this.api.getAllAttendance().subscribe({
      next: (res: any) => {
        let allAttendance = Array.isArray(res) ? res : (res.results || []);

        // Filter by class
        allAttendance = allAttendance.filter((a: any) => {
          const attendanceClass = a.class_name || a.className;
          return attendanceClass === className;
        });

        // Filter by date range if provided
        if (this.historyDateFrom) {
          allAttendance = allAttendance.filter((a: any) => {
            const attendanceDate = a.date.split('T')[0];
            return attendanceDate >= this.historyDateFrom;
          });
        }

        if (this.historyDateTo) {
          allAttendance = allAttendance.filter((a: any) => {
            const attendanceDate = a.date.split('T')[0];
            return attendanceDate <= this.historyDateTo;
          });
        }

        this.attendanceHistory = allAttendance;
        console.log('Attendance history loaded:', this.attendanceHistory.length);
      },
      error: (err) => console.error('Error loading attendance history:', err)
    });
  }

  getClassName(): string {
    if (!this.selectedClassId) return '';
    const selectedClass = this.allClasses.find(c => c.id === this.selectedClassId);
    if (!selectedClass) return '';
    return `${selectedClass.class_number || selectedClass.classNumber}${selectedClass.division}`;
  }

  getLastMarkedTime(studentId: number): string {
    const record = this.existingAttendance.find(a => a.student === studentId);
    if (record) {
      return new Date(record.updated_at || record.created_at).toLocaleString();
    }
    return 'Not marked yet';
  }

  get historyPresentCount(): number {
    return this.attendanceHistory.filter(a => a.status === 'Present').length;
  }

  get historyAbsentCount(): number {
    return this.attendanceHistory.filter(a => a.status === 'Absent').length;
  }
}
