import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { Product } from 'src/app/models/product';
import { CartService } from 'src/app/payment/cart/cart.service';
import { Review } from 'src/app/models/review';
import { ProductService } from '../product.service';
import { FormControl, FormGroup, Validators } from '@angular/forms';

interface PageEvent {
	length: number;
	pageIndex: number;
	pageSize: number;
	previousPageIndex?: number;
}

@Component({
	selector: 'app-product',
	templateUrl: './product.component.html',
	styleUrls: ['./product.component.scss']
})
export class ProductComponent implements OnInit {

	loaded: boolean;
	product: Product | undefined;

	selectedImg: number;
	reviews: Review[];
	reviewAllowed: boolean;
	reviewForm: FormGroup;
	reviewPageEvent: PageEvent;
	reviewCount: number;

	constructor(private productService: ProductService, private router: Router, public cartService: CartService) {
		this.loaded = false;
		this.selectedImg = 0;
		this.reviews = [];
		this.reviewAllowed = false;
		this.reviewForm = new FormGroup({
			score: new FormControl('', [Validators.required]),
			review: new FormControl('')
		});
		this.reviewPageEvent = {
			length: 0,
			pageIndex: 0,
			pageSize: 10,
			previousPageIndex: 0
		};
		this.reviewCount = 0;
	}

	ngOnInit(): void {
		this.productService.getProduct(this.router.url.substr(5)).toPromise().then(product => {
			this.product = product;
			this.loaded = true;
			this.productService.reviewAllowed(this.product.id!).toPromise().then(allowed => {
				this.reviewAllowed = allowed;
			});
			this.productService.getReviewCount(this.product.id!).toPromise().then(count => this.reviewCount = count);
			this.fetchReviews();
		}).catch(err => this.loaded = true);
	}

	ratingUpdated(rating: number): void {
		this.reviewForm.get('score')!.setValue(rating);
	}

	submitReview(): void {
		if (this.reviewForm.valid) {
			const review: Review = {
				product: this.product!.id!,
				score: this.reviewForm.get('score')!.value,
				review: this.reviewForm.get('review')!.value
			};
			this.productService.submitReview(review).toPromise().then(review => {
				if (review) {
					this.reviews.unshift(review);
					this.product!.totalReviews!++;
				}
			})
		}
	}

	get shownReviews(): Review[] {
		const index = this.reviewPageEvent.pageIndex;
		const size = this.reviewPageEvent.pageSize;
		return this.reviews.slice(index * size, index * size + size);
	}

	fetchReviews(event?: PageEvent): void {
		if (event) {
			this.reviewPageEvent = event;
		}
		this.loaded = false;
		this.productService.getReviews(this.product!.id!, this.reviewPageEvent.pageIndex, this.reviewPageEvent.pageSize).toPromise().then(reviews => {
			this.reviews = this.reviews.concat(reviews);
			this.loaded = true;
		}).catch(err => this.loaded = true);
	}

}
