// notebook.service.ts
import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { environment } from '../environment/environment';
import { firstValueFrom } from 'rxjs';

interface NotebookResponse {
  notebook_id: string;
}

interface ExecuteResponse {
  output: any;
}

interface Cell {
  id: string;
  type: 'code' | 'markdown';
  content: string;
  output?: any;
  status: 'idle' | 'running' | 'complete' | 'error';
}

@Injectable({
  providedIn: 'root'
})
export class NotebookService {
  private apiUrl = `${environment.apiUrl}/api/notebooks`;

  constructor(private http: HttpClient) {}

  async createNotebook(): Promise<NotebookResponse> {

    try {
      const response = await firstValueFrom(
        
        this.http.post<NotebookResponse>(`${this.apiUrl}/create`, {})
      );
      
      if (!response) {
        throw new Error('Failed to create notebook');
      }
      
      return response;
    } catch (error) {
      if (error instanceof HttpErrorResponse) {
        throw new Error(`HTTP Error: ${error.message}`);
      }
      throw new Error('Failed to create notebook');
    }
  }

  async executeCode(notebookId: string, cellId: string, code: string): Promise<ExecuteResponse> {
    try {
      const response = await firstValueFrom(
        this.http.post<ExecuteResponse>(
          `${this.apiUrl}/${notebookId}/execute`,
          {
            cell_id: cellId,
            code: code
          }
        )
      );
      
      if (!response) {
        throw new Error('Failed to execute code');
      }
      
      return response;
    } catch (error) {
      if (error instanceof HttpErrorResponse) {
        throw new Error(`HTTP Error: ${error.message}`);
      }
      throw new Error('Failed to execute code');
    }
  }

  async saveNotebook(notebookId: string, cells: Cell[]): Promise<void> {
    try {
      await firstValueFrom(
        this.http.post(
          `${this.apiUrl}/${notebookId}/save`,
          { cells }
        )
      );
    } catch (error) {
      if (error instanceof HttpErrorResponse) {
        throw new Error(`HTTP Error: ${error.message}`);
      }
      throw new Error('Failed to save notebook');
    }
  }
}