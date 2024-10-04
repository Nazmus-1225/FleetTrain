
import { Component, OnInit, ElementRef, ViewChild } from '@angular/core';
import { NotebookService } from '../../services/notebook.service';
import { NotebookPanel, NotebookActions } from '@jupyterlab/notebook';
import { DocumentRegistry } from '@jupyterlab/docregistry';
@Component({
  selector: 'app-notebook',
  standalone: true,
  imports: [],
  templateUrl: './notebook.component.html',
  styleUrl: './notebook.component.css'
})

export class NotebookComponent implements OnInit {
  @ViewChild('notebookContainer', { static: true }) notebookContainer!: ElementRef;
  private notebookPanel: NotebookPanel | null = null;
  private kernel: any = null;

  constructor(private notebookService : NotebookService) {}

  async ngOnInit() {
    try {
      // Start the kernel
      this.kernel = await this.notebookService.startKernel();
      
      // Create a new notebook
      this.createNotebook();
    } catch (error) {
      console.error('Failed to initialize notebook:', error);
    }
  }

  private async createNotebook() {
    const context = {
      sessionContext: {
        kernel: this.kernel,
        session: {
          path: 'notebook.ipynb',
          name: 'python3',
          type: 'notebook'
        }
      }
    } as unknown as DocumentRegistry.IContext<NotebookPanel>;

    // Initialize notebook panel
    this.notebookPanel = new NotebookPanel({ context });
    
    // Add the notebook to the DOM
    this.notebookContainer.nativeElement.appendChild(this.notebookPanel.node);
  }

  async runCell() {
    if (this.notebookPanel) {
      await NotebookActions.run(this.notebookPanel.content, this.kernel);
    }
  }

  async addCell() {
    if (this.notebookPanel) {
      NotebookActions.insertBelow(this.notebookPanel.content);
    }
  }

  ngOnDestroy() {
    if (this.kernel) {
      this.kernel.shutdown();
    }
  }
}
