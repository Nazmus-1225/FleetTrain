import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { webSocket, WebSocketSubject } from 'rxjs/webSocket';
import { Notebook, NotebookCell } from '../models/notebook.model';

@Injectable({
  providedIn: 'root'
})
export class NotebookService {
  private apiUrl = 'http://localhost:8000/api';
  private ws!: WebSocketSubject<any>;

  constructor(private http: HttpClient) {}

  connectWebSocket(notebookId: string) {
    this.ws = webSocket(`ws://localhost:8000/ws/notebook/${notebookId}/`);
    return this.ws;
  }

  getNotebook(id: string) {
    return this.http.get<Notebook>(`${this.apiUrl}/notebooks/${id}/`);
  }

  executeCode(notebookId: string, code: string) {
    this.ws.next({ code });
  }

  saveNotebook(notebook: Notebook) {
    return this.http.put(`${this.apiUrl}/notebooks/${notebook.id}/`, notebook);
  }
}