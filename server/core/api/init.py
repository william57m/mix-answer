from core.api import BaseRequestHandler


class InitHandler(BaseRequestHandler):

    async def get(self):
        ret = {
            'features': {
                'ldap_enabled': self.application.config.getboolean('ldap', 'enabled') or False
            }
        }

        if self.user:
            ret['user'] = self.user.to_dict()

        self.write(ret)
        self.finish()
