import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { AuthService } from '../../services/auth.service';
import { environment } from '../../environment/environment';
import { Router } from '@angular/router';
import { OnInit } from '@angular/core';
@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  email = '';
  password = '';
  baseUrl = environment.apiUrl;
  constructor(private http: HttpClient, private authService: AuthService, private router:Router) {}

  role: string | null = null;
  state: boolean = false;
  async ngOnInit(){
    this.role = this.authService.getRole();
    this.state = await this.authService.verifyToken();
    if(this.state){
      this.router.navigate(['/']);
    }
  }

  login() {
    this.http.post(`${this.baseUrl}accounts/login/`, {
      email: this.email,
      password: this.password
    }).subscribe({
      next: (response: any) => {
        this.authService.login(response.token, response.role);
        this.router.navigate(['/']);
      },
      error: () => alert('Invalid credentials')
    });
  }
}
