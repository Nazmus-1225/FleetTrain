import { Component, OnInit } from '@angular/core';
import { NotebookService } from '../../services/notebook.service';
import { ActivatedRoute } from '@angular/router';
@Component({
  selector: 'app-notebook',
  templateUrl: './notebook.component.html',
  styleUrl: './notebook.component.css'
})
export class NotebookComponent implements OnInit{

  constructor(private notebookService:NotebookService, private route:ActivatedRoute){}

  fileSystem = [
    {
      name: 'Folder 1',
      files: [
        { name: 'File 1.1' },
        { name: 'File 1.2' },
      ],
    },
    {
      name: 'Folder 2',
      files: [
        { name: 'File 2.1' },
        { name: 'File 2.2' },
      ],
    },
  ];

  notebook = {
    name:'untitled-1.ipynb',
    cells: [
      { code: '', output: '', expanded: false },
    ],
  };

  notebookModel = {

  }
  id!: number;
  ngOnInit(): void {
    const paramId = this.route.snapshot.paramMap.get('id');
    this.id = paramId ? parseInt(paramId, 10) : 0;
    this.notebookService.openNotebook(this.id).subscribe({
      next: (response: any) => {
        console.log(response);
      },
      error: () => console.log()
    });
      
  }

  downloadFile(file: any) {
    console.log('Downloading:', file);
    // Implement API call here
  }

  deleteFile(file: any) {
    console.log('Deleting:', file);
    // Implement API call here
  }

  uploadFile() {
    console.log('Uploading file');
    // Implement API call here
  }

  runCell(index: number) {
    console.log('Running cell:', index);
    // Implement API call here
    this.notebook.cells[index].output = 'Output from running the cell';
  }

  stopCell(index: number) {
    console.log('Stopping cell:', index);
    // Implement logic here
  }

  deleteCell(index: number) {
    this.notebook.cells.splice(index, 1);
  }

  addCell() {
    this.notebook.cells.push({ code: '', output: '', expanded: false });
  }

  toggleOutput(cell: any) {
    cell.expanded = !cell.expanded;
  }
}
