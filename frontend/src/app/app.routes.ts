import { Routes } from '@angular/router';

import { LoginComponent } from './pages/login/login';
import { DashboardComponent } from './pages/dashboard/dashboard';
import { MovementComponent } from './pages/movement/movement';
import { HistoryComponent } from './pages/history/history';
import { AddProductComponent } from './pages/add-product/add-product';
import { ProductsComponent } from './pages/products/products';

export const routes: Routes = [

  { path: '', component: LoginComponent },

  { path: 'products', component: ProductsComponent },

  { path: 'dashboard', component: DashboardComponent },

  { path: 'movement', component: MovementComponent },

  { path: 'history', component: HistoryComponent },

  { path: 'add-product', component: AddProductComponent }

];