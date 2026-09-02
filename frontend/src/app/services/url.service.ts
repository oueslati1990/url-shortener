import { HttpClient } from "@angular/common/http";
import { inject, Injectable } from "@angular/core";
import { environment } from "../../environments/environment";
import { Observable } from "rxjs";
import { CreateUrlRequest, UrlItem } from "../models/url.model";

@Injectable({ providedIn: 'root' })
export class UrlService {
    private http = inject(HttpClient)
    private apiUrl = `${environment.apiUrl}/api/urls`

    getAll(): Observable<UrlItem[]> {
        return this.http.get<UrlItem[]>(`${this.apiUrl}/`)
    }

    create(payload: CreateUrlRequest): Observable<UrlItem> {
        return this.http.post<UrlItem>(`${this.apiUrl}/`, payload)
    }
}