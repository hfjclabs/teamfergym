# GymOS · App para el celular

Esta carpeta convierte GymOS en una **app instalable** con el icono de tu gimnasio:
se abre a pantalla completa (sin barras del navegador), tiene pantalla de carga propia,
y permite que el cronómetro avise en la barra de notificaciones y mantenga la pantalla
encendida mientras el socio entrena.

Por dentro sigue siendo el mismo GymOS de Apps Script: esta carpeta es solo la "carcasa".

---

## Por qué hace falta

Google Apps Script sirve la app desde `script.google.com` dentro de un marco cerrado.
Ahí el navegador **no** deja instalar una app propia ni poner tu icono: si haces
"Agregar a pantalla de inicio" te queda el icono de Google y se abre como una pestaña.

La carcasa vive en una dirección tuya (gratis en GitHub Pages) y desde ahí sí se puede:
tu icono, tu nombre, pantalla completa y avisos.

---

## Publicarla — 10 minutos, gratis

### 1. Configura los dos archivos

**`config.js`** — pega la URL de tu aplicación web (la que termina en `/exec`):

```js
url: 'https://script.google.com/macros/s/AKfycb.../exec',
nombre: 'PowerGym',
nombreLargo: 'PowerGym · Gestión',
color: '#f97316',
```

**`manifest.json`** — cambia estas cuatro líneas por lo mismo:

```json
"name": "PowerGym · Gestión",
"short_name": "PowerGym",
"theme_color": "#f97316",
"background_color": "#0a0c11",
```

> `short_name` es lo que sale debajo del icono en el celular: máximo 12 caracteres.

### 2. Cambia el icono (opcional)

Vienen unos iconos con una mancuerna sobre tu color. Para poner el logo del gimnasio
tienes dos caminos:

- **Con Python** (si lo tienes instalado):
  `python3 crear-iconos.py "#f97316" mi-logo.png`
- **A mano**: reemplaza los archivos de la carpeta `icons/` con los tuyos, respetando
  los nombres y tamaños:

| Archivo | Tamaño | Para qué |
|---|---|---|
| `icono-192.png` | 192×192 | Icono normal |
| `icono-512.png` | 512×512 | Icono grande y pantalla de carga |
| `icono-maskable-192.png` | 192×192 | Android recorta los bordes: deja aire alrededor |
| `icono-maskable-512.png` | 512×512 | Igual, en grande |
| `apple-touch-icon.png` | 180×180 | iPhone (sin transparencia) |
| `badge-96.png` | 96×96 | Símbolo blanco de la barra de notificaciones |

### 3. Súbela a GitHub Pages

1. Entra a <https://github.com> y crea una cuenta si no la tienes.
2. **New repository** → nombre `gym` → **Public** → *Create*.
3. **uploading an existing file** → arrastra **todo el contenido** de esta carpeta
   (`index.html`, `config.js`, `manifest.json`, `sw.js` y la carpeta `icons`) → *Commit changes*.
4. **Settings → Pages** → en *Branch* elige `main` y `/ (root)` → **Save**.
5. Espera un minuto: arriba aparece tu dirección, algo como
   `https://tuusuario.github.io/gym/`.

> Sirve igual **Netlify Drop** (<https://app.netlify.com/drop>): arrastras la carpeta y listo.
> Lo único que importa es que quede en **https**.

### 4. Instálala

- **Android (Chrome):** abre la dirección → a los pocos segundos sale el botón
  **Instalar** abajo, o usa **⋮ → Instalar aplicación**.
- **iPhone (Safari):** abre la dirección → **Compartir → Agregar a pantalla de inicio**.

Queda con el icono del gimnasio, sin barra de direcciones y con su propia ventana.
Manda esa misma dirección a los socios por WhatsApp.

---

## Qué gana el socio al instalarla

| | En el navegador | Con la app instalada |
|---|---|---|
| Icono propio del gimnasio | ✗ | ✓ |
| Pantalla completa, sin barras | ✗ | ✓ |
| El cronómetro sigue contando al cerrar | ✓ | ✓ |
| Aviso en la barra de notificaciones | ✗ | ✓ (Android) |
| Vibra al terminar el descanso | ✓ | ✓ |
| La pantalla no se apaga entrenando | ✗ | ✓ |
| Atajos al mantener pulsado el icono | ✗ | ✓ (Android) |

---

## Lo que un sitio web **no** puede hacer

Para no prometer de más:

- **No existe un cronómetro que siga corriendo en segundo plano como Spotify.** Ninguna
  app web puede hacerlo. Lo que sí hace GymOS es contar por **hora de reloj**, no por
  segundos acumulados: aunque el celular se bloquee o el socio cierre la app, al volver
  el cronómetro está en el segundo exacto. No se pierde nada.
- **El aviso de la barra se actualiza mientras la app está abierta o recién cerrada.**
  Cuando Android duerme la app, el número deja de refrescarse, pero el aviso se queda
  visible y al tocarlo vuelve a la app ya puesta al día.
- **En iPhone las notificaciones** solo funcionan si la app está agregada a la pantalla
  de inicio (iOS 16.4 o superior). La vibración no está disponible.
- **La cámara del escáner QR** sigue sin poder abrirse en vivo dentro del marco de
  Apps Script; por eso el botón **📸 Tomar foto del QR**, que funciona siempre.

---

## Actualizar la carcasa

Si cambias algo aquí, sube los archivos de nuevo a GitHub y aumenta el número en la
línea `const CACHE = 'gymos-carcasa-v3';` de `sw.js` (v4, v5…). Así los celulares
descargan la versión nueva en vez de la guardada.

Los cambios del sistema (Apps Script) no necesitan nada de esto: entran solos.

---

*GymOS · Desarrollado por Heiner Jaimes*
