import sys
import json
import os

class SafeCoreApp:
    def __init__(self):
        self.archivo_db = "safecore_db.json"
        self.empresa_actual = None
        self.rubro_actual = None
        self.personal = []
        
        # Cargar los datos guardados automáticamente al iniciar el programa
        self.cargar_datos_json()

    def mostrar_menu(self):
        while True:
            print("\n" + "="*40)
            print("       🛡️ SYSTEM SAFE-CORE v1.2 🛡️")
            print("="*40)
            if self.empresa_actual:
                print(f"🏢 Empresa activa: {self.empresa_actual} ({self.rubro_actual})")
                print(f"👥 Personal registrado: {len(self.personal)} operarios")
            else:
                print("⚠️ Ninguna empresa configurada todavía.")
            print("-" * 40)
            print("1. Configurar Nueva Empresa / Cliente")
            print("2. Registrar Trabajador, Puesto y Capacitación")
            print("3. Correr Auditoría HSE de Control Total")
            print("4. Salir del Sistema")
            print("="*40)
            
            opcion = input("Seleccione una opción (1-4): ")
            
            if opcion == "1":
                self.configurar_empresa()
            elif opcion == "2":
                self.registrar_operario()
            elif opcion == "3":
                self.ejecutar_control()
            elif opcion == "4":
                print("\nCerrando SafeCore. ¡Gestión segura garantizada!")
                sys.exit()
            else:
                print("❌ Opción inválida. Intente de nuevo.")

    def guardar_datos_json(self):
        datos_a_guardar = {
            "empresa_actual": self.empresa_actual,
            "rubro_actual": self.rubro_actual,
            "personal": self.personal
        }
        try:
            with open(self.archivo_db, "w", encoding="utf-8") as f:
                json.dump(datos_a_guardar, f, indent=4, ensure_ascii=False)
            print("💾 [SISTEMA] Base de datos JSON actualizada correctamente.")
        except Exception as e:
            print(f"❌ Error al guardar los datos: {e}")

    def cargar_datos_json(self):
        if os.path.exists(self.archivo_db):
            try:
                with open(self.archivo_db, "r", encoding="utf-8") as f:
                    datos_cargados = json.load(f)
                    self.empresa_actual = datos_cargados.get("empresa_actual")
                    self.rubro_actual = datos_cargados.get("rubro_actual")
                    self.personal = datos_cargados.get("personal", [])
                print("📦 [SISTEMA] Datos previos recuperados con éxito desde el archivo local.")
            except Exception as e:
                print(f"⚠️ No se pudo cargar la base de datos previa: {e}")
        else:
            print("ℹ️ Iniciando sistema limpio. No se detectaron bases de datos previas.")

    def configurar_empresa(self):
        print("\n--- CONFIGURACIÓN DE CLIENTE ---")
        self.empresa_actual = input("Nombre de la empresa: ")
        print("Seleccione el Rubro:")
        print("A - Construcción / Obra")
        print("B - Laboratorio / Planta Química")
        print("C - Logística / Industria General")
        letra = input("Opción (A/B/C): ").upper()
        
        if letra == "A": self.rubro_actual = "Construcción"
        elif letra == "B": self.rubro_actual = "Laboratorio"
        else: self.rubro_actual = "Logística"
        
        print(f"✅ Empresa {self.empresa_actual} guardada.")
        self.guardar_datos_json()

    def registrar_operario(self):
        if not self.empresa_actual:
            print("❌ Primero debe configurar una empresa en la Opción 1.")
            return
        print("\n--- REGISTRO DE PERSONAL Y CAPACITACIÓN ---")
        nombre = input("Nombre del trabajador: ")
        puesto = input("Puesto de trabajo: ")
        meses_epp = int(input("Meses de uso del EPP actual: "))
        
        print("\nEstado de la Capacitación de Ingreso (Inducción):")
        print("A - Al día / Aprobada")
        print("P - Pendiente / Vencida")
        estado_cap = input("Opción (A/P): ").upper()
        
        estado = "Al día" if estado_cap == "A" else "Pendiente"
        fecha_cap = input("Ingrese fecha de última capacitación (AAAA-MM-DD) o 'No aplica': ")
        
        empleado = {
            "nombre": nombre, 
            "puesto": puesto, 
            "meses_epp": meses_epp,
            "estado_capacitacion": estado,
            "fecha_capacitacion": fecha_cap
        }
        
        self.personal.append(empleado)
        print(f"✅ {nombre} registrado correctamente con estado de capacitación: {estado}.")
        self.guardar_datos_json()

    def ejecutar_control(self):
        if not self.empresa_actual or not self.personal:
            print("❌ Falta configurar la empresa o registrar personal para auditar.")
            return
        
        print(f"\n=== REPORTE DE AUDITORÍA AUTOMÁTICO CRÍTICO: {self.empresa_actual} ===")
        limite = 3 if self.rubro_actual == "Construcción" else 6
        
        for p in self.personal:
            print(f"\n👤 {p['nombre']} | Puesto: {p['puesto']}")
            
            # Control de EPP
            if p['meses_epp'] > limite:
                print(f"   ⚠️ ALERTA EPP: Excedido ({p['meses_epp']} meses). Solicitar recambio para {self.rubro_actual}.")
            else:
                print(f"   ✅ EPP: En regla ({p['meses_epp']} meses de uso).")
                
            # Control de Capacitaciones (Campos dinámicos del JSON)
            # Usamos .get() por seguridad por si hay registros viejos en tu JSON sin estos campos
            est_cap = p.get("estado_capacitacion", "Pendiente")
            fec_cap = p.get("fecha_capacitacion", "No registrada")
            
            if est_cap == "Pendiente":
                print(f"   🚨 ALERTA CAPACITACIÓN: El operario registra inducción PENDIENTE. Restringir tareas de riesgo.")
            else:
                print(f"   ✅ CAPACITACIÓN: Al día (Última: {fec_cap}).")
                
        print("\n==================================================")

# =====================================================================
# EXTENSIONES DE CONTROL Y ESTADÍSTICAS
# =====================================================================

def calcular_estadisticas_hse(self):
    if not self.personal:
        print("📊 [ESTADÍSTICAS] No hay personal registrado para procesar.")
        return

    total = len(self.personal)
    epp_ok = 0
    capacitados = 0
    limite = 3 if self.rubro_actual == "Construcción" else 6

    for p in self.personal:
        if p.get('meses_epp', 0) <= limite:
            epp_ok += 1
        if p.get('estado_capacitacion') == "Al día":
            capacitados += 1

    porcentaje_epp = (epp_ok / total) * 100
    porcentaje_cap = (capacitados / total) * 100

    print("\n" + "📊"*20)
    print(f"   DASHBOARD DE RENDIMIENTO HSE: {self.empresa_actual}")
    print("" + "📊"*20)
    print(f"✅ Índice Cumplimiento EPP: {porcentaje_epp:.1f}%")
    print(f"🚨 Índice personal Capacitado: {porcentaje_cap:.1f}%")
    print(f"📋 Estado General: {'CRÍTICO' if porcentaje_cap < 70 or porcentaje_epp < 70 else 'SEGURO'}")
    print("="*40)

# Inyección de las estadísticas
SafeCoreApp.calcular_estadisticas_hse = calcular_estadisticas_hse


# =====================================================================
# ENGANCHE AUTOMÁTICO DEL DASHBOARD
# =====================================================================

control_original = SafeCoreApp.ejecutar_control

def ejecutar_control_con_estadisticas(self):
    control_original(self)
    if self.personal:
        self.calcular_estadisticas_hse()

# Interceptamos la auditoría para que muestre el dashboard
SafeCoreApp.ejecutar_control = ejecutar_control_con_estadisticas

# =====================================================================
# MÓDULO GERENCIAL: DASHBOARDS, SUBCONTRATOS Y EXPORTACIÓN EXCEL/CSV
# =====================================================================
import csv

def generar_reportes_gerenciales(self):
    """
    Genera la base de datos de subcontratistas (simulada por ahora)
    y exporta los 3 reportes CSV clave que todo Gerente necesita revisar.
    """
    if not self.empresa_actual:
        return

    # 1. Simulación de base de datos de Subcontratistas (Módulo pedido por Mauro)
    subcontratistas = [
        {"empresa": "Montajes Industriales S.A.", "gremio": "Metalúrgico", "art": "Al día", "capacitacion_ingreso": "Aprobada", "cumplimiento": "100%"},
        {"empresa": "Electricidad Express", "gremio": "Eléctrico", "art": "Vencida 🚨", "capacitacion_ingreso": "Pendiente 🚨", "cumplimiento": "0%"},
        {"empresa": "Logística del Norte", "gremio": "Transporte", "art": "Al día", "capacitacion_ingreso": "Aprobada", "cumplimiento": "100%"}
    ]

    # 2. Simulación de Estadísticas de Accidentabilidad (KPIs de Gerencia)
    total_operarios = len(self.personal)
    limite = 3 if self.rubro_actual == "Construcción" else 6
    epp_ok = sum(1 for p in self.personal if p.get('meses_epp', 0) <= limite)
    porcentaje_epp = (epp_ok / total_operarios * 100) if total_operarios > 0 else 0
    
    # KPIs típicos de HSE para directores
    kpis_accidentes = {
        "Dias_Sin_Accidentes": 142,
        "Meta_Anual_Dias": 365,
        "Tasa_Frecuencia_Siniestros": "1.2 (Bajo)",
        "Cumplimiento_EPP_Global": f"{porcentaje_epp:.1f}%",
        "Presupuesto_HSE_Ejecutado": "45%"
    }

    print("\n" + "💼"*20)
    print("      EXPORTADOR AUTOMÁTICO PARA GERENCIA")
    print("💼"*20)

    try:
        # PLANILLA 1: Reporte de Personal y Capacitaciones
        with open("reporte_personal_capacitaciones.csv", "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(["Nombre del Trabajador", "Puesto de Trabajo", "Meses Uso EPP", "Estado Capacitación", "Fecha Última Cap"])
            for p in self.personal:
                writer.writerow([p['nombre'], p['puesto'], p['meses_epp'], p.get('estado_capacitacion', 'Pendiente'), p.get('fecha_capacitacion', '-')])
        print("📊 [OK] 'reporte_personal_capacitaciones.csv' generado para Excel.")

        # PLANILLA 2: KPIs de Accidentes y Estadísticas Generales
        with open("dashboard_estadisticas_gerenciales.csv", "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(["Indicador Clave (KPI) de Seguridad", "Valor Actual / Estatus"])
            writer.writerow(["Días Acumulados Sin Accidentes", kpis_accidentes["Dias_Sin_Accidentes"]])
            writer.writerow(["Meta Anual (Días)", kpis_accidentes["Meta_Anual_Dias"]])
            writer.writerow(["Tasa de Frecuencia Siniestros", kpis_accidentes["Tasa_Frecuencia_Siniestros"]])
            writer.writerow(["Cumplimiento Global de EPP", kpis_accidentes["Cumplimiento_EPP_Global"]])
            writer.writerow(["Presupuesto HSE Ejecutado", kpis_accidentes["Presupuesto_HSE_Ejecutado"]])
        print("📈 [OK] 'dashboard_estadisticas_gerenciales.csv' generado para Excel.")

        # PLANILLA 3: Control de Subcontratistas y Contratos Separados
        with open("control_subcontratistas.csv", "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(["Empresa Subcontratista", "Gremio / Actividad", "Estado ART / Seguro", "Inducción de Ingreso", "Porcentaje Cumplimiento"])
            for sub in subcontratistas:
                writer.writerow([sub["empresa"], sub["gremio"], sub["art"], sub["capacitacion_ingreso"], sub["cumplimiento"]])
        print("🏢 [OK] 'control_subcontratistas.csv' generado para Excel.")
        
        print("\n💡 Tip: Los gerentes ya pueden abrir estos 3 archivos haciendo doble clic desde su carpeta.")
        print("="*40)

    except Exception as e:
        print(f"❌ Error al exportar los datos gerenciales: {e}")

# Inyectamos el exportador dentro del flujo de la auditoría (Opción 3)
viejo_control_con_stats = SafeCoreApp.ejecutar_control

def ejecutar_auditoria_completa_gerencial(self):
    # Corre el reporte y las estadísticas de consola que ya tenías
    viejo_control_con_stats(self)
    # Dispara la exportación de las 3 planillas gerenciales por separado
    generar_reportes_gerenciales(self)

SafeCoreApp.ejecutar_control = ejecutar_auditoria_completa_gerencial


# =====================================================================
# ARRANQUE DEL PROGRAMA (Esto va SIEMPRE al final absoluto)
# =====================================================================
if __name__ == "__main__":
    sistema = SafeCoreApp()
    sistema.mostrar_menu()