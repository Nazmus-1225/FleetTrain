import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from '../environment/environment';
import { AuthService } from './auth.service';
import { Observable } from 'rxjs';
@Injectable({
  providedIn: 'root'
})
export class UserService {

  baseUrl = environment.apiUrl;
  headers = new HttpHeaders();

  constructor(private http:HttpClient, private authService:AuthService) {
    this.headers = new HttpHeaders().set('Authorization', `Bearer ${this.authService.getToken()}`);
  }

  getNotebooks(): Observable<any> {
    return this.http.get(`${this.baseUrl}notebooks/all/`,{headers:this.headers});
  }

  deleteNotebook(id : number): Observable<any> {
    const headers = new HttpHeaders().set('Authorization', `Bearer ${this.authService.getToken()}`);
    return this.http.delete(`${this.baseUrl}notebooks/delete/${id}/`,{ headers:headers })
  }

  addNotebook(type : string, nodes:number): Observable<any> {
      const headers = new HttpHeaders().set('Authorization', `Bearer ${this.authService.getToken()}`);
      return this.http.post(`${this.baseUrl}notebooks/create/`,{"type":type,"nodes":nodes},{ headers:headers })
    }
  
}
