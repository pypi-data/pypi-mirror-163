# -*- coding: utf-8 -*-

"""
API Gateway: Cliente en Python
Copyright (C) SASCO SpA (https://sasco.cl)

Este programa es software libre: usted puede redistribuirlo y/o modificarlo
bajo los términos de la GNU Lesser General Public License (LGPL) publicada
por la Fundación para el Software Libre, ya sea la versión 3 de la Licencia,
o (a su elección) cualquier versión posterior de la misma.

Este programa se distribuye con la esperanza de que sea útil, pero SIN
GARANTÍA ALGUNA; ni siquiera la garantía implícita MERCANTIL o de APTITUD
PARA UN PROPÓSITO DETERMINADO. Consulte los detalles de la GNU Lesser General
Public License (LGPL) para obtener una información más detallada.

Debería haber recibido una copia de la GNU Lesser General Public License
(LGPL) junto a este programa. En caso contrario, consulte
<http://www.gnu.org/licenses/lgpl.html>.
"""

from .client import LibreDTE
from .exceptions import LibreDTEApiException


# clase base para las clases que consumen la API (wrappers)
class LibreDTEApiBase:

    auth = {}

    def __init__(self, api_token = None, api_url = None, **kwargs):
        # crear cliente de la API
        self.client = LibreDTE(api_token, api_url)
        # autenticación en SII mediante usuario y clave
        usuario_rut = kwargs.get('usuario_rut', None)
        usuario_clave = kwargs.get('usuario_clave', None)
        if usuario_rut is not None and usuario_clave is not None:
            self.auth = {
                'pass': {
            	    'rut': usuario_rut,
        	        'clave': usuario_clave
		        }
            }

    def get_auth_pass(self):
        if 'pass' not in self.auth:
            raise LibreDTEApiException('auth.pass missing')
        if 'rut' not in self.auth['pass']:
            raise LibreDTEApiException('auth.pass.rut missing')
        if self.auth['pass']['rut'] == '' or self.auth['pass']['rut'] is None:
            raise LibreDTEApiException('auth.pass.rut empty')
        if 'clave' not in self.auth['pass']:
            raise LibreDTEApiException('auth.pass.clave missing')
        if self.auth['pass']['clave'] == '' or self.auth['pass']['clave'] is None:
            raise LibreDTEApiException('auth.pass.clave empty')
        return self.auth
