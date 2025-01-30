import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '../environment/environment';
import { AuthService } from './auth.service';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class NotebookService {

  baseUrl = environment.apiUrl;
  headers = new HttpHeaders();
  
  constructor(private http:HttpClient, private authService:AuthService) {
    this.headers = new HttpHeaders().set('Authorization', `Bearer ${this.authService.getToken()}`);
  }

  openNotebook(id:number): Observable<any>{
    return this.http.get(`${this.baseUrl}notebooks/open/${id}/`,{ headers:this.headers });
  }

  uploadFile(formData:FormData): Observable<any>{
    return this.http.post(`${this.baseUrl}notebooks/upload/`,formData,{ headers:this.headers });
  }

  fetchFile(id:number): Observable<any>{
    return this.http.get(`${this.baseUrl}notebooks/getFiles/${id}/`);
  }

  
}
