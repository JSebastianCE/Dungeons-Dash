# Dungeons Dash

**Dungeons Dash** es un juego de carreras arcade con temática medieval/fantástica desarrollado en **Unreal Engine 5.7**.  
El proyecto combina conducción tipo kart, uso de cartas/power-ups, mecánicas de drift, saltos, checkpoints y un mapa ambientado en un sótano liminal de los 90 con elementos de fantasía y juegos de mesa.

## Descripción del juego

En Dungeons Dash, los jugadores controlan pequeños vehículos inspirados en clases medievales dentro de un entorno gigante a escala de juguete.  
Durante la carrera, los jugadores recogen cartas flotantes distribuidas en la pista. Estas cartas otorgan power-ups que pueden usarse para atacar, defenderse, ganar velocidad, colocar trampas o recuperarse si van rezagados.

El objetivo principal es completar la carrera pasando por checkpoints, usando cartas estratégicamente y aprovechando mecánicas de conducción como drift, salto y mini-turbo.

---

## Motor y plantilla base

- **Motor:** Unreal Engine 5.7
- **Template:** Games → Vehicle
- **Variant:** All
- **Base recomendada:** Offroad Vehicle
- **Tipo de proyecto:** Blueprint-first

Aunque el proyecto se desarrolla principalmente con Blueprints, se deja abierta la posibilidad de usar C++ si en el futuro se necesitan sistemas más técnicos, optimización o plugins.

---

## Alcance del MVP

El MVP se enfoca en estructura, jugabilidad y game loop funcional.  
No se priorizan arte final, VFX, sonido, menús pulidos ni HUD visual definitivo.

### Sistemas principales

- Vehículo arcade funcional.
- Aceleración, frenado y giro.
- Salto.
- Drift y mini-turbo.
- Pickups flotantes que entregan cartas.
- Inventario de cartas.
- Uso obligatorio de cartas, sin descarte manual.
- Selección de cartas con cruceta izquierda/derecha.
- Power-ups básicos.
- Checkpoints.
- Vueltas.
- Posición de carrera.
- Game loop completo.
- Mapa funcional de prueba.

---

## Reglas principales de cartas

Las cartas se obtienen al pasar por actores flotantes colocados en la pista.

### Selección de cartas

| Input | Acción |
|---|---|
| Cruceta izquierda | Seleccionar carta anterior |
| Cruceta derecha | Seleccionar carta siguiente |

### Uso de cartas

Las cartas no se pueden descartar manualmente.  
Si el inventario está lleno, el jugador debe usar una carta para liberar espacio.

---

## Power-ups básicos del MVP

| Power-up | Función |
|---|---|
| Poción de velocidad | Aplica un boost temporal |
| Bola de fuego | Proyectil recto frontal |
| Flecha encantada | Proyectil guiado |
| Escudo arcano | Bloquea un ataque |
| Barril explosivo | Trampa colocada en la pista |
| Bendición de recuperación | Ayuda al jugador rezagado |

---

## Estructura recomendada del proyecto

```text
/Content/DungeonsDash/
    _Core/
        Input/
        Data/
        BlueprintInterfaces/

    Actors/
        Vehicles/
        Pickups/
        Projectiles/
        Traps/

    Environment/
        Track/

    UI/
