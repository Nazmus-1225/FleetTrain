import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { AuthService } from '../../services/auth.service';
import { environment } from '../../environment/environment';
@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  email = '';
  password = '';
  baseUrl = environment.apiUrl;
  constructor(private http: HttpClient, private authService: AuthService) {}

  login() {
    this.http.post(`${this.baseUrl}accounts/login/`, {
      email: this.email,
      password: this.password
    }).subscribe({
      next: (response: any) => {
        this.authService.login(response.token, response.role);
        alert('Login successful!');
      },
      error: () => alert('Invalid credentials')
    });
  }
}
