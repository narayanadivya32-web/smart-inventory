import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  private baseUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  // LOGIN
  login(username: string, password: string): Observable<any> {
    return this.http.post<any>(
      `${this.baseUrl}/api/auth/token`,
      {
        username,
        password
      }
    );
  }

  // PRODUCTS
  getProducts(token: string): Observable<any[]> {

    const headers = new HttpHeaders({
      Authorization: `Bearer ${token}`
    });

    return this.http.get<any[]>(
      `${this.baseUrl}/api/products`,
      { headers }
    );
  }

  // SINGLE PRODUCT MOVEMENTS
  getMovements(productId: number, token: string): Observable<any[]> {

    const headers = new HttpHeaders({
      Authorization: `Bearer ${token}`
    });

    return this.http.get<any[]>(
      `${this.baseUrl}/api/products/${productId}/movements`,
      { headers }
    );
  }

  // ALL MOVEMENTS (History Page)
  getAllMovements(token: string): Observable<any[]> {

    const headers = new HttpHeaders({
      Authorization: `Bearer ${token}`
    });

    return this.http.get<any[]>(
      `${this.baseUrl}/api/movements`,
      { headers }
    );
  }

  // ADD MOVEMENT
  addMovement(data: any, token: string): Observable<any> {

    const headers = new HttpHeaders({
      Authorization: `Bearer ${token}`
    });

    return this.http.post<any>(
      `${this.baseUrl}/api/movements`,
      data,
      { headers }
    );
  }

  // ADD PRODUCT
addProduct(product: any, token: string): Observable<any> {

  const headers = new HttpHeaders({
    Authorization: `Bearer ${token}`
  });

  return this.http.post<any>(
    `${this.baseUrl}/api/products`,
    product,
    { headers }
  );
}

// UPDATE PRODUCT
updateProduct(id: number, product: any, token: string): Observable<any> {

  const headers = new HttpHeaders({
    Authorization: `Bearer ${token}`
  });

  return this.http.put<any>(
    `${this.baseUrl}/api/products/${id}`,
    product,
    { headers }
  );
}

// DELETE PRODUCT
deleteProduct(id: number, token: string): Observable<any> {

  const headers = new HttpHeaders({
    Authorization: `Bearer ${token}`
  });

  return this.http.delete<any>(
    `${this.baseUrl}/api/products/${id}`,
    { headers }
  );
}

}