import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-history',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './history.html',
  styleUrls: ['./history.css']
})
export class HistoryComponent implements OnInit {

  movements: any[] = [];

  constructor(private api: ApiService) {}

  ngOnInit(): void {
    this.loadHistory();
  }

  loadHistory() {

    const token = localStorage.getItem('token');

    if (!token) {
      alert('Please login');
      return;
    }

    this.api.getAllMovements(token).subscribe({

      next: (data: any[]) => {
        console.log(data);
        this.movements = data;
      },

      error: (err: any) => {
        console.error(err);
        alert("Failed to load movement history");
      }

    });

  }

}