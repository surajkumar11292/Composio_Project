import json
import os
from datetime import datetime

def generate_html():
    if not os.path.exists("data/apps_research.json") or not os.path.exists("data/patterns_analysis.json"):
        print("Run Phase 3 and Phase 4 first.")
        return
        
    with open("data/apps_research.json", "r") as f:
        apps = json.load(f)
        
    with open("data/patterns_analysis.json", "r") as f:
        stats = json.load(f)
        
    # Read template (we'll just use a f-string for simplicity, but injecting data as a global JS variable)
    
    js_data = f"""
    const APPS_DATA = {json.dumps(apps)};
    const STATS_DATA = {json.dumps(stats)};
    """
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Composio AI - Research Agent Dashboard</title>
    <meta name="description" content="AI Product Ops Intern case study - 100 Apps researched.">
    
    <!-- Impeccable modern fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    
    <!-- Feather icons -->
    <script src="https://unpkg.com/feather-icons"></script>
    
    <link rel="stylesheet" href="styles.css">
</head>
<body class="dark-theme">
    <div class="glass-bg"></div>
    <div class="glass-bg-2"></div>
    
    <nav class="navbar">
        <div class="nav-content">
            <div class="logo">
                <i data-feather="hexagon" class="brand-icon"></i>
                <span>Composio <span class="highlight">Intelligence</span></span>
            </div>
            <div class="nav-links">
                <a href="#overview">Overview</a>
                <a href="#apps">App Registry</a>
                <a href="https://composio.dev" target="_blank" class="btn-primary">View MCP Gateway</a>
            </div>
        </div>
    </nav>

    <main class="container">
        <!-- Hero Section -->
        <header class="hero">
            <div class="badge">AI Product Ops Assignment</div>
            <h1 class="hero-title">API Ecosystem <br/><span class="text-gradient">Research Synthesis</span></h1>
            <p class="hero-subtitle">Automated analysis of 100 SaaS applications for MCP Gateway integration readiness.</p>
        </header>

        <!-- Stats Grid -->
        <section id="overview" class="stats-grid">
            <div class="stat-card reveal">
                <div class="stat-icon"><i data-feather="check-circle"></i></div>
                <div class="stat-value">{stats['total_apps']}</div>
                <div class="stat-label">Total Apps Researched</div>
            </div>
            <div class="stat-card reveal" style="animation-delay: 0.1s;">
                <div class="stat-icon" style="color: var(--success); background: var(--success-bg)"><i data-feather="zap"></i></div>
                <div class="stat-value">{len(stats.get('easy_wins', []))}</div>
                <div class="stat-label">Ready for Integration</div>
            </div>
            <div class="stat-card reveal" style="animation-delay: 0.2s;">
                <div class="stat-icon" style="color: var(--accent); background: var(--accent-bg)"><i data-feather="server"></i></div>
                <div class="stat-value">{stats['mcp_coverage']['has_mcp']}</div>
                <div class="stat-label">Existing MCP Servers</div>
            </div>
            <div class="stat-card reveal" style="animation-delay: 0.3s;">
                <div class="stat-icon" style="color: var(--warning); background: var(--warning-bg)"><i data-feather="lock"></i></div>
                <div class="stat-value">{sum(1 for a in apps if "Sales" in a.get("access_tier", ""))}</div>
                <div class="stat-label">Enterprise Gated</div>
            </div>
        </section>

        <!-- Executive Narrative -->
        <section class="narrative-section reveal">
            <div class="section-header">
                <h2><i data-feather="file-text"></i> Executive Synthesis</h2>
            </div>
            <div class="narrative-content markdown-body" id="narrative-container">
                <!-- Injected via JS -->
            </div>
            <div class="production-path">
                <h3>Production Scale Path: Composio MCP Gateway</h3>
                <p>While this agent built its own custom tools for demonstration, in a production setting we would leverage the <strong>Composio MCP Gateway</strong>. This provides immediate access to 100+ authenticated tools out-of-the-box, completely removing the need to manage OAuth flows, rate limits, and tool schemas manually.</p>
            </div>
        </section>

        <!-- Data Table -->
        <section id="apps" class="table-section reveal">
            <div class="section-header">
                <h2><i data-feather="database"></i> Researched Registry</h2>
                <div class="search-box">
                    <i data-feather="search"></i>
                    <input type="text" id="searchInput" placeholder="Search apps by name, category, or auth...">
                </div>
            </div>
            
            <div class="table-container">
                <table id="appsTable">
                    <thead>
                        <tr>
                            <th>App Name</th>
                            <th>Category</th>
                            <th>Auth Pattern</th>
                            <th>Access Tier</th>
                            <th>Buildability</th>
                        </tr>
                    </thead>
                    <tbody id="tableBody">
                        <!-- Populated by JS -->
                    </tbody>
                </table>
            </div>
        </section>
    </main>
    
    <footer>
        <p>Built with ❤️ by Suraj for Composio AI | {datetime.now().strftime('%B %Y')}</p>
    </footer>

    <script>
        // Inject Data
        {js_data}
        
        // Initialize Icons
        feather.replace();
        
        // Render Narrative
        document.getElementById('narrative-container').innerHTML = window.marked ? marked.parse(STATS_DATA.executive_narrative) : `<p>${{STATS_DATA.executive_narrative.replace(/\\n/g, '<br>')}}</p>`;

        // Render Table
        function renderTable(data) {{
            const tbody = document.getElementById('tableBody');
            tbody.innerHTML = '';
            
            data.forEach(app => {{
                const tr = document.createElement('tr');
                
                // Status Badge Logic
                let statusClass = 'badge-neutral';
                if(app.buildability === 'Ready to Build') statusClass = 'badge-success';
                if(app.buildability === 'Partially Ready') statusClass = 'badge-warning';
                if(app.buildability.includes('Blocked')) statusClass = 'badge-danger';
                
                tr.innerHTML = `
                    <td>
                        <div class="app-name">
                            <strong>${{app.name}}</strong>
                            ${{app.has_mcp_server ? '<span class="mcp-badge">Has MCP</span>' : ''}}
                        </div>
                    </td>
                    <td>${{app.category}}</td>
                    <td><span class="auth-pill">${{app.auth_methods.join(', ')}}</span></td>
                    <td>${{app.access_tier}}</td>
                    <td><span class="status-badge ${{statusClass}}">${{app.buildability}}</span></td>
                `;
                tbody.appendChild(tr);
            }});
        }}
        
        renderTable(APPS_DATA);
        
        // Search functionality
        document.getElementById('searchInput').addEventListener('input', (e) => {{
            const term = e.target.value.toLowerCase();
            const filtered = APPS_DATA.filter(app => 
                app.name.toLowerCase().includes(term) ||
                app.category.toLowerCase().includes(term) ||
                app.auth_methods.join(' ').toLowerCase().includes(term)
            );
            renderTable(filtered);
        }});
        
        // Intersection Observer for scroll animations
        const observer = new IntersectionObserver((entries) => {{
            entries.forEach(entry => {{
                if (entry.isIntersecting) {{
                    entry.target.classList.add('active');
                }}
            }});
        }}, {{ threshold: 0.1 }});
        
        document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
    </script>
</body>
</html>
"""
    
    with open("dashboard/index.html", "w", encoding='utf-8') as f:
        f.write(html_content)
        
    print("Dashboard HTML generated at dashboard/index.html")

if __name__ == "__main__":
    generate_html()
