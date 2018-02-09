from __future__ import unicode_literals

from django.db import models
from django.core.exceptions import ImproperlyConfigured


class SysConfig(models.Model):
    """
    System configuration parameters class

    Configuration paramters such as Page Size, Support Email and etc... will be store in database
    """

    name = models.CharField(max_length=100, unique=True)
    value = models.CharField(max_length=250, blank=True)
    description = models.CharField(max_length=500)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)

    class Meta:
        db_table = 'doorstep_sys_config'
        verbose_name = 'System Config'
        verbose_name_plural = 'System Configs'
        ordering = ['id']

    @classmethod
    def get_config(cls, name):
        """
        Returns System Configuration value defined in database against name
        """
        sys_configs = SysConfig.get_configs()
        if name in sys_configs:
            return sys_configs[name]

        raise ImproperlyConfigured('"%s" does not found, it should be defined it in System Configs' % name)

    @classmethod
    def get_configs(cls):
        """
        Returns System Configs dictionary from database

        Configurations will be loaded when first time demanded
        """
        if not hasattr(cls, 'sys_configs'):
            cls.sys_configs = dict((sys_config.name, sys_config.value) for sys_config in cls.objects.all())

        return cls.sys_configs
