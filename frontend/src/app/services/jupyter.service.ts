
  import { Injectable } from '@angular/core';
  import { ServerConnection, SessionManager, KernelManager, KernelMessage } from '@jupyterlab/services';
    
    @Injectable({
      providedIn: 'root',
    })
    export class JupyterService {
      private serverSettings = ServerConnection.makeSettings({
        baseUrl: 'http://localhost:8888', // Jupyter server URL
        token: '69c85d5a28a813ac25aa229e1d1cc046509d979b40040247',       // Replace with your token
      });
    
      private kernelManager = new KernelManager({ serverSettings: this.serverSettings });
      private sessionManager = new SessionManager({
        serverSettings: this.serverSettings,
        kernelManager: this.kernelManager,
      });
    
      constructor() {}
    
      async createSession(path: string, kernelName: string) {
        try {
          const session = await this.sessionManager.startNew({
            path: 'example.ipynb', // Specify a valid path
            kernel: { name: 'python3' }, // Provide the kernel as an object
            name: 'MySession', // Optional: Name of the session
            type: 'notebook', // Optional: Type of the session (e.g., notebook, console)
          });
          console.log('Session started:', session);
        } catch (error) {
          console.error('Failed to start session:', error);
        }
        
      }
    
      async executeCode(session: any, code: string) {
        const future = session.kernel.requestExecute({ code });
        future.onIOPub = (msg: KernelMessage.IIOPubMessage) => {
          console.log('Execution Result:', msg);
        };
      }
    }
    
