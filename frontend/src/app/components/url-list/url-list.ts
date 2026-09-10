import { Component, inject, OnInit, signal } from '@angular/core';
import { DatePipe } from '@angular/common';
import { UrlService } from '../../services/url.service';
import { UrlItem } from '../../models/url.model';

@Component({
  selector: 'app-url-list',
  imports: [DatePipe],
  templateUrl: './url-list.html',
  styleUrl: './url-list.scss',
})
export class UrlListComponent implements OnInit {
  private urlService = inject(UrlService);

  urls = signal<UrlItem[]>([]);
  isLoading = signal(true);

  ngOnInit(): void {
    this.load();
  }

  load(): void {
    this.isLoading.set(true);
    this.urlService.getAll().subscribe({
      next: (urls) => {
        this.urls.set(urls);
        this.isLoading.set(false);
      },
      error: () => this.isLoading.set(false),
    });
  }

  /** Called by parent to optimistically add a new URL without a full reload */
  prepend(url: UrlItem): void {
    this.urls.update((prev) => [url, ...prev]);
  }
}
