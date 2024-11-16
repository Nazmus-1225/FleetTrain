// src/app/components/dashboard/dashboard.component.ts
import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../auth/auth.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html'
})
export class DashboardComponent implements OnInit {
  message: string = '';

  constructor(private authService: AuthService) {}

  ngOnInit(): void {
    this.authService.verifyToken().subscribe(
      () => {
        this.message = 'Welcome to the dashboard!';
      },
      (error) => {
        console.error('Token verification failed', error);
      }
    );
  }
}
