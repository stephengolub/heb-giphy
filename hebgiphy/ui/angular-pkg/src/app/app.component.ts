import { Component } from '@angular/core';

import { GiphyComponent } from './giphy/giphy.component';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'HEB Giphy Search';

  constructor() { }
}
