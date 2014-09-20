from __future__ import unicode_literals

from django.db import models


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
        db_table = 'doorsale_sys_config'
        verbose_name = 'System Config'
        verbose_name_plural = 'System Configs'
        ordering = ['id']
