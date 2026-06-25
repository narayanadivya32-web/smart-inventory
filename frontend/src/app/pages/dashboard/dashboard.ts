import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../services/api.service';
import { RouterLink } from '@angular/router';



@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    RouterLink
  ],
  templateUrl: './dashboard.html',
  styleUrls: ['./dashboard.css']
})
export class DashboardComponent implements OnInit {

  products: any[] = [];
  filteredProducts: any[] = [];

  searchText = '';

  totalProducts = 0;
  lowProducts = 0;
  criticalProducts = 0;

  constructor(
    private api: ApiService,
    private cdr: ChangeDetectorRef
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

        this.products = [...data];
        this.filteredProducts = [...data];

        this.totalProducts = this.products.length;

        this.lowProducts =
          this.products.filter(p => p.status === 'LOW').length;

        this.criticalProducts =
          this.products.filter(p => p.status === 'CRITICAL').length;

        this.cdr.detectChanges();

      },

      error: (err) => {
        console.error(err);
        alert('Failed to load products');
      }

    });

  }

  filterProducts(): void {

    const text = this.searchText.toLowerCase();

    this.filteredProducts = this.products.filter(product =>

      product.name.toLowerCase().includes(text) ||

      product.sku.toLowerCase().includes(text) ||

      product.category.toLowerCase().includes(text)

    );

  }

  logout(): void {

    localStorage.removeItem('token');

    window.location.href = '/';

  }

}