'''
API Endpoints
'''

from .auth import SignupApi, LoginApi, ForgotPassword, ResetPassword, TokenRefresh, CheckPassword, UserApi, TwoFactorApi
from .file import UploaderApi, MediaApi, SingleMediaApi

from .page import PagesApi, PageApi
from .product import ProductsApi, ProductApi

from .admin import AdminApi, AdminUsersApi, AdminUserApi, AdminUsersCountApi, AdminPagesApi, AdminPageApi, AdminPagesCountApi, AdminPageSlugApi, AdminProductsApi, AdminProductApi, AdminCountApi, AdminProductSlugAvailableApi

import resources.sockets

def initialize_routes(api, base):
	api.add_resource(SignupApi, base + 'auth/signup')
	api.add_resource(LoginApi, base + 'auth/login')
	api.add_resource(ForgotPassword, base + 'auth/forgot')
	api.add_resource(ResetPassword, base + 'auth/reset')
	api.add_resource(TokenRefresh, base + 'auth/refresh')
	api.add_resource(CheckPassword, base + 'auth/checkPassword')
	api.add_resource(UserApi, base + 'auth/user')
	api.add_resource(TwoFactorApi, base + 'auth/2fa')

	api.add_resource(UploaderApi, base + 'file/uploader')
	api.add_resource(MediaApi, base + 'file/media')
	api.add_resource(SingleMediaApi, base + 'file/media/<filename>')

	api.add_resource(PagesApi, base + 'page/pages')
	api.add_resource(PageApi, base + 'page/page')

	api.add_resource(AdminApi, base + 'admin/admin')
	api.add_resource(AdminUsersApi, base + 'admin/users')
	api.add_resource(AdminUserApi, base + 'admin/user/<id>')
	api.add_resource(AdminUsersCountApi, base + 'admin/users/count')
	api.add_resource(AdminPagesApi, base + 'admin/pages')
	api.add_resource(AdminPageApi, base + 'admin/page/<id>')
	api.add_resource(AdminPagesCountApi, base + 'admin/pages/count')
	api.add_resource(AdminPageSlugApi, base + 'admin/pages/slugTaken')
	api.add_resource(AdminProductsApi, base + 'admin/products')
	api.add_resource(AdminProductApi, base + 'admin/product/<id>')
	api.add_resource(AdminProductsCountApi, base + 'admin/products/count')
	api.add_resource(AdminProductSlugAvailableApi, base + 'admin/products/slugTaken')