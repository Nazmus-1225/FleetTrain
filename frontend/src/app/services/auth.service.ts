import { Injectable } from '@angular/core';
import { environment } from '../environment/environment';
import { of } from 'rxjs';
import { HttpHeaders, HttpClient, HttpResponse } from '@angular/common/http';
import { catchError, map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private tokenKey = 'jwt-token';
  private roleKey = 'user-role';
  private verifyTokenUrl = `${environment.apiUrl}accounts/jwt-verify/`;

  constructor(private http: HttpClient) {}

  login(token: string, role: string) {
    localStorage.setItem(this.tokenKey, token);
    localStorage.setItem(this.roleKey, role);
  }

  logout() {
    localStorage.removeItem(this.tokenKey);
    localStorage.removeItem(this.roleKey);
  }

  getRole(): string | null {
    return localStorage.getItem(this.roleKey);
  }

  getToken(): string | null {
    return localStorage.getItem(this.tokenKey);
  }

  verifyToken(callback: (isAuthenticated: boolean) => void) {
    const token = this.getToken();

    const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);
    this.http.get<any>(this.verifyTokenUrl,{headers}).subscribe({next:(response: HttpResponse<any>)=>{

      if(response.status==200){
        const isAuthenticated = true;
        callback(isAuthenticated);
      }
      else 
        {const isAuthenticated = false;
        callback(isAuthenticated);
        }
        
    },
    error: (e: any) => console.error(e)
  })

  
  
  }
  
  
}
