import logging
from spaceone.core.handler import BaseMutationHandler

_LOGGER = logging.getLogger(__name__)


class SpaceONEMutationHandler(BaseMutationHandler):

    def request(self, params):
        scope = self.transaction.get_meta('authorization.scope')
        role_type = self.transaction.get_meta('authorization.role_type')
        domain_id = self.transaction.get_meta('domain_id')

        if self._check_mutation(scope, role_type):
            params = self._append_parameter(params)

        if role_type in ['DOMAIN', 'PROJECT', 'USER']:
            params['domain_id'] = domain_id

        return params

    @staticmethod
    def _check_mutation(scope, role_type):
        if scope == 'DOMAIN':
            if role_type in ['DOMAIN', 'PROJECT', 'USER']:
                return True
        elif scope == 'PROJECT':
            if role_type in ['PROJECT', 'USER']:
                return True
        elif scope == 'USER':
            if role_type == 'USER':
                return True

        return False

    def _append_parameter(self, params):
        append_parameter = self.transaction.get_meta('mutation.append_parameter', {})
        if isinstance(append_parameter, dict):
            for key, value in append_parameter.items():
                if key not in params:
                    if isinstance(value, dict):
                        meta_key = value.get('meta')
                        data = value.get('data')

                        if meta_key and data:
                            params[key] = []

                            meta_value = self.transaction.get_meta(meta_key)
                            if isinstance(meta_value, list):
                                params[key] += meta_value
                            else:
                                params[key].append(meta_value)

                            if data:
                                params[key] += data

                        elif meta_key:
                            params[key] = self.transaction.get_meta(meta_key)
                        elif data:
                            params[key] = data

                    else:
                        params[key] = self.transaction.get_meta(value)

        return params
