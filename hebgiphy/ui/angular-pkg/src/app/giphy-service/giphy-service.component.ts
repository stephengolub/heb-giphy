import { Component, Inject, OnInit } from '@angular/core';
import {MatDialog, MatDialogRef, MAT_DIALOG_DATA} from '@angular/material';

import { ApiService } from '../api.service';
import { GiphyComponent } from '../giphy/giphy.component';

class Result {
  data: [];
  pagination: {
    total_count: number;
  }
}

export interface DialogData {
  favorites: []
}

@Component({
  selector: 'app-giphy-service',
  templateUrl: './giphy-service.component.html',
  styleUrls: ['./giphy-service.component.scss']
})
export class GiphyServiceComponent implements OnInit {
  displayedData = [];
  totalImages = 0;
  morePages = true;
  loading = false;
  query = '';

  constructor (private api: ApiService, public dialog: MatDialog) {
    this.api = api;
  }

  ngOnInit() {
    const queryParams = new URLSearchParams(window.location.search);
    this.query = queryParams.get('q')
    if (this.query && this.query != '') {
      this.load();
    }
  }

  onEnter(value: string) {
    this.query = value;
    this.displayedData = [];
    this.load();
  }

  load(offset: number = 0) {
    this.loading = true;
		this.api.search(this.query, offset).subscribe((results: Result) => {
      this.addToDisplay(results);
      this.loading = false;
    });
  }

  addToDisplay(results: Result) {
    this.displayedData = this.displayedData.concat(results.data);
    this.totalImages = results.pagination.total_count;
    if (results && results.data && results.pagination) {
      this.morePages = this.displayedData.length < results.pagination.total_count;
    }
  }

  loadMore() {
    if (this.morePages) {
      this.load(this.displayedData.length);
    }
  }

  showFavorites() {
    this.api.fetchFavorites().subscribe((faves) => {
      this.dialog.open(FavoriteDialog, {
        width: '75%',
        height: '75%',
        data: {
          favorites: faves
        }
      });
    });
  }
}

@Component({
  selector: 'favorites-dialog',
  templateUrl: 'favorites-dialog.html'
})
export class FavoriteDialog {
  constructor(
    public dialogRef: MatDialogRef<FavoriteDialog>,
    @Inject(MAT_DIALOG_DATA) public data: DialogData) {}

  onNoClick() {
    this.dialogRef.close();
  }
}
