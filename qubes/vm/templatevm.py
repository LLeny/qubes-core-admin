#!/usr/bin/python2 -O
# vim: fileencoding=utf-8

import qubes
import qubes.config
import qubes.vm.qubesvm

class TemplateVM(qubes.vm.qubesvm.QubesVM):
    '''Template for AppVM'''

    dir_path_prefix = qubes.config.system_path['qubes_templates_dir']

    @property
    def rootcow_img(self):
        '''COW image'''
        return self.storage.rootcow_img

    @property
    def appvms(self):
        for vm in self.app.domains:
            if hasattr(vm, 'template') and vm.template is self:
                yield vm

    def __init__(self, *args, **kwargs):
        assert 'template' not in kwargs, "A TemplateVM can not have a template"
        super(TemplateVM, self).__init__(*args, **kwargs)

        # Some additional checks for template based VM
        # TODO find better way
#       assert self.root_img is not None, "Missing root_img for standalone VM!"


    def clone_disk_files(self, src):
        super(TemplateVM, self).clone_disk_files(src)

        # Create root-cow.img
        self.commit_changes()


    def commit_changes(self):
        '''Commit changes to template'''
        self.log.debug('commit_changes()')

        if not self.app.vmm.offline_mode:
            assert not self.is_running(), \
                'Attempt to commit changes on running Template VM!'

        self.log.info(
            'Commiting template update; COW: {}'.format(self.rootcow_img))
        self.storage.commit_template_changes()
