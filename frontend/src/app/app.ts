import { Component, viewChild } from '@angular/core';
import { UrlShortenerComponent } from './components/url-shortener/url-shortener';
import { UrlListComponent } from './components/url-list/url-list';
import { UrlItem } from './models/url.model';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [UrlShortenerComponent, UrlListComponent],
  template: `
    <header><h1>URL Shortener</h1></header>
    <main>
      <app-url-shortener (urlCreated)="onCreated($event)" />
      <app-url-list #list />
    </main>
  `,
  styles: [`
    header { background: #1d6cd8; color: #fff; padding: 1rem 1.5rem; }
    h1 { margin: 0; font-size: 1.25rem; }
    main { max-width: 860px; margin: 2rem auto; padding: 0 1rem; }
  `],
})
export class AppComponent {
  list = viewChild.required(UrlListComponent);

  onCreated(url: UrlItem): void {
    this.list().prepend(url);
  }
}