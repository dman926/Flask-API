'''
Admin routes
'''

from flask import jsonify, request
from flask_restful_swagger_2 import Resource, swagger
from flask_jwt_extended import jwt_required, get_jwt_identity

from mongoengine.errors import DoesNotExist, FieldDoesNotExist, ValidationError, InvalidQueryError
from resources.errors import UnauthorizedError, InternalServerError, ResourceNotFoundError

from database.models import User, Page, Product, Order

from services.util_service import make_ngrams
from services.logging_service import writeWarningToLog

import datetime

class AdminApi(Resource):
	@swagger.doc({
		'tags': ['Admin'],
		'description': 'Get if the current user is admin',
		'responses': {
			'200': {
				'description': 'True if the user is admin, false otherwise'
			}
		}
	})
	@jwt_required()
	def get(self):
		try:
			user = User.objects.get(id=get_jwt_identity())
			return user.admin
		except UnauthorizedError:
			raise UnauthorizedError
		except Exception as e:
			writeWarningToLog('Unhandled exception in resources.admin.AdminApi get', e)
			raise InternalServerError

class AdminUsersApi(Resource):
	@swagger.doc({
		'tags': ['Admin', 'User'],
		'description': 'Get all users according to pagination criteria',
		'parameters': [
			{
				'name': 'page',
				'description': 'The page index',
				'in': 'query',
				'type': 'int',
				'schema': None,
				'required': False
			},
			{
				'name': 'size',
				'description': 'The page size',
				'in': 'query',
				'type': 'int',
				'schema': None,
				'required': False
			}
		],
		'responses': {
			'200': {
				'description': 'An array of User'
			}
		}
	})
	@jwt_required()
	def get(self):
		try:
			user = User.objects.get(id=get_jwt_identity())
			if not user.admin:
				raise UnauthorizedError
			page = int(request.args.get('page', 0))
			size = int(request.args.get('size', User.objects.count()))
			users = User.objects[page * size : page * size + size]
			return jsonify(list(map(lambda u: u.serialize(), users)))
		except UnauthorizedError:
			raise UnauthorizedError
		except Exception as e:
			writeWarningToLog('Unhandled exception in resources.admin.AdminUsersApi get', e)
			raise InternalServerError

class AdminUserApi(Resource):
	@swagger.doc({
		'tags': ['Admin', 'User'],
		'description': 'Get user',
		'parameters': [
			{
				'name': 'id',
				'description': 'The user id',
				'in': 'path',
				'type': 'object',
				'schema': None,
				'required': True
			}
		],
		'responses': {
			'200': {
				'description': 'The user'
			}
		}
	})
	@jwt_required()
	def get(self, id):
		try:
			user = User.objects.get(id=get_jwt_identity())
			if not user.admin:
				raise UnauthorizedError
			user = User.objects.get(id=id)
			return jsonify(user.serialize())
		except UnauthorizedError:
			raise UnauthorizedError
		except Exception as e:
			writeWarningToLog('Unhandled exception in resources.admin.AdminUserApi get', e)
			raise InternalServerError
	@swagger.doc({
		'tags': ['Admin', 'User'],
		'description': 'Update user',
		'parameters': [
			{
				'name': 'id',
				'description': 'The user id',
				'in': 'path',
				'type': 'object',
				'schema': None,
				'required': True
			}
		],
		'responses': {
			'200': {
				'description': 'User updated'
			}
		}
	})
	@jwt_required()
	def put(self, id):
		try:
			user = User.objects.get(id=get_jwt_identity())
			if not user.admin:
				raise UnauthorizedError
			user = User.objects.get(id=id)
			user.update(**request.get_json())
			return 'ok'
		except UnauthorizedError:
			raise UnauthorizedError
		except DoesNotExist:
			raise ResourceNotFoundError
		except Exception as e:
			writeWarningToLog('Unhandled exception in resources.admin.AdminUserApi put', e)
			raise InternalServerError
	@swagger.doc({
		'tags': ['Admin', 'User'],
		'description': 'Delete user',
		'parameters': [
			{
				'name': 'id',
				'description': 'The user id',
				'in': 'path',
				'type': 'object',
				'schema': None,
				'required': True
			}
		],
		'responses': {
			'200': {
				'description': 'User deleted'
			}
		}
	})
	@jwt_required()
	def delete(self, id):
		try:
			user = User.objects.get(id=get_jwt_identity())
			if not user.admin:
				raise UnauthorizedError
			user = User.objects.get(id=id)
			user.delete()
			return 'ok'
		except UnauthorizedError:
			raise UnauthorizedError
		except DoesNotExist:
			raise ResourceNotFoundError
		except Exception as e:
			writeWarningToLog('Unhandled exception in resources.admin.AdminUserApi delete', e)
			raise InternalServerError

class AdminUsersCountApi(Resource):
	@swagger.doc({
		'tags': ['Admin', 'User', 'Counter'],
		'description': 'Get the amount of users',
		'responses': {
			'200': {
				'description': 'The amount of users'
			}
		}
	})
	@jwt_required()
	def get(self):
		try:
			user = User.objects.get(id=get_jwt_identity())
			if not user.admin:
				raise UnauthorizedError
			return User.objects.count()
		except UnauthorizedError:
			raise UnauthorizedError
		except Exception as e:
			writeWarningToLog('Unhandled exception in resources.admin.AdminUsersCountApi get', e)
			raise InternalServerError

class AdminPagesApi(Resource):
	@swagger.doc({
		'tags': ['Admin', 'Page'],
		'description': 'Get all pages according to pagination criteria',
		'parameters': [
			{
				'name': 'page',
				'description': 'The page index',
				'in': 'query',
				'type': 'int',
				'schema': None,
				'required': False
			},
			{
				'name': 'size',
				'description': 'The page size',
				'in': 'query',
				'type': 'int',
				'schema': None,
				'required': False
			}
		],
		'responses': {
			'200': {
				'description': 'An array of Page'
			}
		}
	})
	@jwt_required()
	def get(self):
		try:
			user = User.objects.get(id=get_jwt_identity())
			if not user.admin:
				raise UnauthorizedError
			page = int(request.args.get('page', 0))
			size = int(request.args.get('size', Page.objects.count()))
			pages = Page.objects[page * size : page * size + size]
			return jsonify(list(map(lambda p: p.serialize(), pages)))
		except UnauthorizedError:
			raise UnauthorizedError
		except Exception as e:
			writeWarningToLog('Unhandled exception in resources.admin.AdminPagesApi get', e)
			raise InternalServerError
	@swagger.doc({
		'tags': ['Admin', 'Page'],
		'description': 'Create new Page',
		'responses': {
			'200': {
				'description': 'Page added'
			}
		}
	})
	@jwt_required()
	def post(self):
		try:
			user = User.objects.get(id=get_jwt_identity())
			if not user.admin:
				raise UnauthorizedError
			page = Page(**request.get_json(), author=user)
			page.save()
			return jsonify(page.serialize())
		except UnauthorizedError:
			raise UnauthorizedError
		except Exception as e:
			writeWarningToLog('Unhandled exception in resources.admin.AdminPagesApi post', e)
			raise InternalServerError

class AdminPageApi(Resource):
	@swagger.doc({
		'tags': ['Admin', 'Page'],
		'description': 'Get page',
		'parameters': [
			{
				'name': 'id',
				'description': 'The page id',
				'in': 'path',
				'type': 'string',
				'schema': None,
				'required': True
			}
		],
		'responses': {
			'200': {
				'description': 'The page'
			}
		}
	})
	@jwt_required()
	def get(self, id):
		try:
			user = User.objects.get(id=get_jwt_identity())
			if not user.admin:
				raise UnauthorizedError
			page = Page.objects.get(id=id)
			return jsonify(page.serialize())
		except UnauthorizedError:
			raise UnauthorizedError
		except DoesNotExist:
			raise ResourceNotFoundError
		except Exception as e:
			writeWarningToLog('Unhandled exception in resources.admin.AdminPostApi get', e)
			raise InternalServerError
	@swagger.doc({
		'tags': ['Admin', 'Page'],
		'description': 'Update page',
		'parameters': [
			{
				'name': 'id',
				'description': 'The page id',
				'in': 'path',
				'type': 'object',
				'schema': None,
				'required': True
			}
		],
		'responses': {
			'200': {
				'description': 'Page updated'
			}
		}
	})
	@jwt_required()
	def put(self, id):
		try:
			user = User.objects.get(id=get_jwt_identity())
			if not user.admin:
				raise UnauthorizedError
			page = Page.objects.get(id=id)
			page.update(**request.get_json())
			page.reload()
			page.modified = datetime.datetime.now
			page.generateNgrams()
			page.save()
			return 'ok'
		except UnauthorizedError:
			raise UnauthorizedError
		except Exception as e:
			writeWarningToLog('Unhandled exception in resources.admin.AdminPageApi put', e)
			raise InternalServerError
	@swagger.doc({
		'tags': ['Admin', 'Page'],
		'description': 'Delete page',
		'parameters': [
			{
				'name': 'id',
				'description': 'The page id',
				'in': 'path',
				'type': 'string',
				'schema': None,
				'required': True
			}
		],
		'responses': {
			'200': {
				'description': 'Page deleted'
			}
		}
	})
	@jwt_required()
	def delete(self, id):
		try:
			user = User.objects.get(id=get_jwt_identity())
			if not user.admin:
				raise UnauthorizedError
			Page.objects.get(id=id).delete()
			return 'ok'
		except UnauthorizedError:
			raise UnauthorizedError
		except DoesNotExist:
			raise ResourceNotFoundError
		except Exception as e:
			writeWarningToLog('Unhandled exception in resources.admin.AdminPageApi delete', e)
			raise InternalServerError

class AdminPagesCountApi(Resource):
	@swagger.doc({
		'tags': ['Admin', 'Page'],
		'description': 'Get the amount of pages',
		'responses': {
			'200': {
				'description': 'The amount of pages'
			}
		}
	})
	@jwt_required()
	def get(self):
		try:
			user = User.objects.get(id=get_jwt_identity())
			if not user.admin:
				raise UnauthorizedError
			return Page.objects.count()
		except UnauthorizedError:
			raise UnauthorizedError
		except Exception as e:
			writeWarningToLog('Unhandled exception in resources.admin.AdminPagesCountApi get', e)
			raise InternalServerError

class AdminPageSlugApi(Resource):
	@swagger.doc({
		'tags': ['Admin', 'Page', 'Validator'],
		'description': 'Get if this page slug is taken',
		'responses': {
			'200': {
				'description': 'If the slug is taken'
			}
		}
	})
	@jwt_required()
	def get(self):
		try:
			user = User.objects.get(id=get_jwt_identity())
			if not user.admin:
				raise UnauthorizedError
			Page.objects.get(slug=request.args.get('slug'))
			return False
		except DoesNotExist:
			return True
		except Exception as e:
			writeWarningToLog('Unhandled exception in resources.admin.AdminPageSlugApi get', e)
			raise InternalServerError

class AdminProductsApi(Resource):
	@swagger.doc({
		'tags': ['Admin', 'Product'],
		'description': 'Get all pages according to pagination criteria',
		'parameters': [
			{
				'name': 'page',
				'description': 'The page index',
				'in': 'query',
				'type': 'int',
				'schema': None,
				'required': False
			},
			{
				'name': 'size',
				'description': 'The page size',
				'in': 'query',
				'type': 'int',
				'schema': None,
				'required': False
			}
		],
		'responses': {
			'200': {
				'description': 'An array of Page'
			}
		}
	})
	@jwt_required()
	def get(self):
		try:
			user = User.objects.get(id=get_jwt_identity())
			if not user.admin:
				raise UnauthorizedError
			page = int(request.args.get('page', 0))
			size = int(request.args.get('size', User.objects.count()))
			products = Product.objects[page * size : page * size + size]
			return jsonify(list(map(lambda p: p.serialize(), products)))
		except UnauthorizedError:
			raise UnauthorizedError
		except Exception as e:
			writeWarningToLog('Unhandled exception in resources.admin.AdminProductsApi get', e)
			raise InternalServerError
	@swagger.doc({
		'tags': ['Admin', 'Product'],
		'description': 'Add new product',
		'parameters': [
			{
				'name': '',
				'description': 'A product object',
				'in': 'body',
				'type': 'object',
				'schema': None,
				'required': True
			}
		],
		'responses': {
			'200': {
				'description': 'Product added',
			}
		}
	})
	@jwt_required()
	def post(self):
		try:
			user = User.objects.get(id=get_jwt_identity())
			if not user.admin:
				raise UnauthorizedError
			product = Product(**request.get_json(), author=user)
			product.generateNgrams()
			product.save()
			return jsonify(product.serialize())
		except (FieldDoesNotExist, ValidationError):
			raise SchemaValidationError
		except UnauthorizedError:
			raise UnauthorizedError
		except Exception as e:
			writeWarningToLog('Unhandled exception in resources.admin.AdminProductsApi post', e)
			raise InternalServerError

class AdminProductApi(Resource):
	@swagger.doc({
		'tags': ['Admin', 'Product'],
		'description': 'Get the product',
		'parameters': [
			{
				'name': 'id',
				'description': 'The item id',
				'in': 'path',
				'type': 'string',
				'required': True
			}
		],
		'responses': {
			'200': {
				'description': 'The product',
			}
		}
	})
	@jwt_required()
	def get(self, id):
		try:
			user = User.objects.get(id=get_jwt_identity())
			if not user.admin:
				raise UnauthorizedError
			product = Product.objects.get(id=id)
			return jsonify(product.serialize())
		except UnauthorizedError:
			raise UnauthorizedError
		except Exception as e:
			writeWarningToLog('Unhandled exception in resources.admin.AdminProductApi get', e)
			raise InternalServerError
	@swagger.doc({
		'tags': ['Admin', 'Product'],
		'description': 'Update the product',
		'parameters': [
			{
				'name': 'id',
				'description': 'The item id',
				'in': 'path',
				'type': 'string',
				'required': True
			}
		],
		'responses': {
			'200': {
				'description': 'Product updated',
			}
		}
	})
	@jwt_required()
	def put(self, id):
		try:
			user = User.objects.get(id=get_jwt_identity())
			if not user.admin:
				raise UnauthorizedError
			product = Product.objects.get(id=id)
			product.update(**request.get_json())
			product.reload()
			if product.price and product.price < 0:
				product.price = 0
			product.modified = datetime.datetime.now
			product.generateNgrams()
			product.save()
			return 'ok', 200
		except InvalidQueryError:
			raise SchemaValidationError
		except UnauthorizedError:
			raise UnauthorizedError
		except Exception as e:
			writeWarningToLog('Unhandled exception in resources.admin.AdminProductApi put', e)
			raise InternalServerError
	@swagger.doc({
		'tags': ['Admin', 'Product'],
		'description': 'Delete the product',
		'parameters': [
			{
				'name': 'id',
				'description': 'The item id',
				'in': 'path',
				'type': 'string',
				'required': True
			}
		],
		'responses': {
			'200': {
				'description': 'Product deleted',
			}
		}
	})
	@jwt_required()
	def delete(self, id):
		try:
			user = User.objects.get(id=get_jwt_identity())
			if not user.admin:
				raise UnauthorizedError
			product = Product.objects.get(id=id)
			product.status = 'deactivated'
			product.save()
			return 'ok', 200
		except UnauthorizedError:
			raise UnauthorizedError
		except Exception as e:
			writeWarningToLog('Unhandled exception in resources.admin.AdminProductApi delete', e)
			raise InternalServerError

class AdminProductCountApi(Resource):
	@swagger.doc({
		'tags': ['Admin', 'Product', 'Counter'],
		'description': 'Get the number of products',
		'parameters': [
			{
				'name': 'status',
				'description': 'A list of possible statuses',
				'in': 'query',
				'type': 'string',
				'required': False
			}
		],
		'responses': {
			'200': {
				'description': 'The number of products',
			}
		}
	})
	@jwt_required()
	def get(self):
		try:
			user = User.objects.get(id=get_jwt_identity())
			if not user.admin:
				raise UnauthorizedError
			return Product.objects(status__in=list(request.args['status'])).count()
		except UnauthorizedError:
			return UnauthorizedError
		except Exception as e:
			writeWarningToLog('Unhandled exception in resources.admin.AdminProductCountApi get', e)
			raise InternalServerError

class AdminProductSlugAvailableApi(Resource):
	@swagger.doc({
		'tags': ['Admin', 'Product', 'Validator'],
		'description': 'Get if this product slug is taken',
		'parameters': [
			{
				'name': 'slug',
				'description': 'The product slug',
				'in': 'body',
				'schema': None,
				'type': 'string',
				'required': True
			}
		],
		'responses': {
			'200': {
				'description': 'If the product slug is taken',
			}
		}
	})
	@jwt_required()
	def get(self):
		try:
			user = User.objects.get(id=get_jwt_identity())
			if not user.admin:
				raise UnauthorizedError
			Product.objects.get(slug=request.args.get('slug'))
			return False
		except DoesNotExist:
			return True
		except Exception as e:
			writeWarningToLog('Unhandled exception in resources.admin.AdminProductSlugAvailableApi get', e)
			raise InternalServerError

class AdminCouponsApi(Resource):
	@swagger.doc({
		'tags': ['Admin', 'Coupon'],
		'description': 'Get all coupons according to pagination criteria',
		'parameters': [
			{
				'name': 'page',
				'description': 'The page index',
				'in': 'query',
				'type': 'int',
				'schema': None,
				'required': False
			},
			{
				'name': 'size',
				'description': 'The page size',
				'in': 'query',
				'type': 'int',
				'schema': None,
				'required': False
			}
		],
		'responses': {
			'200': {
				'description': 'An array of Coupon'
			}
		}
	})
	@jwt_required()
	def get(self):
		try:
			user = User.objects.get(id=get_jwt_identity())
			if not user.admin:
				raise UnauthorizedError
			page = int(request.args.get('page', 0))
			size = int(request.args.get('size', User.objects.count()))
			coupons = Coupon.objects[page * size : page * size + size]
			return jsonify(list(map(lambda c: c.serialize(), coupons)))
		except UnauthorizedError:
			raise UnauthorizedError
		except Exception as e:
			writeWarningToLog('Unhandled exception in resources.admin.AdminCouponsApi get', e)
			raise InternalServerError
	@swagger.doc({
		'tags': ['Admin', 'Coupon'],
		'description': 'Add new coupon',
		'responses': {
			'200': {
				'description': 'Coupon added',
			}
		}
	})
	@jwt_required()
	def post(self):
		try:
			user = User.objects.get(id=get_jwt_identity())
			if not user.admin:
				raise UnauthorizedError
			coupon = Product(**request.get_json(), author=user)
			coupon.save()
			return jsonify(coupon.serialize())
		except (FieldDoesNotExist, ValidationError):
			raise SchemaValidationError
		except UnauthorizedError:
			raise UnauthorizedError
		except Exception as e:
			writeWarningToLog('Unhandled exception in resources.admin.AdminCouponsApi post', e)
			raise InternalServerError

class AdminCouponApi(Resource):
	@swagger.doc({
		'tags': ['Admin', 'Coupon'],
		'description': 'Get the coupon',
		'parameters': [
			{
				'name': 'id',
				'description': 'The coupon id',
				'in': 'path',
				'type': 'string',
				'required': True
			}
		],
		'responses': {
			'200': {
				'description': 'The coupon',
			}
		}
	})
	def get(self, id):
		try:
			user = User.objects.get(id=get_jwt_identity())
			if not user.admin:
				raise UnauthorizedError
			coupon = Coupon.objects.get(id=id)
			return jsonify(coupon.serialize())
		except UnauthorizedError:
			raise UnauthorizedError
		except Exception as e:
			writeWarningToLog('Unhandled exception in resources.admin.AdminCouponApi get', e)
			raise InternalServerError
	@swagger.doc({
		'tags': ['Admin', 'Coupon'],
		'description': 'Update the coupon',
		'parameters': [
			{
				'name': 'id',
				'description': 'The coupon id',
				'in': 'path',
				'type': 'string',
				'required': True
			}
		],
		'responses': {
			'200': {
				'description': 'Coupon updated',
			}
		}
	})
	@jwt_required()
	def put(self, id):
		try:
			user = User.objects.get(id=get_jwt_identity())
			if not user.admin:
				raise UnauthorizedError
			coupon = Coupon.objects.get(id=id)
			coupon.update(**request.get_json())
			coupon.reload()
			coupon.modified = datetime.datetime.now
			coupon.generateNgrams()
			coupon.save()
			return 'ok', 200
		except InvalidQueryError:
			raise SchemaValidationError
		except UnauthorizedError:
			raise UnauthorizedError
		except Exception as e:
			writeWarningToLog('Unhandled exception in resources.admin.AdminProductApi put', e)
			raise InternalServerError
	@swagger.doc({
		'tags': ['Admin', 'Coupon'],
		'description': 'Delete the coupon',
		'parameters': [
			{
				'name': 'id',
				'description': 'The coupon id',
				'in': 'path',
				'type': 'string',
				'required': True
			}
		],
		'responses': {
			'200': {
				'description': 'Coupon deleted',
			}
		}
	})
	@jwt_required()
	def delete(self, id):
		try:
			user = User.objects.get(id=get_jwt_identity())
			if not user.admin:
				raise UnauthorizedError
			coupon = Coupon.objects.get(id=id)
			coupon.status = 'deactivated'
			coupon.save()
			return 'ok', 200
		except UnauthorizedError:
			raise UnauthorizedError
		except Exception as e:
			writeWarningToLog('Unhandled exception in resources.admin.AdminCouponApi delete', e)
			raise InternalServerError

class AdminCouponCountApi(Resource):
	@swagger.doc({
		'tags': ['Admin', 'Coupon', 'Counter'],
		'description': 'Get the number of coupons',
		'parameters': [
			{
				'name': 'status',
				'description': 'A list of possible statuses',
				'in': 'query',
				'type': 'string',
				'required': True
			}
		],
		'responses': {
			'200': {
				'description': 'The number of coupons',
			}
		}
	})
	def get(self):
		try:
			user = User.objects.get(id=get_jwt_identity())
			if not user.admin:
				raise UnauthorizedError
			return Coupon.objects(status__in=list(request.args['status'])).count()
		except UnauthorizedError:
			return UnauthorizedError
		except Exception as e:
			writeWarningToLog('Unhandled exception in resources.admin.AdminCouponCountApi get', e)
			raise InternalServerError

class AdminCouponSlugAvailableApi(Resource):
	@swagger.doc({
		'tags': ['Admin', 'Coupon', 'Validator'],
		'description': 'Get if this coupon slug is taken',
		'parameters': [
			{
				'name': 'slug',
				'description': 'The coupon slug',
				'in': 'body',
				'schema': None,
				'type': 'string',
				'required': True
			}
		],
		'responses': {
			'200': {
				'description': 'If the coupon slug is taken',
			}
		}
	})
	@jwt_required()
	def get(self):
		try:
			user = User.objects.get(id=get_jwt_identity())
			if not user.admin:
				raise UnauthorizedError
			Coupon.objects.get(slug=request.args.get('slug'))
			return False
		except DoesNotExist:
			return True
		except Exception as e:
			writeWarningToLog('Unhandled exception in resources.admin.AdminProductSlugAvailableApi get', e)
			raise InternalServerError

class AdminOrdersApi(Resource):
	@swagger.doc({
		'tags': ['Admin', 'Order'],
		'description': 'Get all orders according to pagination criteria',
		'parameters': [
			{
				'name': 'page',
				'description': 'The page index',
				'in': 'query',
				'type': 'int',
				'schema': None,
				'required': False
			},
			{
				'name': 'size',
				'description': 'The page size',
				'in': 'query',
				'type': 'int',
				'schema': None,
				'required': False
			}
		],
		'responses': {
			'200': {
				'description': 'An array of Order'
			}
		}
	})
	@jwt_required()
	def get(self):
		try:
			user = User.objects.get(id=get_jwt_identity())
			if not user.admin:
				raise UnauthorizedError
			page = int(request.args.get('page', 0))
			size = int(request.args.get('size', User.objects.count()))
			orders = Order.objects[page * size : page * size + size]
			return jsonify(list(map(lambda o: o.serialize(), orders)))
		except UnauthorizedError:
			raise UnauthorizedError
		except Exception as e:
			writeWarningToLog('Unhandled exception in resources.admin.AdminOrdersApi get', e)
			raise InternalServerError

class AdminOrderApi(Resource):
	@swagger.doc({
		'tags': ['Admin', 'Order'],
		'description': 'Get the order',
		'parameters': [
			{
				'name': 'id',
				'description': 'The order id',
				'in': 'path',
				'type': 'string',
				'required': True
			}
		],
		'responses': {
			'200': {
				'description': 'The order',
			}
		}
	})
	def get(self, id):
		try:
			user = User.objects.get(id=get_jwt_identity())
			if not user.admin:
				raise UnauthorizedError
			order = Order.objects.get(id=id)
			return jsonify(order.serialize())
		except UnauthorizedError:
			raise UnauthorizedError
		except Exception as e:
			writeWarningToLog('Unhandled exception in resources.admin.AdminOrderApi get', e)
			raise InternalServerError
	@swagger.doc({
		'tags': ['Admin', 'Order'],
		'description': 'Update the order',
		'parameters': [
			{
				'name': 'id',
				'description': 'The order id',
				'in': 'path',
				'type': 'string',
				'required': True
			}
		],
		'responses': {
			'200': {
				'description': 'Order updated',
			}
		}
	})
	@jwt_required()
	def put(self, id):
		try:
			user = User.objects.get(id=get_jwt_identity())
			if not user.admin:
				raise UnauthorizedError
			order = Order.objects.get(id=id)
			order.update(**request.get_json())
			order.reload()
			order.modified = datetime.datetime.now
			order.save()
			return 'ok', 200
		except InvalidQueryError:
			raise SchemaValidationError
		except UnauthorizedError:
			raise UnauthorizedError
		except Exception as e:
			writeWarningToLog('Unhandled exception in resources.admin.AdminOrderApi put', e)
			raise InternalServerError
	@swagger.doc({
		'tags': ['Admin', 'Coupon'],
		'description': 'Delete the coupon',
		'parameters': [
			{
				'name': 'id',
				'description': 'The coupon id',
				'in': 'path',
				'type': 'string',
				'required': True
			}
		],
		'responses': {
			'200': {
				'description': 'Coupon deleted',
			}
		}
	})
	@jwt_required()
	def delete(self, id):
		try:
			user = User.objects.get(id=get_jwt_identity())
			if not user.admin:
				raise UnauthorizedError
			Order.objects.get(id=id).delete()
			return 'ok', 200
		except UnauthorizedError:
			raise UnauthorizedError
		except Exception as e:
			writeWarningToLog('Unhandled exception in resources.admin.AdminOrderApi delete', e)
			raise InternalServerError

class AdminOrderCountApi(Resource):
	@swagger.doc({
		'tags': ['Admin', 'Order', 'Counter'],
		'description': 'Get the number of orders',
		'parameters': [
			{
				'name': 'status',
				'description': 'A list of possible statuses',
				'in': 'query',
				'type': 'string',
				'required': True
			}
		],
		'responses': {
			'200': {
				'description': 'The number of orders',
			}
		}
	})
	def get(self):
		try:
			user = User.objects.get(id=get_jwt_identity())
			if not user.admin:
				raise UnauthorizedError
			return Order.objects(status__in=list(request.args['status'])).count()
		except UnauthorizedError:
			return UnauthorizedError
		except Exception as e:
			writeWarningToLog('Unhandled exception in resources.admin.AdminOrderCountApi get', e)
			raise InternalServerError