# coding=utf-8
'''
	Copyright (C) 2012  Juho Vähä-Herttua

	This library is free software; you can redistribute it and/or
	modify it under the terms of the GNU Lesser General Public
	License as published by the Free Software Foundation; either
	version 2.1 of the License, or (at your option) any later version.

	This library is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
	Lesser General Public License for more details.
'''

import os
import sys
import platform

from ctypes import *

audio_init_prototype =        CFUNCTYPE(py_object, c_void_p, c_int, c_int, c_int)
audio_set_volume_prototype =  CFUNCTYPE(None, c_void_p, c_void_p, c_float)
audio_process_prototype =     CFUNCTYPE(None, c_void_p, c_void_p, c_void_p, c_int)
audio_flush_prototype =       CFUNCTYPE(None, c_void_p, c_void_p)
audio_destroy_prototype =     CFUNCTYPE(None, c_void_p, c_void_p)

class RaopNativeCallbacks(Structure):
	_fields_ = [("cls",               py_object),
	            ("audio_init",        audio_init_prototype),
	            ("audio_set_volume",  audio_set_volume_prototype),
	            ("audio_process",     audio_process_prototype),
	            ("audio_flush",       audio_flush_prototype),
	            ("audio_destroy",     audio_destroy_prototype)]

def LoadShairplay(path):
	if sys.maxsize < 2**32:
		libname = "shairplay32"
	else:
		libname = "shairplay64"

	if platform.system() == "Windows":
		libname = libname + ".dll"
	elif platform.system() == "Darwin":
		libname = "lib" + libname + ".dylib"
	else:
		libname = "lib" + libname + ".so"

	try:
		fullpath = os.path.join(path, libname)
		libshairplay = cdll.LoadLibrary(fullpath)
	except:
		raise RuntimeError("Couldn't load shairplay library " + libname)

	# Initialize dnssd related functions
	libshairplay.dnssd_init.restype = c_void_p
	libshairplay.dnssd_init.argtypes = [POINTER(c_int)]
	libshairplay.dnssd_register_raop.restype = c_int
	libshairplay.dnssd_register_raop.argtypes = [c_void_p, c_char_p, c_ushort, POINTER(c_char), c_int]
	libshairplay.dnssd_register_airplay.restype = c_int
	libshairplay.dnssd_register_airplay.argtypes = [c_void_p, c_char_p, c_ushort, POINTER(c_char), c_int]
	libshairplay.dnssd_unregister_raop.restype = None
	libshairplay.dnssd_unregister_raop.argtypes = [c_void_p]
	libshairplay.dnssd_unregister_airplay.restype = None
	libshairplay.dnssd_unregister_airplay.argtypes = [c_void_p]
	libshairplay.dnssd_destroy.restype = None
	libshairplay.dnssd_destroy.argtypes = [c_void_p]

	# Initialize raop related functions
	libshairplay.raop_init.restype = c_void_p
	libshairplay.raop_init.argtypes = [POINTER(RaopNativeCallbacks), c_char_p]
	libshairplay.raop_start.restype = c_int
	libshairplay.raop_start.argtypes = [c_void_p, POINTER(c_ushort), POINTER(c_char), c_int]
	libshairplay.raop_stop.restype = None
	libshairplay.raop_stop.argtypes = [c_void_p]
	libshairplay.raop_destroy.restype = None
	libshairplay.raop_destroy.argtypes = [c_void_p]

	return libshairplay

RSA_KEY = """
-----BEGIN RSA PRIVATE KEY-----
MIIEpQIBAAKCAQEA59dE8qLieItsH1WgjrcFRKj6eUWqi+bGLOX1HL3U3GhC/j0Qg90u3sG/1CUt
wC5vOYvfDmFI6oSFXi5ELabWJmT2dKHzBJKa3k9ok+8t9ucRqMd6DZHJ2YCCLlDRKSKv6kDqnw4U
wPdpOMXziC/AMj3Z/lUVX1G7WSHCAWKf1zNS1eLvqr+boEjXuBOitnZ/bDzPHrTOZz0Dew0uowxf
/+sG+NCK3eQJVxqcaJ/vEHKIVd2M+5qL71yJQ+87X6oV3eaYvt3zWZYD6z5vYTcrtij2VZ9Zmni/
UAaHqn9JdsBWLUEpVviYnhimNVvYFZeCXg/IdTQ+x4IRdiXNv5hEewIDAQABAoIBAQDl8Axy9XfW
BLmkzkEiqoSwF0PsmVrPzH9KsnwLGH+QZlvjWd8SWYGN7u1507HvhF5N3drJoVU3O14nDY4TFQAa
LlJ9VM35AApXaLyY1ERrN7u9ALKd2LUwYhM7Km539O4yUFYikE2nIPscEsA5ltpxOgUGCY7b7ez5
NtD6nL1ZKauw7aNXmVAvmJTcuPxWmoktF3gDJKK2wxZuNGcJE0uFQEG4Z3BrWP7yoNuSK3dii2jm
lpPHr0O/KnPQtzI3eguhe0TwUem/eYSdyzMyVx/YpwkzwtYL3sR5k0o9rKQLtvLzfAqdBxBurciz
aaA/L0HIgAmOit1GJA2saMxTVPNhAoGBAPfgv1oeZxgxmotiCcMXFEQEWflzhWYTsXrhUIuz5jFu
a39GLS99ZEErhLdrwj8rDDViRVJ5skOp9zFvlYAHs0xh92ji1E7V/ysnKBfsMrPkk5KSKPrnjndM
oPdevWnVkgJ5jxFuNgxkOLMuG9i53B4yMvDTCRiIPMQ++N2iLDaRAoGBAO9v//mU8eVkQaoANf0Z
oMjW8CN4xwWA2cSEIHkd9AfFkftuv8oyLDCG3ZAf0vrhrrtkrfa7ef+AUb69DNggq4mHQAYBp7L+
k5DKzJrKuO0r+R0YbY9pZD1+/g9dVt91d6LQNepUE/yY2PP5CNoFmjedpLHMOPFdVgqDzDFxU8hL
AoGBANDrr7xAJbqBjHVwIzQ4To9pb4BNeqDndk5Qe7fT3+/H1njGaC0/rXE0Qb7q5ySgnsCb3DvA
cJyRM9SJ7OKlGt0FMSdJD5KG0XPIpAVNwgpXXH5MDJg09KHeh0kXo+QA6viFBi21y340NonnEfdf
54PX4ZGS/Xac1UK+pLkBB+zRAoGAf0AY3H3qKS2lMEI4bzEFoHeK3G895pDaK3TFBVmD7fV0Zhov
17fegFPMwOII8MisYm9ZfT2Z0s5Ro3s5rkt+nvLAdfC/PYPKzTLalpGSwomSNYJcB9HNMlmhkGzc
1JnLYT4iyUyx6pcZBmCd8bD0iwY/FzcgNDaUmbX9+XDvRA0CgYEAkE7pIPlE71qvfJQgoA9em0gI
LAuE4Pu13aKiJnfft7hIjbK+5kyb3TysZvoyDnb3HOKvInK7vXbKuU4ISgxB2bB3HcYzQMGsz1qJ
2gG0N5hvJpzwwhbhXqFKA4zaaSrw622wDniAK5MlIE0tIAKKP4yxNGjoD2QYjhBGuhvkWKY=
-----END RSA PRIVATE KEY-----
"""

class RaopCallbacks:
	def audio_init(self, bits, channels, samplerate):
		raise NotImplementedError()

	def audio_set_volume(self, session, volume):
		pass

	def audio_process(self, session, buffer):
		raise NotImplementedError()

	def audio_flush(self, session):
		pass

	def audio_destroy(self, session):
		pass

class RaopService:
	def audio_init_cb(self, cls, bits, channels, samplerate):
		session = self.callbacks.audio_init(bits, channels, samplerate)
		self.sessions.append(session)
		return session

	def audio_set_volume_cb(self, cls, sessionptr, volume):
		session = cast(sessionptr, py_object).value
		self.callbacks.audio_set_volume(session, volume)

	def audio_process_cb(self, cls, sessionptr, buffer, buflen):
		session = cast(sessionptr, py_object).value
		strbuffer = string_at(buffer, buflen)
		self.callbacks.audio_process(session, strbuffer)

	def audio_flush_cb(self, cls, sessionptr):
		session = cast(sessionptr, py_object).value
		self.callbacks.audio_flush(session)

	def audio_destroy_cb(self, cls, sessionptr):
		session = cast(sessionptr, py_object).value
		self.callbacks.audio_destroy(session)
		if session in self.sessions:
			self.sessions.remove(session)


	def __init__(self, libshairplay, callbacks):
		self.libshairplay = libshairplay
		self.callbacks = callbacks
		self.sessions = []
		self.instance = None

		# We need to hold a reference to native_callbacks
		self.native_callbacks = RaopNativeCallbacks()
		self.native_callbacks.audio_init = audio_init_prototype(self.audio_init_cb)
		self.native_callbacks.audio_set_volume = audio_set_volume_prototype(self.audio_set_volume_cb)
		self.native_callbacks.audio_process = audio_process_prototype(self.audio_process_cb)
		self.native_callbacks.audio_flush = audio_flush_prototype(self.audio_flush_cb)
		self.native_callbacks.audio_destroy = audio_destroy_prototype(self.audio_destroy_cb)

		# Initialize the raop instance with our callbacks
		self.instance = self.libshairplay.raop_init(pointer(self.native_callbacks), RSA_KEY)
		if self.instance == None:
			raise RuntimeError("Initializing library failed")

	def __del__(self):
		if self.instance != None:
			self.libshairplay.raop_destroy(self.instance)
		self.instance = None

	def start(self, port, hwaddrstr):
		port = c_ushort(port)
		hwaddr = create_string_buffer(hwaddrstr, len(hwaddrstr))

		ret = self.libshairplay.raop_start(self.instance, pointer(port), hwaddr, c_int(len(hwaddr)))
		if ret < 0:
			raise RuntimeError("Starting RAOP instance failed")
		return port.value

	def stop(self):
		self.libshairplay.raop_stop(self.instance)

class DnssdService:
	def __init__(self, libshairplay):
		self.libshairplay = libshairplay
		self.instance = None

		error = c_int(0)

		self.instance = self.libshairplay.dnssd_init(pointer(error))
		if self.instance == None:
			raise RuntimeError("Initializing library failed: " + str(error.value))

	def __del__(self):
		if self.instance != None:
			self.libshairplay.dnssd_destroy(self.instance)
		self.instance = None

	def register_raop(self, name, port, hwaddrstr):
		hwaddr = create_string_buffer(hwaddrstr, len(hwaddrstr))
		self.libshairplay.dnssd_register_raop(self.instance, name, c_ushort(port), hwaddr, len(hwaddr))

	def unregister_raop(self):
		self.libshairplay.dnssd_unregister_raop(self.instance)

	def register_airplay(self, name, port, hwaddrstr):
		hwaddr = create_string_buffer(hwaddrstr, len(hwaddrstr))
		self.libshairplay.dnssd_register_airplay(self.instance, name, c_ushort(port), hwaddr, len(hwaddr))

	def unregister_airplay(self):
		self.libshairplay.dnssd_unregister_airplay(self.instance)
