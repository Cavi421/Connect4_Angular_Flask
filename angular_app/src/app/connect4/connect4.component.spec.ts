import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Connect4Component } from './connect4.component';

describe('Connect4Component', () => {
  let component: Connect4Component;
  let fixture: ComponentFixture<Connect4Component>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [Connect4Component]
    });
    fixture = TestBed.createComponent(Connect4Component);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
