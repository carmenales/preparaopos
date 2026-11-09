#!/usr/bin/env python3
"""
Servidor local para la aplicación de Tests PreparaTIC.
Permite ejecutar y probar las versiones V3 (SPA Vue 3) y V2 (Gentelella/Bootstrap)
sin problemas de políticas CORS de archivos locales (file://).
"""

import http.server
import socketserver
import webbrowser
import os
import sys

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        # Deshabilitar caché para pruebas de desarrollo
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

def run_server(port=PORT):
    for p in range(port, port + 10):
        try:
            with socketserver.TCPServer(("", p), Handler) as httpd:
                print("=" * 60)
                print(f" Servidor de Tests PreparaTIC activo en:")
                print(f" -> Version V3 (Principal - Vue 3 SPA):  http://localhost:{p}/")
                print(f" -> Version V2 (Historica - Gentelella): http://localhost:{p}/v2/index.html")
                print("=" * 60)
                print("Presiona Ctrl+C para detener el servidor.\n")
                
                # Abrir navegador automáticamente
                webbrowser.open(f"http://localhost:{p}/")
                try:
                    httpd.serve_forever()
                except KeyboardInterrupt:
                    print("\nServidor detenido correctamente.")
                return
        except OSError:
            print(f"Puerto {p} ocupado, intentando con {p+1}...")
            continue
    print("Error: No se pudo encontrar un puerto libre entre 8080 y 8090.")

if __name__ == "__main__":
    port_arg = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else PORT
    run_server(port_arg)

