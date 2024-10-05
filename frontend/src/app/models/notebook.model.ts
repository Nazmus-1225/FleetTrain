export interface NotebookCell {
    id: string;
    type: 'code' | 'markdown';
    content: string;
    outputs: any[];
  }
  
  export interface Notebook {
    id: string;
    title: string;
    cells: NotebookCell[];
  }
  