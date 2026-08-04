import http.server
import json
import os
import sqlite3

PORT = 8000
DB_PATH = "safecore.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Tabla de Personal
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS personnel (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            dni TEXT NOT NULL,
            company TEXT NOT NULL,
            medical_clearance TEXT NOT NULL,
            status TEXT NOT NULL
        )
    """)
    
    # Tabla de IPER
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS iper_matrix (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_name TEXT NOT NULL,
            hazard TEXT NOT NULL,
            risk TEXT NOT NULL,
            control_measure TEXT NOT NULL,
            severity TEXT NOT NULL
        )
    """)

    # Tabla de Incidentes / Accidentes (Con formato de fecha YYYY-MM para control mensual)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            incident_date TEXT NOT NULL,
            project_name TEXT NOT NULL,
            injured_name TEXT NOT NULL,
            person_type TEXT NOT NULL,
            description TEXT NOT NULL,
            lost_days INTEGER NOT NULL,
            severity_type TEXT NOT NULL
        )
    """)

    # Datos iniciales de prueba
    cursor.execute("SELECT COUNT(*) FROM personnel")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO personnel (full_name, dni, company, medical_clearance, status) VALUES (?, ?, ?, ?, ?)", [
            ("Carlos Gómez", "32.456.789", "Propio", "Al día", "Apto"),
            ("Esteban Quito", "28.123.456", "Subcontratista A", "Al día", "Apto"),
            ("Marcos Perez", "35.789.123", "Subcontratista B", "Vencido", "Observado")
        ])

    cursor.execute("SELECT COUNT(*) FROM iper_matrix")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO iper_matrix (project_name, hazard, risk, control_measure, severity) VALUES (?, ?, ?, ?, ?)", [
            ("Obra Minera Norte", "Manipulación de cargas", "Caída de objetos", "Grúa certificada", "Alto")
        ])

    cursor.execute("SELECT COUNT(*) FROM incidents")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO incidents (incident_date, project_name, injured_name, person_type, description, lost_days, severity_type) VALUES (?, ?, ?, ?, ?, ?, ?)", [
            ("2026-07-15", "Obra Minera Norte", "Lucas Díaz", "Tercero", "Golpe en pie por caída de herramienta menor.", 3, "Leve"),
            ("2026-08-01", "Obra Minera Norte", "Mario Ruiz", "Propio", "Esquinze leve en pasarela de acceso.", 0, "Leve")
        ])

    conn.commit()
    conn.close()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SafeCore - Reporte Gerencial Mensual</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Incluimos Chart.js para gráficos profesionales -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { background-color: #f1f5f9; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        .navbar { background-color: #0f172a; }
        .card-metric { border-left: 4px solid #3b82f6; box-shadow: 0 4px 6px rgba(0,0,0,0.05); background: white; border-radius: 8px; }
        .table-container { background: white; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border-radius: 8px; padding: 20px; margin-bottom: 25px; }
        .chart-container { background: white; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border-radius: 8px; padding: 20px; margin-bottom: 25px; position: relative; height: 320px; }
    </style>
</head>
<body>
    <nav class="navbar navbar-dark px-4 py-3 d-flex justify-content-between">
        <span class="navbar-brand mb-0 h1 fw-bold">🛡️ SafeCore <small class="text-muted fs-6">| Reporte Gerencial y Estadísticas Mensuales</small></span>
        <div>
            <button class="btn btn-outline-light btn-sm me-2" onclick="alert('Exportando reporte mensual PDF para SRT y Directorio...')">📊 Exportar Informe Mensual</button>
            <span class="badge bg-success">Sistema Conectado</span>
        </div>
    </nav>

    <div class="container my-4">
        <!-- Filtro de Periodo Mensual -->
        <div class="row mb-4">
            <div class="col-md-4">
                <label class="form-label fw-bold text-secondary">📅 Seleccionar Periodo de Análisis:</label>
                <select class="form-select" id="filter-month" onchange="cargarTodo()">
                    <option value="ALL">Histórico Completo</option>
                    <option value="2026-08" selected>Agosto 2026 (Mes Actual)</option>
                    <option value="2026-07">Julio 2026</option>
                </select>
            </div>
        </div>

        <!-- Panel Gerencial de Métricas Clave -->
        <div class="row g-4 mb-4">
            <div class="col-md-3">
                <div class="card card-metric p-3" style="border-left-color: #ef4444;">
                    <h6 class="text-muted">Accidentes del Mes</h6>
                    <h3 class="fw-bold text-dark" id="stat-accidents">0</h3>
                    <small class="text-danger" id="stat-accidents-desc">Propios vs Terceros</small>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card card-metric p-3" style="border-left-color: #f59e0b;">
                    <h6 class="text-muted">Días Perdidos (Bajas)</h6>
                    <h3 class="fw-bold text-dark" id="stat-lost-days">0</h3>
                    <small class="text-warning">Impacto operativo mensual</small>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card card-metric p-3" style="border-left-color: #3b82f6;" title="Frecuencia: Cuántos accidentes ocurren por cada millón de horas trabajadas.">
                    <h6 class="text-muted">Índice de Frecuencia (IF) ℹ️</h6>
                    <h3 class="fw-bold text-primary" id="stat-if">0.00</h3>
                    <small class="text-muted">Meta: < 15.00</small>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card card-metric p-3" style="border-left-color: #8b5cf6;" title="Gravedad: Cuántos días se pierden por cada millón de horas trabajadas.">
                    <h6 class="text-muted">Índice de Gravedad (IG) ℹ️</h6>
                    <h3 class="fw-bold text-purple" id="stat-ig">0.00</h3>
                    <small class="text-muted">Meta: < 50.00</small>
                </div>
            </div>
        </div>

        <!-- Sección de Gráficos Visuales para la Gerencia -->
        <div class="row">
            <div class="col-md-6">
                <div class="chart-container">
                    <h5 class="fw-bold text-secondary mb-3">📊 Siniestralidad: Propios vs Terceros</h5>
                    <canvas id="chartType"></canvas>
                </div>
            </div>
            <div class="col-md-6">
                <div class="chart-container">
                    <h5 class="fw-bold text-secondary mb-3">📉 Evolución de Días Perdidos</h5>
                    <canvas id="chartDays"></canvas>
                </div>
            </div>
        </div>

        <!-- Módulo del Licenciado: Registro y Control de Accidentes -->
        <div class="table-container border-top border-danger border-4">
            <div class="d-flex justify-content-between align-items-center mb-3">
                <div>
                    <h4 class="fw-bold text-danger mb-0">🚨 Registro Mensual de Siniestralidad</h4>
                    <small class="text-muted">Carga detallada del Licenciado (Trazabilidad de eventos)</small>
                </div>
                <button class="btn btn-danger btn-sm fw-bold" data-bs-toggle="modal" data-bs-target="#modalIncident">➕ Cargar Nuevo Siniestro</button>
            </div>
            <div class="table-responsive">
                <table class="table table-hover align-middle">
                    <thead class="table-dark">
                        <tr>
                            <th>ID</th>
                            <th>Fecha</th>
                            <th>Proyecto</th>
                            <th>Afectado</th>
                            <th>Tipo</th>
                            <th>Descripción del Hecho</th>
                            <th>Días Perdidos</th>
                            <th>Gravedad</th>
                        </tr>
                    </thead>
                    <tbody id="tbody-incidents"></tbody>
                </table>
            </div>
        </div>

        <!-- Módulo de Personal -->
        <div class="table-container">
            <div class="d-flex justify-content-between align-items-center mb-3">
                <h4 class="fw-bold text-secondary mb-0">👷 Control de Personal y Vencimientos</h4>
                <button class="btn btn-success btn-sm" data-bs-toggle="modal" data-bs-target="#modalPersonal">➕ Registrar Colaborador</button>
            </div>
            <div class="table-responsive">
                <table class="table table-hover align-middle">
                    <thead class="table-dark">
                        <tr>
                            <th>ID</th>
                            <th>Colaborador</th>
                            <th>DNI</th>
                            <th>Empresa</th>
                            <th>Apto Médico</th>
                            <th>Estado</th>
                        </tr>
                    </thead>
                    <tbody id="tbody-personnel"></tbody>
                </table>
            </div>
        </div>
    </div>

    <!-- Modales de Carga -->
    <div class="modal fade" id="modalIncident" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header bg-danger text-white">
                    <h5 class="modal-title fw-bold">Registrar Siniestro / Accidente</h5>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <form id="form-incident">
                        <div class="mb-3"><label class="form-label">Fecha del Suceso</label><input type="date" class="form-control" id="incident_date" required value="2026-08-02"></div>
                        <div class="mb-3"><label class="form-label">Proyecto / Obra</label><input type="text" class="form-control" id="inc_project" required value="Obra Minera Norte"></div>
                        <div class="mb-3"><label class="form-label">Nombre del Afectado</label><input type="text" class="form-control" id="injured_name" required placeholder="Ej: Juan Pérez"></div>
                        <div class="mb-3">
                            <label class="form-label">Tipo de Personal</label>
                            <select class="form-select" id="person_type">
                                <option value="Propio">Personal Propio</option>
                                <option value="Tercero">Personal de Terceros / Contratista</option>
                            </select>
                        </div>
                        <div class="mb-3"><label class="form-label">Descripción de lo ocurrido</label><textarea class="form-control" id="description" rows="2" required placeholder="¿Qué pasó? ¿Cómo afectó?"></textarea></div>
                        <div class="mb-3"><label class="form-label">Días Perdidos (Baja médica)</label><input type="number" class="form-control" id="lost_days" required value="0"></div>
                        <div class="mb-3">
                            <label class="form-label">Gravedad</label>
                            <select class="form-select" id="severity_type">
                                <option value="Leve">Leve (Sin baja o baja menor)</option>
                                <option value="Grave con baja">Grave con baja médica</option>
                            </select>
                        </div>
                        <button type="submit" class="btn btn-danger w-100 fw-bold">Guardar y Actualizar Índices</button>
                    </form>
                </div>
            </div>
        </div>
    </div>

    <div class="modal fade" id="modalPersonal" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header bg-success text-white">
                    <h5 class="modal-title">Registrar Colaborador</h5>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <form id="form-personal">
                        <div class="mb-3"><label class="form-label">Nombre y Apellido</label><input type="text" class="form-control" id="full_name" required></div>
                        <div class="mb-3"><label class="form-label">DNI</label><input type="text" class="form-control" id="dni" required></div>
                        <div class="mb-3"><label class="form-label">Empresa</label><input type="text" class="form-control" id="company" required></div>
                        <div class="mb-3"><label class="form-label">Apto Médico</label><select class="form-select" id="medical_clearance"><option value="Al día">Al día</option><option value="Vencido">Vencido</option></select></div>
                        <div class="mb-3"><label class="form-label">Estado</label><select class="form-select" id="status"><option value="Apto">Apto</option><option value="Observado">Observado</option></select></div>
                        <button type="submit" class="btn btn-success w-100">Guardar</button>
                    </form>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        let chartTypeInstance = null;
        let chartDaysInstance = null;

        async function cargarTodo() {
            const selectedMonth = document.getElementById('filter-month').value;

            // Cargar Incidentes
            const resInc = await fetch('/api/incidents');
            const dataInc = await resInc.json();
            
            // Filtrar por mes seleccionado si aplica
            const filteredInc = dataInc.filter(row => {
                if (selectedMonth === 'ALL') return true;
                return row.incident_date.startsWith(selectedMonth);
            });

            const tbodyInc = document.getElementById('tbody-incidents');
            tbodyInc.innerHTML = '';
            
            let totalAcc = filteredInc.length;
            let totalLostDays = 0;
            let propios = 0;
            let terceros = 0;

            filteredInc.forEach(row => {
                totalLostDays += row.lost_days;
                if(row.person_type === 'Propio') propios++; else terceros++;
                let badgeType = row.person_type === 'Propio' ? 'bg-primary' : 'bg-warning text-dark';
                tbodyInc.innerHTML += `
                    <tr>
                        <td>${row.id}</td>
                        <td>${row.incident_date}</td>
                        <td><strong>${row.project_name}</strong></td>
                        <td>${row.injured_name}</td>
                        <td><span class="badge ${badgeType}">${row.person_type}</span></td>
                        <td>${row.description}</td>
                        <td><span class="badge bg-secondary">${row.lost_days} días</span></td>
                        <td>${row.severity_type}</td>
                    </tr>
                `;
            });

            // Actualizar Tarjetas Gerenciales
            document.getElementById('stat-accidents').innerText = totalAcc + ' Siniestros';
            document.getElementById('stat-accidents-desc').innerText = `Propios: ${propios} | Terceros: ${terceros}`;
            document.getElementById('stat-lost-days').innerText = totalLostDays + ' Días';

            // Cálculo Automático de Índices (Base 25,000 Horas-Hombre mensuales)
            let hhTrabajadas = 25000; 
            let indiceFrecuencia = (totalAcc * 1000000) / hhTrabajadas;
            let indiceGravedad = (totalLostDays * 1000000) / hhTrabajadas;

            document.getElementById('stat-if').innerText = indiceFrecuencia.toFixed(2);
            document.getElementById('stat-ig').innerText = indiceGravedad.toFixed(2);

            // Renderizar Gráficos con Chart.js
            renderCharts(propios, terceros, totalLostDays);

            // Cargar Personal
            const resPers = await fetch('/api/personnel');
            const dataPers = await resPers.json();
            const tbodyPers = document.getElementById('tbody-personnel');
            tbodyPers.innerHTML = '';
            dataPers.forEach(row => {
                let badgeMed = row.medical_clearance === 'Vencido' ? 'bg-danger' : 'bg-success';
                tbodyPers.innerHTML += `<tr><td>${row.id}</td><td><strong>${row.full_name}</strong></td><td>${row.dni}</td><td>${row.company}</td><td><span class="badge ${badgeMed}">${row.medical_clearance}</span></td><td><span class="badge bg-primary">${row.status}</span></td></tr>`;
            });
        }

        function renderCharts(propios, terceros, lostDays) {
            // Gráfico 1: Propios vs Terceros (Pastel/Dona)
            const ctxType = document.getElementById('chartType').getContext('2d');
            if(chartTypeInstance) chartTypeInstance.destroy();
            chartTypeInstance = new Chart(ctxType, {
                type: 'doughnut',
                data: {
                    labels: ['Personal Propio', 'Personal Terceros'],
                    datasets: [{
                        data: [propios, terceros],
                        backgroundColor: ['#3b82f6', '#f59e0b']
                    }]
                },
                options: { responsive: true, maintainAspectRatio: false }
            });

            // Gráfico 2: Días Perdidos (Barras)
            const ctxDays = document.getElementById('chartDays').getContext('2d');
            if(chartDaysInstance) chartDaysInstance.destroy();
            chartDaysInstance = new Chart(ctxDays, {
                type: 'bar',
                data: {
                    labels: ['Días de Baja Médica'],
                    datasets: [{
                        label: 'Días Perdidos',
                        data: [lostDays],
                        backgroundColor: ['#ef4444']
                    }]
                },
                options: { responsive: true, maintainAspectRatio: false, scales: { y: { beginAtZero: true } } }
            });
        }

        document.getElementById('form-incident').addEventListener('submit', async (e) => {
            e.preventDefault();
            const payload = {
                incident_date: document.getElementById('incident_date').value,
                project_name: document.getElementById('inc_project').value,
                injured_name: document.getElementById('injured_name').value,
                person_type: document.getElementById('person_type').value,
                description: document.getElementById('description').value,
                lost_days: parseInt(document.getElementById('lost_days').value),
                severity_type: document.getElementById('severity_type').value
            };
            const res = await fetch('/api/incidents', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(payload) });
            if(res.ok) { bootstrap.Modal.getInstance(document.getElementById('modalIncident')).hide(); document.getElementById('form-incident').reset(); cargarTodo(); }
        });

        document.getElementById('form-personal').addEventListener('submit', async (e) => {
            e.preventDefault();
            const payload = {
                full_name: document.getElementById('full_name').value,
                dni: document.getElementById('dni').value,
                company: document.getElementById('company').value,
                medical_clearance: document.getElementById('medical_clearance').value,
                status: document.getElementById('status').value
            };
            const res = await fetch('/api/personnel', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(payload) });
            if(res.ok) { bootstrap.Modal.getInstance(document.getElementById('modalPersonal')).hide(); document.getElementById('form-personal').reset(); cargarTodo(); }
        });

        cargarTodo();
    </script>
</body>
</html>
"""

class SafeCoreHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path == '/' or self.path == '/index.html':
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(HTML_TEMPLATE.encode('utf-8'))
            elif self.path == '/api/incidents':
                conn = get_db_connection()
                rows = [dict(row) for row in conn.cursor().execute("SELECT * FROM incidents").fetchall()]
                conn.close()
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(rows).encode('utf-8'))
            elif self.path == '/api/personnel':
                conn = get_db_connection()
                rows = [dict(row) for row in conn.cursor().execute("SELECT * FROM personnel").fetchall()]
                conn.close()
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(rows).encode('utf-8'))
            else:
                self.send_response(404)
                self.end_headers()
        except (ConnectionAbortedError, ConnectionResetError, BrokenPipeError):
            pass

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        data = json.loads(self.rfile.read(content_length).decode('utf-8'))
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if self.path == '/api/incidents':
            cursor.execute("INSERT INTO incidents (incident_date, project_name, injured_name, person_type, description, lost_days, severity_type) VALUES (?, ?, ?, ?, ?, ?, ?)",
                           (data['incident_date'], data['project_name'], data['injured_name'], data['person_type'], data['description'], data['lost_days'], data['severity_type']))
        elif self.path == '/api/personnel':
            cursor.execute("INSERT INTO personnel (full_name, dni, company, medical_clearance, status) VALUES (?, ?, ?, ?, ?)",
                           (data['full_name'], data['dni'], data['company'], data['medical_clearance'], data['status']))
            
        conn.commit()
        conn.close()
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "success"}).encode('utf-8'))

if __name__ == '__main__':
    init_db()
    server_address = ('', PORT)
    httpd = http.server.HTTPServer(server_address, SafeCoreHandler)
    print(f"Servidor gerencial con gráficos mensuales corriendo en http://localhost:{PORT}")
    httpd.serve_forever()

if __name__ == "__main__":
    from http.server import HTTPServer, SimpleHTTPRequestHandler
    server_address = ('127.0.0.1', PORT)
    print(f"Servidor corriendo en http://localhost:{PORT}")
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    httpd.serve_forever()