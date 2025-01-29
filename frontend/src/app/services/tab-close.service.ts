import { Injectable, OnDestroy } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../environment/environment';
@Injectable({
  providedIn: 'root',
})
export class TabCloseService implements OnDestroy {
  id:number=0;
  constructor(private http: HttpClient) {
    // Attach event listener for browser/tab close
    window.addEventListener('beforeunload', this.onTabClose.bind(this));
  }

  setId(id:number){
    this.id=id;
  }

  onTabClose(event: Event) {
    const url = `${environment.apiUrl}notebooks/close/${this.id}/`;
    this.http.delete(url, {}).subscribe({
      next: () => console.log('Tab close notified'),
      error: (err) => console.error('Error notifying tab close', err),
    });
  }

  ngOnDestroy(): void {
    // Clean up event listener
    window.removeEventListener('beforeunload', this.onTabClose.bind(this));
  }
}
