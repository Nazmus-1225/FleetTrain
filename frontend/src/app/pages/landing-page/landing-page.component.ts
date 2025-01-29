import { Component } from '@angular/core';
import { AuthService } from '../../services/auth.service';
import { AdminService } from '../../services/admin.service';
import { OnInit } from '@angular/core';
import { FormGroup, FormControl } from '@angular/forms';
import { UserService } from '../../services/user.service';
import { Router } from '@angular/router';
@Component({
  selector: 'app-landing-page',
  templateUrl: './landing-page.component.html',
  styleUrls: ['./landing-page.component.css']
})
export class LandingPageComponent implements OnInit {
  role: string | null = null;
  state: boolean = false;
  showModal: boolean = false;
  resources: any[] = [];
  kernels: any[] = [];
  notebooks: any[] = [];
  createResourceForm: FormGroup = new FormGroup({
    ip_address: new FormControl(''), // Default value as an empty string
    max_kernels: new FormControl(0),  // Default value as 0
    token: new FormControl(''), 
    username: new FormControl(''), 
    password: new FormControl('')
  });
  newNotebookType: string = 'central';
  newNotebookNodes: number = 1;

  constructor(private authService: AuthService, private adminService: AdminService, private userService:UserService, private router:Router) {}
  async ngOnInit(){
    this.role = this.authService.getRole();
    this.state = await this.authService.verifyToken();
    if(this.role=="admin"){
      this.fetchKernels();
      this.fetchResources();
    }
    if(this.role=="user"){
      this.fetchNotebooks();
    }
  }

  onTypeChange(value: string): void {
    this.newNotebookType = value; // Update the variable when the radio button changes
  }

  logout() {
    this.authService.logout();
    window.location.reload();
  }

  openCreateResourceModal(): void {
    this.showModal = true;
  }

  closeCreateResourceModal(): void {
    this.showModal = false;
    this.createResourceForm.reset();
  }

  createResource(): void {
    if (this.createResourceForm.valid){
      this.adminService.addResource(this.createResourceForm).subscribe({
        next: () => {
          this.closeCreateResourceModal();
          this.fetchResources(); // Refresh the resources list
        },
        error: (error) => {
          console.error('Error creating resource:', error);
        }
      });}
    
  }

  fetchResources(): void {
    this.adminService.getResources().subscribe({
      next: (data: any) => {
        this.resources = data;
      },
      error: (error) => {
        console.error('Error fetching resources:', error);
      }
    });
  }

  fetchKernels(): void {
    this.adminService.getKernels().subscribe({
      next: (data: any) => {
        this.kernels = data;
      },
      error: (error) => {
        console.error('Error fetching resources:', error);
      }
    });
  }

  deleteNotebook(id: number): void {
    this.userService.deleteNotebook(id).subscribe({
      next: () => {
        this.notebooks = this.notebooks.filter(notebook => notebook.id !== id);
      },
      error: (error) => {
        console.error('Error deleting resource:', error);
      }
    });
  }

  fetchNotebooks(): void {
    this.userService.getNotebooks().subscribe({
      next: (data: any) => {
        this.notebooks = data;
      },
      error: (error) => {
        console.error('Error fetching resources:', error);
      }
    });
  }

  deleteResource(id: number): void {
    this.adminService.deleteResource(id).subscribe({
      next: () => {
        this.resources = this.resources.filter(resource => resource.id !== id);
      },
      error: (error) => {
        console.error('Error deleting resource:', error);
      }
    });
  }

  createNotebook(): void {
    this.userService.addNotebook(this.newNotebookType,this.newNotebookNodes).subscribe({
      next: (data : any) => {
        this.router.navigate(['/notebook', data['notebook_id']]);
      },
      error: (error) => {
        console.error('Error creating resource:', error);
        }
      });}
    
  }

