import { Injectable } from '@angular/core';
import { ServerConnection } from '@jupyterlab/services';
import { ISessionContext } from '@jupyterlab/apputils';
import { ServiceManager } from '@jupyterlab/services';

@Injectable({
  providedIn: 'root'
})
export class NotebookService {
  private serviceManager: ServiceManager;

  constructor() {
    // Configure the server connection settings
    const serverSettings = ServerConnection.makeSettings({
      baseUrl: 'http://localhost:8888', // Your Jupyter server URL
      wsUrl: 'ws://localhost:8888',     // WebSocket URL
      token: 'your_token_here'          // Your Jupyter server token
    });

    // Initialize the service manager
    this.serviceManager = new ServiceManager({ serverSettings });
  }

  async startKernel() {
    const kernel = await this.serviceManager.kernels.startNew({
      name: 'python3'
    });
    return kernel;
  }
}
