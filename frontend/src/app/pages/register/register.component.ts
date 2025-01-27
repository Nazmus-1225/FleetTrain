import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environment/environment';
import { Router } from '@angular/router';
import { OnInit } from '@angular/core';
import { AuthService } from '../../services/auth.service';
@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit{
  email = '';
  password = '';
  baseUrl = environment.apiUrl;

  constructor(private http: HttpClient,private router: Router, private authService:AuthService) {}

  role: string | null = null;
  state: boolean = false;
  async ngOnInit(){
    this.role = this.authService.getRole();
    this.state = await this.authService.verifyToken();
    if(this.state){
      this.router.navigate(['/']);
    }
  }

  register() {
    this.http.post(`${this.baseUrl}accounts/register/`, {
      email: this.email,
      password: this.password,
    }).subscribe({
      next: () => this.router.navigate(['/']),
      error: () => alert('Error during registration')
    });
  }
}
