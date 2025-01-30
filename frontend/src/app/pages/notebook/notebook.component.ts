import { Component, OnInit } from '@angular/core';
import { NotebookService } from '../../services/notebook.service';
import { ActivatedRoute } from '@angular/router';
import { TabCloseService } from '../../services/tab-close.service';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environment/environment';
@Component({
  selector: 'app-notebook',
  templateUrl: './notebook.component.html',
  styleUrl: './notebook.component.css'
})
export class NotebookComponent implements OnInit{

  constructor(private notebookService:NotebookService, private route:ActivatedRoute, private tabCloseService:TabCloseService, private http:HttpClient){}
  
  newCellType = 'central';
  fileSystem:string[] = [];

  notebook = {
    cells: [
      { code: 'xyz', outputs: ['xyz','abc', 'pqr'],  type:'distributed' }
    ],
  };

  notebookModel!: {
    id: number;
    name: string;
    create_date: string;
    type: string;
    num_of_nodes: number;
    user_id: number;
  };
  id!: number;
  paramId:string|null='';
  selectedFile: File | null = null;
  onFileSelected(event: any): void {
    this.selectedFile = event.target.files[0];
  }
  ngOnInit(): void {
    this.paramId = this.route.snapshot.paramMap.get('id');
    this.id = this.paramId ? parseInt(this.paramId, 10) : 0;
    this.tabCloseService.setId(this.id);
    this.notebookService.openNotebook(this.id).subscribe({
      next: (response: any) => {
        this.notebookModel=response;
        this.newCellType=this.notebookModel['type'];
      },
      error: () => console.log()
    });
    this.notebookService.fetchFile(this.notebookModel.id).subscribe({
      next: (response) => {
        console.log(response);
        this.fileSystem=response},
      error: (error) => console.error(error),
    });
      
  }

  downloadFile(file: string) {
    this.http.get(`${environment.apiUrl}notebooks/download/${this.notebookModel.id}/${file}/`).subscribe({
      next: (response) => console.log( response),
      error: (error) => console.error( error),
    });
  }

  downloadNotebook() {
    this.http.get(`${environment.apiUrl}notebooks/download/${this.notebookModel.id}/`).subscribe({
      next: (response) => console.log( response),
      error: (error) => console.error( error),
    });
  }

  deleteFile(file: any) {
    console.log('Deleting:', file);
    // Implement API call here
  }

  uploadFile(): void {
    if (!this.selectedFile) {
      alert('Please select a file first.');
      return;
    }

    const formData = new FormData();
    formData.append('file', this.selectedFile);
    if (this.paramId){
      formData.append('notebook_id',this.paramId);}

    this.notebookService.uploadFile(formData).subscribe({
      next: (response) => console.log('File uploaded successfully', response),
      error: (error) => console.error('File upload failed', error),
    });
    this.notebookService.fetchFile(this.notebookModel.id).subscribe({
      next: (response) => this.fileSystem=response,
      error: (error) => console.error(error),
    });
  }

  runCell(cell: any) {
    console.log(cell['outputs']);
    this.http.post(`${environment.apiUrl}notebooks/execute/`,{cells:this.notebook.cells,code:cell['code'],type:cell['type'],notebook_id:this.id}).subscribe({
      next: (response) => cell['outputs']=response,
      error: (error) => console.error( error),
    });
  }

  stopCell(index: number) {
    console.log('Stopping cell:', index);
    // Implement logic here
  }

  deleteCell(index: number) {
    this.notebook.cells.splice(index, 1);
  }

  addCell() {
    let outputs:string[] = [];

    if (this.newCellType === 'distributed') {
      outputs = new Array(this.notebookModel.num_of_nodes).fill('');}
    else{
      outputs=[''];
    }
    this.notebook.cells.push({ code: '', outputs: outputs, type: this.newCellType });
  }

  toggleOutput(cell: any) {
    cell.expanded = !cell.expanded;
  }
}
