import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from '../environment/environment';
import { AuthService } from './auth.service';
import { Observable } from 'rxjs';
import { FormGroup } from '@angular/forms';
@Injectable({
  providedIn: 'root'
})
export class AdminService {

  baseUrl = environment.apiUrl;
  headers = new HttpHeaders();

  constructor(private http:HttpClient, private authService:AuthService) {
    this.headers = new HttpHeaders().set('Authorization', `Bearer ${this.authService.getToken()}`);
  }

  getResources(): Observable<any> {
    return this.http.get(`${this.baseUrl}resources/all/`,{headers:this.headers});
  }

  getKernels(): Observable<any> {
    return this.http.get(`${this.baseUrl}resources/kernels/`,{headers:this.headers});
  }

  addResource(createResourceForm : FormGroup): Observable<any> {
    return this.http.post(`${this.baseUrl}resources/create/`,createResourceForm.value,{ headers:this.headers });
  }

  deleteResource(id : number): Observable<any> {
    return this.http.delete(`${this.baseUrl}resources/delete/${id}/`,{ headers:this.headers });
  }
}
