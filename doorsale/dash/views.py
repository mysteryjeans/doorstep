from __future__ import unicode_literals

from doorsale.views import BaseView
from doorsale.decorators import staff_member_required


class DashBaseView(BaseView):
    """
    A base view class inherit by all dash views
    """
    style_name = 'dash'
    dash_template_name='dash/dash_base.html'

    def get_context_data(self, **kwargs):
        return super(DashBaseView, self).get_context_data(
            dash_template_name=self.dash_template_name,
            **kwargs)

    @classmethod
    def get_decorators(cls):
        """
        Applying common decorators for all views of dashboard

        Sequence of decorators applied to view is last in first out
        """
        
        # Decorators from extended classes 
        decorators = super(DashBaseView, cls).get_decorators()

        # Only allowing staff member to see dashboard
        decorators += [staff_member_required]
        
        return decorators


class IndexView(DashBaseView):
    """
    Dashboard index view
    """
    template_name = 'dash/dash_index.html'
