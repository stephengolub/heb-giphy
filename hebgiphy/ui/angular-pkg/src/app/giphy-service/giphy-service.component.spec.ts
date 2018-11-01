import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { GiphyServiceComponent } from './giphy-service.component';

describe('GiphyServiceComponent', () => {
  let component: GiphyServiceComponent;
  let fixture: ComponentFixture<GiphyServiceComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ GiphyServiceComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(GiphyServiceComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
