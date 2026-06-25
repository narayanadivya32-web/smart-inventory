import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-add-product',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    RouterLink
  ],
  templateUrl: './add-product.html',
  styleUrls: ['./add-product.css']
})
export class AddProductComponent {

  product = {
    sku: '',
    name: '',
    reorder_level: 10
  };

  constructor(
    private api: ApiService,
    private router: Router
  ) {}

  saveProduct(): void {

    const token = localStorage.getItem('token');

    if (!token) {
      alert('Please login');
      return;
    }

    this.api.addProduct(this.product, token).subscribe({

      next: () => {

        alert('Product added successfully.');

        this.router.navigate(['/dashboard']);

      },

      error: (err: any) => {

        console.error(err);

        if (err.error?.detail) {
          alert(err.error.detail);
        } else {
          alert('Failed to add product');
        }

      }

    });

  }

}