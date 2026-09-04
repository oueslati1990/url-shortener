import { Component, inject, output, signal } from '@angular/core';
import { UrlService } from '../../services/url.service';
import { FormControl, Validators } from '@angular/forms';
import { UrlItem } from '../../models/url.model';

@Component({
  selector: 'app-url-shortener',
  imports: [],
  templateUrl: './url-shortener.html',
  styleUrl: './url-shortener.scss',
})
export class UrlShortenerComponent {
  private urlService = inject(UrlService)

  isLoading = signal(false);
  error = signal<string | null>(null);
  lastCreated = signal<UrlItem | null>(null);

  urlCreated = output<UrlItem>();

  urlControl = new FormControl('', [
    Validators.required,
    Validators.pattern(/^https?:\/\/.+/),
  ]);

  submit(): void {
    if (this.urlControl.invalid) return;

    this.isLoading.set(true);
    this.error.set(null);

    this.urlService.create({ original_url: this.urlControl.value! }).subscribe({
      next: (url) => {
        this.lastCreated.set(url);
        this.urlCreated.emit(url);
        this.urlControl.reset();
        this.isLoading.set(false);
      },
      error: (err) => {
        this.error.set(err.error?.detail ?? 'Something went wrong. Is the backend running?');
        this.isLoading.set(false);
      },
    });
  }
}
