import { TestBed } from '@angular/core/testing';

import { TabCloseService } from './tab-close.service';

describe('TabCloseService', () => {
  let service: TabCloseService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(TabCloseService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
