from flask import abort, url_for, redirect, request, flash

from flask_admin.contrib.sqla import ModelView
from flask_admin.form import SecureForm
from flask_security import current_user


# Create customized model view class
class BaseAdminModelView(ModelView):
    form_base_class = SecureForm
    form_excluded_columns = ('created_at', 'deleted_at', 'deleted', 'updated_at')
    column_display_pk = True

    def delete_model(self, model):
        if model.deleted:
            flash('Model is already deleted!')
            return
        model.soft_delete()
        self.session.commit()

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('superuser'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect auth when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))


class ImmutableAdminView(BaseAdminModelView):
    can_create = False
    can_edit = False
    can_delete = False


def init(admin):
    pass
