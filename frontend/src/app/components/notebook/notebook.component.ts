import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { NotebookService } from '../../services/notebook.service';
import { Notebook, NotebookCell } from '../../models/notebook.model';
import * as monaco from 'monaco-editor';
import { marked } from 'marked';

@Component({
  selector: 'app-notebook',
  templateUrl: './notebook.component.html',
  styleUrls: ['./notebook.component.scss']
})
export class NotebookComponent implements OnInit {
  notebook!: Notebook;
  editor!: monaco.editor.IStandaloneCodeEditor;
  activeCell!: NotebookCell;

  constructor(
    private route: ActivatedRoute,
    private notebookService: NotebookService
  ) {}

  ngOnInit() {
    const notebookId = this.route.snapshot.paramMap.get('id');
    if (!notebookId) {
      console.error('Notebook ID is missing from the route');
      return;
    }
    this.notebookService.getNotebook(notebookId).subscribe(notebook => {
      this.notebook = notebook;
      this.setupWebSocket();
    });
  }

  setupWebSocket() {
    this.notebookService.connectWebSocket(this.notebook.id).subscribe(
      message => {
        if (message.outputs) {
          this.activeCell.outputs = message.outputs;
        }
      },
      error => console.error('WebSocket error:', error)
    );
  }

  initializeEditor(element: HTMLElement, cell: NotebookCell) {
    this.editor = monaco.editor.create(element, {
      value: cell.content,
      language: 'python',
      theme: 'vs-dark',
      minimap: { enabled: false },
      automaticLayout: true
    });

    this.editor.onDidChangeModelContent(() => {
      cell.content = this.editor.getValue();
    });
  }

  executeCell(cell: NotebookCell) {
    this.activeCell = cell;
    cell.outputs = [];
    this.notebookService.executeCode(this.notebook.id, cell.content);
  }

  addCell(type: 'code' | 'markdown') {
    const newCell: NotebookCell = {
      id: Math.random().toString(36).substr(2, 9),
      type,
      content: '',
      outputs: []
    };
    this.notebook.cells.push(newCell);
  }

  renderMarkdown(content: string): string {
    return String(marked(content));
  }
}
