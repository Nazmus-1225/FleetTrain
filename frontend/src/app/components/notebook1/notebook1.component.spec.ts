import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Notebook1Component } from './notebook1.component';

describe('Notebook1Component', () => {
  let component: Notebook1Component;
  let fixture: ComponentFixture<Notebook1Component>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [Notebook1Component]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Notebook1Component);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
