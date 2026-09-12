import { Component, inject, output, signal } from '@angular/core';
import { ReactiveFormsModule, FormGroup, FormControl, Validators } from '@angular/forms';
import { UrlService } from '../../services/url.service';
import { UrlItem } from '../../models/url.model';

@Component({
  selector: 'app-url-shortener',
  imports: [ReactiveFormsModule],
  templateUrl: './url-shortener.html',
  styleUrl: './url-shortener.scss',
})
export class UrlShortenerComponent {
  private urlService = inject(UrlService);

  isLoading = signal(false);
  error = signal<string | null>(null);
  lastCreated = signal<UrlItem | null>(null);

  urlCreated = output<UrlItem>();

  urlForm = new FormGroup({
    url: new FormControl('', [
      Validators.required,
      Validators.pattern(/^https?:\/\/.+/),
    ]),
  });

  get urlControl() { return this.urlForm.controls.url; }

  submit(): void {
    if (this.urlForm.invalid) return;

    this.isLoading.set(true);
    this.error.set(null);

    this.urlService.create({ original_url: this.urlControl.value! }).subscribe({
      next: (url) => {
        this.lastCreated.set(url);
        this.urlCreated.emit(url);
        this.urlForm.reset();
        this.isLoading.set(false);
      },
      error: (err) => {
        this.error.set(err.error?.detail ?? 'Something went wrong. Is the backend running?');
        this.isLoading.set(false);
      },
    });
  }
}
