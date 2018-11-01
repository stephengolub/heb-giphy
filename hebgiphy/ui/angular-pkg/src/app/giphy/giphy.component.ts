import { Component, Inject, Input, OnInit } from '@angular/core';
import {COMMA, ENTER} from '@angular/cdk/keycodes';
import {MatChipInputEvent, MatDialog, MatDialogRef, MAT_DIALOG_DATA} from '@angular/material';

import { ApiService } from '../api.service';

class Tag {
  name: string;
}
class Gif {
  giphy_embed_url = '';
  giphy_direct_url = '';
  giphy_url =  '';
  giphy_id = '';
  giphy_tags: Array<Tag> = [];
};

export interface DialogData {
  gif: Gif
}


@Component({
  selector: 'app-giphy',
  templateUrl: './giphy.component.html',
  styleUrls: ['./giphy.component.scss']
})
export class GiphyComponent implements OnInit {
  @Input() gif: Gif;
  @Input() zoomed = false;

  constructor(private api: ApiService, public dialog: MatDialog) {
    this.api = api;
  }

  ngOnInit() {
  }

  toggleFavorite() {
    if (this.isFavorite()) {
      return this.api.unfavorite(this.gif.giphy_id).subscribe();
    } else {
      return this.api.favorite(this.gif.giphy_id).subscribe();
    }
  }

  showTags() {
    this.dialog.open(TagDialog, {
      data: {
        gif: this.gif
      }
    });
  }

  zoom() {
    this.api.fetchFavorites().subscribe((faves) => {
      this.dialog.open(ZoomDialog, {
        data: {
          gif: this.gif
        }
      });
    });
  }

  isFavorite() {
    return this.api.isFavorite(this.gif.giphy_id);
  }
}

@Component({
  selector: 'zoom-gif-dialog',
  template: `<div class="zoom-gif"><app-giphy [gif]="data.gif" [zoomed]="true"></app-giphy></div>`
})
export class ZoomDialog {
  constructor(
    public dialogRef: MatDialogRef<ZoomDialog>,
    @Inject(MAT_DIALOG_DATA) public data: DialogData) {}

  onNoClick() {
    this.dialogRef.close();
  }
}

@Component({
  selector: 'tag-gif-dialog',
  templateUrl: 'tags.html'
})
export class TagDialog {
  visible = true;
  selectable = true;
  removable = true;
  addOnBlur = true;
  readonly separatorKeysCodes: number[] = [ENTER, COMMA];

  constructor(
    public dialogRef: MatDialogRef<ZoomDialog>,
    @Inject(MAT_DIALOG_DATA) public data: DialogData,
    private api: ApiService) {
      this.api = api;
    }

  onNoClick() {
    this.dialogRef.close();
  }

  saveTags() {
    const tags = this.data.gif.giphy_tags.map((tag) => tag.name);
    return this.api.saveTags(this.data.gif.giphy_id, tags).subscribe();;
  }

  add(event: MatChipInputEvent): void {
    const input = event.input;
    const value = event.value;

    // Add our fruit
    if ((value || '').trim()) {
      this.data.gif.giphy_tags.push({name: value.trim()});
    }

    // Reset the input value
    if (input) {
      input.value = '';
    }
    this.saveTags();
  }

  remove(tag: Tag): void {
    const index = this.data.gif.giphy_tags.indexOf(tag);

    if (index >= 0) {
      this.data.gif.giphy_tags.splice(index, 1);
    }
    this.saveTags();
  }
}
