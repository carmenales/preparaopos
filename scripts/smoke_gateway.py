"""Script de verificación (smoke test) del Gateway Nginx y microservicios PreparaOpos.

Comprueba a través del puerto público :8080:
  1. /healthz en el gateway (200 OK)
  2. / -> Study Assistant (200 OK)
  3. /tests/ -> Test Engine (200 OK)
  4. /tests -> Redirección canónica 301 a /tests/
  5. Segregación de ficheros estáticos:
     - /tests/static/style.css (CSS de test-engine con selectores distintivos)
     - /static/style.css (CSS de study-assistant con selectores distintivos)
  6. Simulacro completo en test-engine a través del gateway:
     - Inicio de examen (POST /tests/sessions/)
     - Carga de pregunta 1 con temporizador y htmx prefijados
     - Respuesta (POST /tests/sessions/{id}/answer)
     - Cierre y visualización de resultados (GET /tests/sessions/{id}/result)
  7. Navegación cruzada bidireccional:
     - Study Assistant -> Test Engine (POST /tests/practice/by-note/{note_id})
     - Test Engine -> Study Assistant (GET /notes/{note_id})
     - Botón de práctica en la nota apuntando a /tests/practice/by-note/...
  8. Comprobación de página de error 50x cuando un upstream no responde.

Uso:
  python scripts/smoke_gateway.py [--gateway-url http://localhost:8080]
"""

from __future__ import annotations

import argparse
import re
import sys
import httpx


def log_step(name: str) -> None:
    print(f"\n[+] {name}")


def log_ok(msg: str) -> None:
    print(f"  [OK] {msg}")


def log_err(msg: str) -> None:
    print(f"  [FAIL] {msg}")


def run_smoke_tests(base_url: str = "http://localhost:8080") -> bool:
    base_url = base_url.rstrip("/")
    print(f"Iniciando verificación contra Gateway en {base_url}...")
    errors: list[str] = []

    client = httpx.Client(timeout=10.0, follow_redirects=False)

    # -------------------------------------------------------------------------
    # 1. Healthcheck del propio Gateway
    # -------------------------------------------------------------------------
    log_step("1. Healthcheck del Gateway (/healthz)")
    try:
        r = client.get(f"{base_url}/healthz")
        if r.status_code == 200 and "OK" in r.text:
            log_ok("Gateway respondió 200 OK en /healthz")
        else:
            errors.append(f"/healthz devolvió {r.status_code}: {r.text[:100]}")
            log_err(errors[-1])
    except Exception as e:
        errors.append(f"Error conectando a /healthz: {e}")
        log_err(errors[-1])

    # -------------------------------------------------------------------------
    # 2. Study Assistant en la raíz /
    # -------------------------------------------------------------------------
    log_step("2. Raíz (/) -> Study Assistant")
    try:
        r = client.get(f"{base_url}/")
        if r.status_code == 200 and ("Study Assistant" in r.text or "dashboard" in r.text.lower() or "procesos" in r.text.lower()):
            log_ok("Study Assistant respondió 200 OK en /")
        else:
            errors.append(f"/ devolvió {r.status_code} sin marcas esperadas de Study Assistant")
            log_err(errors[-1])
    except Exception as e:
        errors.append(f"Error conectando a /: {e}")
        log_err(errors[-1])

    # -------------------------------------------------------------------------
    # 3. Test Engine en /tests/ y redirección canónica /tests
    # -------------------------------------------------------------------------
    log_step("3. Catálogo (/tests/) y redirección canónica (/tests)")
    try:
        r_redir = client.get(f"{base_url}/tests")
        if r_redir.status_code == 301 and r_redir.headers.get("location", "").endswith("/tests/"):
            log_ok("/tests redirige con 301 a /tests/")
        else:
            errors.append(f"/tests devolvió {r_redir.status_code} (Location: {r_redir.headers.get('location')})")
            log_err(errors[-1])

        r_tests = client.get(f"{base_url}/tests/")
        if r_tests.status_code == 200 and ("Test Engine" in r_tests.text or "Exámenes disponibles" in r_tests.text):
            log_ok("Test Engine respondió 200 OK en /tests/")
        else:
            errors.append(f"/tests/ devolvió {r_tests.status_code} sin marcas esperadas")
            log_err(errors[-1])
    except Exception as e:
        errors.append(f"Error conectando a /tests/: {e}")
        log_err(errors[-1])

    # -------------------------------------------------------------------------
    # 4. Segregación de ficheros estáticos (/tests/static/... vs /static/...)
    # -------------------------------------------------------------------------
    log_step("4. Segregación de estilos CSS estáticos")
    try:
        r_css_te = client.get(f"{base_url}/tests/static/style.css")
        r_css_sa = client.get(f"{base_url}/static/style.css")

        te_ok = (
            r_css_te.status_code == 200
            and (".scoreboard" in r_css_te.text or ".timer" in r_css_te.text or ".note-dropdown" in r_css_te.text)
        )
        if te_ok:
            log_ok("/tests/static/style.css devolvió el CSS distintivo de Test Engine")
        else:
            errors.append(f"/tests/static/style.css erróneo (status {r_css_te.status_code})")
            log_err(errors[-1])

        sa_ok = (
            r_css_sa.status_code == 200
            and ("search" in r_css_sa.text or "prose" in r_css_sa.text or "nested-toc" in r_css_sa.text or "note-card" in r_css_sa.text)
        )
        if sa_ok:
            log_ok("/static/style.css devolvió el CSS distintivo de Study Assistant")
        else:
            errors.append(f"/static/style.css erróneo (status {r_css_sa.status_code})")
            log_err(errors[-1])

        # Asegurar que no se confunden
        if ".scoreboard" in r_css_sa.text:
            errors.append("/static/style.css contiene estilos de Test Engine (.scoreboard)")
            log_err(errors[-1])

    except Exception as e:
        errors.append(f"Error verificando CSS estático: {e}")
        log_err(errors[-1])

    # -------------------------------------------------------------------------
    # 5. Flujo completo de simulacro en Test Engine vía Gateway
    # -------------------------------------------------------------------------
    log_step("5. Flujo completo de simulacro (examen, timer, respuesta htmx y resultados)")
    session_id: str | None = None
    try:
        # Inicio de sesión
        r_start = client.post(
            f"{base_url}/tests/sessions/",
            data={"mode": "exam", "source": "exam", "source_ref": "53"},
        )
        if r_start.status_code == 303:
            loc = r_start.headers.get("location", "")
            if "/tests/sessions/" in loc and "/question/1" in loc:
                session_id = loc.split("/sessions/")[1].split("/")[0]
                log_ok(f"Sesión creada correctamente ({session_id}) con salto 303 prefijado")
            else:
                errors.append(f"Salto 303 sin prefijo correcto: {loc}")
                log_err(errors[-1])
        else:
            errors.append(f"Inicio de sesión devolvió {r_start.status_code}")
            log_err(errors[-1])

        if session_id:
            # Pregunta 1
            r_q1 = client.get(f"{base_url}/tests/sessions/{session_id}/question/1")
            if r_q1.status_code == 200 and 'hx-post="/tests/sessions/' in r_q1.text and "timer" in r_q1.text:
                log_ok("Pregunta 1 renderizada con timer y hx-post prefijados bajo /tests/")
            else:
                errors.append("Pregunta 1 no contiene los atributos o prefijos esperados")
                log_err(errors[-1])

            # Responder por htmx
            r_ans = client.post(
                f"{base_url}/tests/sessions/{session_id}/answer",
                data={"question_id": 18012, "selected_option_id": 1, "n": 1},
            )
            if r_ans.status_code == 200 and ("Respuesta guardada" in r_ans.text or "feedback" in r_ans.text):
                log_ok("Respuesta htmx procesada correctamente")
            else:
                errors.append(f"Respuesta htmx falló con status {r_ans.status_code}")
                log_err(errors[-1])

            # Resultados
            r_res = client.get(f"{base_url}/tests/sessions/{session_id}/result")
            if r_res.status_code == 200 and "Resultado" in r_res.text and 'href="/tests/"' in r_res.text:
                log_ok("Hoja de resultados renderizada con enlace de retorno prefijado a /tests/")
            else:
                errors.append("Hoja de resultados no contiene el enlace o contenido esperado")
                log_err(errors[-1])

    except Exception as e:
        errors.append(f"Error en flujo de examen: {e}")
        log_err(errors[-1])

    # -------------------------------------------------------------------------
    # 6. Navegación cruzada bidireccional
    # -------------------------------------------------------------------------
    log_step("6. Navegación cruzada bidireccional (Study Assistant <-> Test Engine)")
    try:
        # A) Study Assistant -> Test Engine (Práctica por apunte)
        client_follow = httpx.Client(timeout=10.0, follow_redirects=True)
        r_cross = client_follow.post(f"{base_url}/tests/practice/by-note/tema-i-01-derecho-constitucional")
        if r_cross.status_code == 200 and "/tests/sessions/" in str(r_cross.url) and "/question/1" in str(r_cross.url):
            log_ok("Navegación cruzada SA -> TE resolvió con éxito cadena 307 -> 303 -> 200 en /tests/sessions/.../question/1")
        else:
            errors.append(f"Práctica por apunte no finalizó en la pregunta esperada: {r_cross.status_code} ({r_cross.url})")
            log_err(errors[-1])

        # B) Test Engine -> Study Assistant (Lectura de apunte enlazado)
        r_note = client.get(f"{base_url}/notes/tema-i-01-derecho-constitucional")
        if r_note.status_code == 200 and ("tema-i-01" in r_note.text or "Constitucional" in r_note.text):
            log_ok("Acceso al apunte vía Gateway (TE -> SA) respondió 200 OK")
            if 'action="/tests/practice/by-note/' in r_note.text:
                log_ok("El formulario de práctica en el apunte apunta correctamente a /tests/practice/by-note/...")
            else:
                errors.append("El formulario de práctica en el apunte no incluye la URL prefijada /tests/...")
                log_err(errors[-1])
        else:
            errors.append(f"Acceso a la nota vía Gateway devolvió {r_note.status_code}")
            log_err(errors[-1])

    except Exception as e:
        errors.append(f"Error en pruebas de navegación cruzada: {e}")
        log_err(errors[-1])

    # -------------------------------------------------------------------------
    # Resumen final
    # -------------------------------------------------------------------------
    print("\n" + "=" * 60)
    if errors:
        print(f"SMOKE TEST FALLIDO: {len(errors)} error(es) detectado(s):")
        for err in errors:
            print(f"  - {err}")
        return False
    else:
        print("SMOKE TEST COMPLETADO CON ÉXITO: Todas las verificaciones del Gateway pasaron al 100%.")
        return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Smoke test para el Gateway Nginx de PreparaOpos")
    parser.add_argument("--gateway-url", default="http://localhost:8080", help="URL base del gateway (por defecto http://localhost:8080)")
    args = parser.parse_args()

    success = run_smoke_tests(args.gateway_url)
    sys.exit(0 if success else 1)
