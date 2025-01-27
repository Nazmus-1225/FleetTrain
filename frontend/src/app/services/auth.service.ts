import { Injectable } from '@angular/core';
import { environment } from '../environment/environment';
import { HttpHeaders, HttpClient, HttpResponse } from '@angular/common/http';

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

  verifyToken(): Promise<boolean> {
    const token = this.getToken();
    if (!token) {
      return Promise.resolve(false);
    }
  
    const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);
    return this.http.get<any>(this.verifyTokenUrl, { headers }).toPromise()
      .then((response) => {
        // If the request succeeds and status is 200
        return true;
      })
      .catch((error) => {
        console.error(error);
        // If there's an error (e.g., token invalid or expired)
        return false;
      });
  }
  
  
}
