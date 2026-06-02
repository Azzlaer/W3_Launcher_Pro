<?php
$mapsFile = __DIR__ . '/maps.json';
if (!file_exists($mapsFile)) {
    file_put_contents($mapsFile, json_encode([], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $maps = json_decode(file_get_contents($mapsFile), true) ?: [];
    $maps[] = [
        'name' => trim($_POST['name'] ?? ''),
        'epicwar_url' => trim($_POST['epicwar_url'] ?? ''),
        'comment' => trim($_POST['comment'] ?? ''),
        'user' => trim($_POST['user'] ?? 'Anonimo'),
        'date' => date('Y-m-d H:i:s'),
    ];
    file_put_contents($mapsFile, json_encode($maps, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));
    header('Location: index.php?ok=1');
    exit;
}

$maps = json_decode(file_get_contents($mapsFile), true) ?: [];
?>
<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Mapas Warcraft III - LatinBattle</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
<style>
body{background:#0d1117;color:#e6edf3}.card{background:#161b22;border:1px solid #30363d}.form-control{background:#0d1117;color:#e6edf3;border-color:#30363d}.form-control:focus{background:#0d1117;color:#fff}.table{--bs-table-bg:#161b22;--bs-table-color:#e6edf3;--bs-table-border-color:#30363d}.badge{font-size:.8rem}
a{color:#58a6ff}.hero{border:1px solid #30363d;border-radius:18px;padding:22px;background:linear-gradient(135deg,#161b22,#0d1117)}
</style>
</head>
<body>
<div class="container py-4">
  <div class="hero mb-4">
    <h1>⚔️ Mapas Warcraft III - LatinBattle</h1>
    <p class="mb-0">Listado colaborativo de mapas populares con enlaces de EpicWar, comentarios, usuario y fecha de ingreso.</p>
  </div>

  <?php if (isset($_GET['ok'])): ?><div class="alert alert-success">Mapa agregado correctamente.</div><?php endif; ?>

  <div class="row g-4">
    <div class="col-lg-8">
      <div class="card p-3">
        <h4>📜 Listado</h4>
        <div class="table-responsive">
          <table class="table table-hover align-middle">
            <thead><tr><th>Mapa</th><th>EpicWar</th><th>Usuario</th><th>Fecha</th><th>Comentario</th></tr></thead>
            <tbody>
            <?php foreach ($maps as $map): ?>
              <tr>
                <td><?= htmlspecialchars($map['name'] ?? '') ?></td>
                <td><a href="<?= htmlspecialchars($map['epicwar_url'] ?? '#') ?>" target="_blank">Descargar / Ver</a></td>
                <td><span class="badge text-bg-primary"><?= htmlspecialchars($map['user'] ?? '') ?></span></td>
                <td><?= htmlspecialchars($map['date'] ?? '') ?></td>
                <td><?= htmlspecialchars($map['comment'] ?? '') ?></td>
              </tr>
            <?php endforeach; ?>
            </tbody>
          </table>
        </div>
      </div>
    </div>
    <div class="col-lg-4">
      <div class="card p-3">
        <h4>➕ Agregar mapa</h4>
        <form method="post">
          <label class="form-label">Nombre del mapa</label>
          <input class="form-control mb-2" name="name" required>
          <label class="form-label">URL EpicWar</label>
          <input class="form-control mb-2" name="epicwar_url" placeholder="https://www.epicwar.com/maps/349240/" required>
          <label class="form-label">Usuario</label>
          <input class="form-control mb-2" name="user" value="Azzlaer">
          <label class="form-label">Comentario</label>
          <textarea class="form-control mb-3" name="comment" rows="4"></textarea>
          <button class="btn btn-primary w-100">Guardar</button>
        </form>
      </div>
    </div>
  </div>
</div>
</body>
</html>
