import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-products',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    RouterLink
  ],
  templateUrl: './products.html',
  styleUrls: ['./products.css']
})
export class ProductsComponent implements OnInit {

  products: any[] = [];
  searchText = '';

  constructor(private api: ApiService) {}

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
      },

      error: (err: any) => {
        console.error(err);
        alert('Failed to load products');
      }

    });

  }

  deleteProduct(id: number): void {

    const confirmDelete = confirm(
      'Are you sure you want to delete this product?'
    );

    if (!confirmDelete) {
      return;
    }

    const token = localStorage.getItem('token');

    if (!token) {
      return;
    }

    this.api.deleteProduct(id, token).subscribe({

      next: () => {

        alert('Product deleted successfully');

        this.loadProducts();

      },

      error: (err: any) => {

        console.error(err);

        if (err.error?.detail) {
          alert(err.error.detail);
        } else {
          alert('Delete failed');
        }

      }

    });

  }

  get filteredProducts() {

    return this.products.filter(p =>
      p.name.toLowerCase().includes(this.searchText.toLowerCase()) ||
      p.sku.toLowerCase().includes(this.searchText.toLowerCase())
    );

  }

}