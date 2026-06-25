import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './login.html'
})
export class LoginComponent {

  username = '';
  password = '';

  constructor(
    private api: ApiService,
    private router: Router
  ) {}

  login() {

    console.log('LOGIN CLICKED'); // debug

    this.api.login(this.username, this.password).subscribe({
      next: (res: any) => {

        console.log('LOGIN SUCCESS:', res);

        // store token
        localStorage.setItem('token', res.access_token);

        alert('Login successful');

        // navigate to dashboard
        this.router.navigate(['/dashboard']);
      },

      error: (err) => {
        console.error('LOGIN ERROR:', err);
        alert('Login failed');
      }
    });
  }
}