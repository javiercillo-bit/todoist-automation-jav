# Todoist Label Rotation — GitHub Actions

Automatiza la rotación de etiquetas temporales en Todoist usando tres workflows independientes.

---

## Etiquetas que rota

| Ciclo | Etiquetas involucradas |
|---|---|
| **Diario** (00:00 Chile) | `Mañana → Hoy → Ayer → Atrasado` |
| **Semanal** (dom 23:59 Chile) | `Próxima semana → Esta semana → Semana pasada → Atrasado` |
| **Mensual** (último día del mes 23:59 Chile) | `Próximo mes → Este mes → Mes pasado → Atrasado` |

**Regla:** las tareas que ya tienen la etiqueta `Atrasado` son ignoradas.

---

## Setup

### 1. Crear el repositorio

Puedes usar un repo privado vacío. Solo necesitas la carpeta `.github/workflows/` con los tres archivos `.yml`.

### 2. Agregar el token de Todoist como Secret

1. Ve a tu Todoist → **Settings → Integrations → Developer**
2. Copia tu **API token**
3. En GitHub: **Settings → Secrets and variables → Actions → New repository secret**
4. Nombre: `TODOIST_API_TOKEN`
5. Valor: tu token

### 3. Verificar nombres de etiquetas

Asegúrate de que las etiquetas en Todoist se llamen **exactamente** así (sensible a mayúsculas y tildes):

- `Mañana`, `Hoy`, `Ayer`
- `Próxima semana`, `Esta semana`, `Semana pasada`
- `Próximo mes`, `Este mes`, `Mes pasado`
- `Atrasado`

### 4. Probar manualmente

En GitHub, ve a **Actions → [nombre del workflow] → Run workflow** para dispararlo sin esperar el cron.

---

## Zona horaria

Los workflows usan `UTC-3` (horario de verano de Chile). Si en invierno hay desfase de una hora, puedes ajustar los cron así:

| Workflow | Cron actual (verano UTC-3) | Cron invierno (UTC-4) |
|---|---|---|
| Diario | `0 3 * * *` | `0 4 * * *` |
| Semanal | `59 2 * * 1` | `59 3 * * 1` |
| Mensual | `59 2 28-31 * *` | `59 3 28-31 * *` |

---

## Notas técnicas

- El workflow mensual corre los días 28–31 pero **solo ejecuta la rotación si es el último día real del mes** (verificación interna en Python). Febrero queda cubierto automáticamente.
- El orden de rotación en cada script va de la etiqueta más vieja a la más nueva para evitar que una tarea rote dos veces en el mismo run.
- Se aplica un delay de 300ms entre cada actualización para respetar el rate limit de la API de Todoist.
