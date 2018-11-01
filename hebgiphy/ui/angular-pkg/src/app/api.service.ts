import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Subject } from 'rxjs';
import { Cacheable, CacheBuster } from 'ngx-cacheable';

const favoriteNotifier = new Subject();

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  csrf_token = '';
  public favorites = [];
  constructor(private http: HttpClient) {
    this.csrf_token = (<HTMLInputElement>document.querySelector('[name=csrfmiddlewaretoken]')).value;
  }

  search(query: string, offset: number = 0) {
    const opts = {
      params: new HttpParams().set('q', query).set('offset', offset.toString())
    };
    return this.http.get('/gifs/search', opts);
  }

  @CacheBuster({
    cacheBusterNotifier: favoriteNotifier
  })
  favorite(giphyId: string) {
    return this.http.post('/gifs/favorite/' + giphyId, {});
  }

  @CacheBuster({
    cacheBusterNotifier: favoriteNotifier
  })
  unfavorite(giphyId: string) {
    return this.http.delete('/gifs/favorite/' + giphyId, {});
  }

  @Cacheable({
    cacheBusterObserver: favoriteNotifier
  })
  fetchFavorites() {
    return this.http.get('/gifs/favorites');
  }

  getFavorites() {
    return this.fetchFavorites().subscribe((results: Array<any>) => {
      this.favorites = results;
      return this.favorites;
    });
  }

  isFavorite(giphyId) {
    this.getFavorites();
    return this.favorites.some((gif) => gif.giphy_id === giphyId);
  }

  @CacheBuster({
    cacheBusterNotifier: favoriteNotifier
  })
  saveTags(giphyId: string, tagList: Array<string>) {
    return this.http.post('/gifs/tags/' + giphyId, tagList);
  }
}
