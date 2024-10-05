import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { NotebookComponent } from './components/notebook/notebook.component';


const routes: Routes = [
  {path: 'notebook/:id', component: NotebookComponent }
]

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }