import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environment/environment';
@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent {
  email = '';
  password = '';
  baseUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  register() {
    this.http.post(`${this.baseUrl}accounts/register/`, {
      email: this.email,
      password: this.password,
    }).subscribe({
      next: () => alert('Registration successful!'),
      error: () => alert('Error during registration')
    });
  }
}
