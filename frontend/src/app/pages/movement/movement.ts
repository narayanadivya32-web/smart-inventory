import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-movement',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './movement.html',
  styleUrls: ['./movement.css']
})
export class MovementComponent implements OnInit {

  products: any[] = [];

 movement = {
  product_id: 0,
  warehouse_id: 1,
  movement_type: 'IN',
  quantity: 1
};

  constructor(
    private api: ApiService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.loadProducts();
  }

  loadProducts(): void {

    const token = localStorage.getItem('token');

    if (!token) {
      alert('Please login again');
      return;
    }

    this.api.getProducts(token).subscribe({
      next: (data: any[]) => {
        this.products = data;

        if (this.products.length > 0) {
          this.movement.product_id = this.products[0].id;
        }
      },
      error: (err) => console.error(err)
    });

  }

  saveMovement(): void {

    const token = localStorage.getItem('token');

    if (!token) {
      alert('Please login');
      return;
    }

    this.api.addMovement(this.movement, token).subscribe({
      next: () => {
        alert('Stock movement saved successfully.');
        this.router.navigate(['/dashboard']);
      },
    error: (err: any) => {

  console.log("=================================");
  console.log("HTTP STATUS:", err.status);
  console.log("ERROR BODY:", err.error);
  console.log("FULL ERROR:", err);
  console.log("=================================");

  if (err.error?.detail) {
    alert(err.error.detail);
  } else {
    alert("Status: " + err.status);
  }

}
    });

  }

}