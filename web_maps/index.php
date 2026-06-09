<?php
// WC3 Maps List - simple PHP page for EpicWar links
// Credits: ChatGPT OpenAI y Azzlaer para LatinBattle.com
$dataFile = __DIR__ . '/maps.json';
if (!file_exists($dataFile)) file_put_contents($dataFile, json_encode([], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));
$maps = json_decode(file_get_contents($dataFile), true) ?: [];
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $maps[] = [
        'title' => trim($_POST['title'] ?? ''),
        'url' => trim($_POST['url'] ?? ''),
        'comment' => trim($_POST['comment'] ?? ''),
        'user' => trim($_POST['user'] ?? 'Azzlaer'),
        'date' => date('Y-m-d H:i:s'),
    ];
    file_put_contents($dataFile, json_encode($maps, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));
    header('Location: index.php'); exit;
}
?>
<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>WC3 Mapas más jugados</title><link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
<style>body{background:#07130b;color:#e8f4df}.card,.table{background:#102018;color:#e8f4df}.text-gold{color:#d6a642}.btn-orc{background:#1e8e3e;color:white}.form-control{background:#0c1a10;color:#e8f4df;border-color:#315c3e}</style>
</head><body><div class="container py-4"><h1 class="text-gold">⚔️ Mapas Warcraft III - EpicWar</h1><p>Listado comunitario de mapas populares.</p>
<div class="card p-3 mb-4"><form method="post" class="row g-2"><div class="col-md-3"><input class="form-control" name="title" placeholder="Nombre mapa" required></div><div class="col-md-3"><input class="form-control" name="url" placeholder="https://www.epicwar.com/maps/..." required></div><div class="col-md-2"><input class="form-control" name="user" placeholder="Usuario"></div><div class="col-md-3"><input class="form-control" name="comment" placeholder="Comentario"></div><div class="col-md-1"><button class="btn btn-orc w-100">Agregar</button></div></form></div>
<table class="table table-dark table-striped align-middle"><thead><tr><th>Mapa</th><th>Enlace</th><th>Comentario</th><th>Usuario</th><th>Fecha</th></tr></thead><tbody>
<?php foreach(array_reverse($maps) as $m): ?><tr><td><?=htmlspecialchars($m['title'])?></td><td><a href="<?=htmlspecialchars($m['url'])?>" target="_blank">Descargar</a></td><td><?=htmlspecialchars($m['comment'])?></td><td><?=htmlspecialchars($m['user'])?></td><td><?=htmlspecialchars($m['date'])?></td></tr><?php endforeach; ?>
</tbody></table><footer class="small text-secondary">Créditos: ChatGPT OpenAI y Azzlaer para LatinBattle.com</footer></div></body></html>
