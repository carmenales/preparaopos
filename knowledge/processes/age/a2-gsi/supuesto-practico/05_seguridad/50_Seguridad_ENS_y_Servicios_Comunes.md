# SEGURIDAD ENS + SERVICIOS COMUNES

## 1. FASE 1 — CATEGORIZACIÓN ENS Y LEYES APLICABLES

### 1.1. Dimensiones ENS (C, I, D) — cómo explicarlas en el examen

| Dimensión | Qué protege | Cuándo predomina | Frase para examen |
| :--- | :--- | :--- | :--- |
| **Confidencialidad** | Acceso ilegítimo a info | Datos personales, económicos, acceso funcionario | *El impacto en confidencialidad es relevante porque el sistema trata datos…* |
| **Integridad** | Alteraciones no autorizadas | Expedientes, firmas, pagos | *La integridad es crítica para asegurar que el expediente mantiene validez jurídica…* |
| **Disponibilidad** | Servicio no accesible | Tramitadores internos 24/7, portales críticos | *La disponibilidad es prioritaria para garantizar la continuidad del servicio…* |

### 1.2. Plantilla de categorización ENS

> “La categorización del sistema se realiza según el ENS (RD 311/2022) evaluando el impacto en **Confidencialidad**, **Integridad** y **Disponibilidad**.
>
> Considerando [datos personales / información económica / servicio crítico / exposición pública], el impacto sería [limitado / grave / muy grave], clasificando el sistema como Categoría **[Baja / Media / Alta]**.
>
> Se aplican las medidas de refuerzo del Anexo II acordes a dicha categoría.”

---

## 2. FASE 2 — MEDIDAS ENS (ORG, OP, MP) POR CATEGORÍA

Aquí está el núcleo del documento:

* [x] Medidas reales **ENS**
* [x] Con códigos correctos
* [x] Y adaptadas a cada nivel

### 2.1. MEDIDAS ORGANIZATIVAS (ORG)

| Código | Qué exige | Baja | Media | Alta |
| :--- | :--- | :--- | :--- | :--- |
| **org.1** | Política seguridad | Documento, roles | Manual básico, Política + Comité | CISO + revisiones |
| **org.2** | Procedimientos | Procedimientos aprobados | Limitados, Gestión de cambios | Procesos auditados |
| **org.4** | Gestión de accesos | Roles/responsables, Roles básicos | Matrices + revisiones | Control estricto + segregación |

### 2.2. MEDIDAS OPERACIONALES (OP)

| Código | Qué asegura | Baja | Media | Alta |
| :--- | :--- | :--- | :--- | :--- |
| **op.exp.8** | Registro actividad | Trazabilidad, Logs locales | Logs centralizados | Logs en SIEM |
| **op.exp.10** | Protección registros | Integridad de logs, Firmas hash | Almacenamiento seguro | WORM + segregación |
| **op.mon.1** | Detección intrusión | IDS/IPS Básico | IDS | IDS + análisis avanzado |
| **op.mon.2** | Monitorización | Supervisión Manual | Herramienta base | SOC 24/7 |

### 2.3. MEDIDAS DE PROTECCIÓN (MP)

| Código | Qué protege | Baja | Media | Alta |
| :--- | :--- | :--- | :--- | :--- |
| **mp.acc** | Control acceso | Usuarios, 1FA | MFA interno | MFA + acceso VPN + bastionadomp. |
| **mp.com.1** | Perímetro | Red interna, Firewall básico | NGFW + VLAN | DMZ + doble firewall |
| **mp.com.2** | Confidencialidad | Cifrado tráfico, TLS básico | TLS 1.2+ FIPS | HSM / túneles dedicados |
| **mp.com.3** | Integridad canal | Firmas / sellos, Hash | Certificados FNMT | Sellado + TSU |
| **mp.si.2** | Criptografía | Datos y documentos, Cifrado básico | Cifrado AES + firma | Criptografía robusta + HSM |
| **mp.back** | Backups | Continuidad, Semanal | Diario + cifrado | Replica CPD alterno |
| **mp.cont** | Continuidad DRP | Plan simple | RTO<24h | RTO<4h + CPD alterno |

*(Códigos alineados con Anexo II. Algunos ENS no usan nombres exactos pero el tribunal sí espera estos conceptos)*

---

## 3. FASE 3 — ELEMENTOS DE SEGURIDAD QUE DEBES ENUMERAR SEGÚN CATEGORÍA

Aquí está lo que debes escribir tal cual.

### 3.1 SI ES CATEGORÍA BAJA
* Control de acceso básico (**mp.acc**)
* HTTPS (**mp.com.2**)
* Backup simple
* Logs mínimos (**op.exp.8**)
* Antivirus

### 3.2 SI ES CATEGORÍA MEDIA (la más habitual)
* **MFA** (**mp.acc**)
* Firewall **NGFW** (**mp.com.1**)
* **IDS/IPS** (**op.mon.1**)
* **WAF** si expuesto
* Segmentación VLAN
* Logs centralizados (**op.exp.8**)
* Protección de logs (**op.exp.10**)
* Cifrado BBDD
* Backups cifrados + retención
* Hardening de servidores
* Análisis de vulnerabilidades (**mp.si.1**)
* Auditoría anual ENS

### 3.3 SI ES CATEGORÍA ALTA
* **SOC 24/7** (**op.mon.2**)
* Sondas CCN (SAT-INET / LUCIA)
* Doble firewall + DMZ
* WAF avanzado
* Segmentación **microsegmentada**
* Criptografía robusta con **HSM** (**mp.si.2**)
* Replica síncrona entre CPD
* **RTO < 4h**
* **RPO ≈ 0**
* DRP completo
* Doble CPD

---

## 4. FASE 4 — TRAZABILIDAD COMPLETA

Servicios Comunes AGE ↔ Medidas ENS
Aquí está la parte que nadie tiene bien preparada.

### 4.1. Red SARA / Nube SARA

| Función | Medidas ENS |
| :--- | :--- |
| Comunicaciones | mp.com.1–3 |
| Aislamiento | mp.com.1 |
| Monitorización | op.mon.1–2 |

**Frase examen:**
> “Red/Nube SARA garantiza comunicaciones seguras aplicando **mp.com.1–3** y monitorización conforme **op.mon.**.”

### 4.2. Cl@ve / Autentica

| Función | Medidas |
| :--- | :--- |
| Autenticación | mp.acc |
| Control de acceso | org.4 |
| Registro usado | op.exp.8–10 |

### 4.3. @FIRMA / FIRe

| Función | Medidas |
| :--- | :--- |
| Firma electrónica | mp.si.2 |
| Integridad | mp.com.3 |
| Registro | op.exp.8 |

### 4.4. INSIDE

| Función | Medidas |
| :--- | :--- |
| Integridad documental | mp.si.2 |
| Control acceso expediente | mp.acc |
| Trazabilidad | op.exp.8–10 |

### 4.5. SIR / GEISER / ORVE

| Función | Medidas |
| :--- | :--- |
| Registro | op.exp.8–10 |
| Seguro en intercambio | mp.com.2 |
| Digitalización | mp.si.2 |

### 4.6. Notifica / DEHú

| Función | Medidas |
| :--- | :--- |
| Canal seguro | mp.com.2–3 |
| Trazabilidad notificación | op.exp.8 |

### 4.7. PID – Plataforma de Intermediación

| Función | Medidas |
| :--- | :--- |
| Interoperabilidad | mp.com.2–3 |
| Control acceso | mp.acc |
| Registro de consultas | op.exp.8 |

### 4.8. DIR3

| Función | Medidas |
| :--- | :--- |
| Identificación unívoca | org.2 / org.4 |

---

## 5. FASE 5 — PLANTILLAS PROFESIONALES DE RESPUESTA

### 5.1. Seguridad lógica y perimetral

!!! tip "Seguridad lógica y perimetral"

    La **seguridad** se articula según **defensa en profundidad**, aplicando las medidas **ENS** asociadas a la categoría del sistema.
    
    En **control de acceso** se aplica **[mp.acc]**, reforzado mediante autenticación delegada en **Cl@ve**.
    
    Las **comunicaciones** se protegen mediante **[mp.com.1–3]**, complementado con firewall **NGFW**, **WAF** e **IDS/IPS** (**[op.mon.1]**).
    
    Se habilita **trazabilidad** completa mediante registro y protección de logs (**[op.exp.8–10]**).
    
    La **integridad** y **autenticidad** de documentos se garantiza mediante **@firma/INSIDE** (**[mp.si.2]**, **[mp.com.3]**).

### 5.2. Seguridad física del CPD

!!! tip "Seguridad física del CPD"

    El CPD aplica control de acceso físico, videovigilancia, climatización redundante, SAIs, detección/extinción y zonas segregadas, cumpliendo las medidas ENS de continuidad (**mp.cont**) y de protección física.

### 5.3. Servicios comunes

!!! tip "Servicios comunes"

    La integración con **Red SARA**, **Cl@ve**, **@firma**, **INSIDE**, **PID** y **Notifica** garantiza cumplimiento **ENS** en comunicaciones (**[mp.com.1–3]**), control de acceso (**[mp.acc]**), integridad (**[mp.si.2]**) y trazabilidad completa (**[op.exp.8–10]**).

---

## 6. FASE 6 — ESCENARIOS REALES DE SUPUESTO (esto es oro para examen)

!!! tip "Sistema INTERNO sin RGPD"
    Portal funcionario / gestor interno

    * No aplica RGPD → impacta **Integridad** + **Disponibilidad** → categoría **MEDIA**
    * Seguridad clave: **mp.acc, mp.com.\***, op.exp.8, op.mon.\*, backups, segmentación VLAN

!!! tip "Sistema para Ciudadano con datos personales"
    * Impacta **Confidencialidad** + **Integridad** → categoría **MEDIA**
    * Servicios comunes obligatorios
    * Servicios comunes → Trazabilidad + autenticación

!!! tip "Sistema CRÍTICO 24/7" 
    Ej: pagos, nóminas, emergencias

    * Impacta **Disponibilidad** → categoría **ALTA**
    * RTO<4h, RPO ≈ 0
    * Sondas CCN
    * Doble CPD

---

## 7. FASE 7 — CIERRE LEGAL PROFESIONAL

> “La solución cumple las medidas exigidas por el **ENS** según su categorización, garantizando prevención, detección, protección y trazabilidad, conforme al **RD 311/2022** y a las guías **CCN-STIC** aplicables.”

---
