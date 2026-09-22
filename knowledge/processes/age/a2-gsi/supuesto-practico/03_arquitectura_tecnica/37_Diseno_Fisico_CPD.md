# DISEÑO FÍSICO DE CPD E INFRAESTRUCTURA

Especificaciones técnicas para el alojamiento de sistemas (si no se usa Nube SARA o se pide diseñar un CPD propio).

---

## 1. UBICACIÓN Y ARQUITECTURA
* **Emplazamiento:** Fuera de zonas inundables o sísmicas. Sin señalización externa (discreción).
* **Suelo Técnico:** Elevado para paso de cableado y flujo de aire.
* **Diseño Modular:** Capacidad de ampliación sin parar el servicio.

## 2. ELECTRICIDAD (DISPONIBILIDAD)
* **SAI/UPS:** Sistemas de Alimentación Ininterrumpida redundantes (N+1) para filtrar picos y mantener el servicio ante microcortes.
* **Grupo Electrógeno:** Generador diésel para cortes prolongados. Conmutación automática.
* **Doble Acometida:** Alimentación eléctrica por dos caminos independientes.

## 3. CLIMATIZACIÓN (EFICIENCIA)
* **Pasillos Frío/Caliente:** Diseño eficiente donde el aire frío entra por el frontal de los racks y el caliente sale por detrás.
* **Temperatura/Humedad:** Control estricto (20-25ºC, 40-55% HR).

## 4. EXTINCIÓN DE INCENDIOS (SEGURIDAD)
* **Detección:** Precoz (detectores iónicos/ópticos) en ambiente y falso suelo.
* **Extinción:** Uso de **Agentes Gaseosos** (Gases Inertes como Novec 1230) que extinguen el fuego sin dañar los servidores (el agua está prohibida).
* **Normativa:** Cumplimiento del RIPCI (RD 513/2017).