
import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { SidebarComponent } from './components/sidebar/sidebar';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
      CommonModule,
    RouterOutlet,
    SidebarComponent
  ],
  templateUrl: './app.html',
  styleUrls: ['./app.css']
})
export class App {

  showSidebar(): boolean {

    return window.location.pathname !== '/';

  }

}