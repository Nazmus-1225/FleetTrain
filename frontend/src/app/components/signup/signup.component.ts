// src/app/components/signup/signup.component.ts
import { Component } from '@angular/core';
import { AuthService } from '../../auth/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html'
})
export class SignupComponent {
  email: string = '';
  password: string = '';

  constructor(private authService: AuthService, private router: Router) {}

  onSignup() {
    this.authService.signup({ email: this.email, password: this.password }).subscribe(
      () => {
        alert('Account created successfully!');
        this.router.navigate(['/login']);
      },
      (error) => {
        console.error('Signup failed', error);
      }
    );
  }
}
