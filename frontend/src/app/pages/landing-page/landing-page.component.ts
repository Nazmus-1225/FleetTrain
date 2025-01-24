import { Component } from '@angular/core';
import { AuthService } from '../../services/auth.service';
import { OnInit } from '@angular/core';
@Component({
  selector: 'app-landing-page',
  templateUrl: './landing-page.component.html',
  styleUrls: ['./landing-page.component.css']
})
export class LandingPageComponent implements OnInit {
  role: string | null = null;
  state: boolean = true;

  constructor(private authService: AuthService) {
    this.role = this.authService.getRole();
  }

  ngOnInit(): void {
    this.authService.verifyToken((isAuthenticated) => {
      if (isAuthenticated) {
        this.state=true;
      } 
      // else {
      //   this.state=false;
      // }
    });
  }

  logout() {
    this.authService.logout();
  }
}
