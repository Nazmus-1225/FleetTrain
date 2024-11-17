import { Component, OnInit } from '@angular/core';
import { NotebookService } from '../../service/notebook.service';
interface Cell {
  id: string;
  type: 'code' | 'markdown';
  content: string;
  output?: any;
  status: 'idle' | 'running' | 'complete' | 'error';
}
@Component({
  selector: 'app-notebook1',
  templateUrl: './notebook1.component.html',
  styleUrl: './notebook1.component.css'
})

export class Notebook1Component {
  cells: Cell[] = [];
  notebookId: string | null = null;

  constructor(private notebookService: NotebookService) {}

  ngOnInit() {
    this.initializeNotebook();
  }

  async initializeNotebook() {
    try {
      const response = await this.notebookService.createNotebook();
      this.notebookId = response.notebook_id;
      this.addCell('code'); // Add initial cell
    } catch (error) {
      console.error('Failed to initialize notebook:', error);
    }
  }

  addCell(type: 'code' | 'markdown') {
    const newCell: Cell = {
      id: Math.random().toString(36).substr(2, 9),
      type,
      content: '',
      status: 'idle'
    };
    this.cells.push(newCell);
  }

  deleteCell(cellId: string) {
    this.cells = this.cells.filter(cell => cell.id !== cellId);
  }

  async executeCell(cell: Cell) {
    if (!this.notebookId || cell.type !== 'code') return;

    cell.status = 'running';
    try {
      const result = await this.notebookService.executeCode(
        this.notebookId,
        cell.id,
        cell.content
      );
      cell.output = result.output;
      cell.status = 'complete';
    } catch (error:any) {
      cell.status = 'error';
      cell.output = error.message;
    }
  }

  async saveNotebook() {
    if (!this.notebookId) return;
    
    try {
      await this.notebookService.saveNotebook(this.notebookId, this.cells);
      console.log('Notebook saved successfully');
    } catch (error) {
      console.error('Failed to save notebook:', error);
    }
  }
}
// notebook.component.ts




