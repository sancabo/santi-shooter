# generic-shooter

A top-down shooter game built from scratch in Python — no engine, no framework, no tutorials followed. Written as a learning exercise to understand both Python and the internal mechanics that power real game engines.

![](https://storage.googleapis.com/santi-documents/game.jpg "Game Image 1")

---

## Why this project exists

I built this to prove to myself — and to anyone reviewing my work — that I can engineer something from scratch outside my main area of expertise. I didn't use Unity, Godot, or any game framework. I reasoned through the problems independently and converged on many of the same solutions that professional game engines use, often without knowing those solutions had names.

The rest of this README documents what I discovered.

---

## Proto-patterns: game engine internals I re-invented

Below are the architectural patterns I implemented, along with how they map to the standard industry terminology I learned *after* writing the code.

### 1. Fixed-Timestep Game Loop
**Where:** `main.py` — `Game.run()`

The core loop accumulates elapsed wall-clock time in a `lag` counter and calls `update_logic` in fixed 17 ms slices (≈60 Hz) until the lag is consumed. Rendering happens once per visual frame with the leftover lag passed in as an interpolation hint.

This is the canonical "Fix Your Timestep" pattern described by Glenn Fiedler, and is how Unity separates `FixedUpdate` from `Update`.

```
while lag >= MS_PER_UPDATE:
    update_logic(MS_PER_UPDATE)
    lag -= MS_PER_UPDATE
render(lag / MS_PER_UPDATE)   # interpolation percentage
```

---

### 2. Delta Time
**Where:** `lag` parameter throughout `update_state(lag)` calls

Every object that moves or ticks receives `lag` (milliseconds since last update). All physics calculations divide by `ONE_SEC = 1000` to produce frame-rate-independent results:

```python
self.__current_speed_x += self.__acceleration_x * lag / ONE_SEC
```

This is identically what `Time.deltaTime` does in Unity.

---

### 3. Scene Graph (Scene Tree)
**Where:** `first_level.py` — `self.__sceneTree`

All renderable objects are stored in an ordered list. Each frame, the scene tree is iterated and every node's `render()` is called. Nodes are added (spawned enemies, damage text, UI overlays) and removed dynamically during gameplay.

```python
self.__sceneTree: [Drawable] = []
# ...
for entity in self.__sceneTree:
    entity.render(percentage, graphics)
```

This is the same concept as a scene hierarchy in Unity or Godot.

---

### 4. Game State Stack (Scene Stack)
**Where:** `internals.py` — `GameState`, `main.py` — `game_state_stack`

Game screens (playing, paused, game over) are managed as a LIFO stack of `GameState` objects. Pushing a new state transitions to it; popping returns to the previous one. The main loop always executes the top-of-stack state.

```python
def go_to_state(self, new_state):
    self.__state_queue.put(new_state)   # push

def go_previous_state(self):
    self.__state_queue.get_nowait()     # pop
```

This is the Game State / Scene Stack pattern used in virtually every shipped game. Unity's `SceneManager.LoadScene` with additive loading is a managed version of the same idea.

---

### 5. Null Object Pattern for Game Termination
**Where:** `internals.py` — `NullGameState`

Rather than scattering null-checks through the loop, a sentinel `NullGameState` sits at the bottom of the stack. When it becomes the active state it raises `GameClosedException`, cleanly signaling the main loop to exit. No special-case code needed anywhere else.

---

### 6. Component-style Mixins (Proto-ECS)
**Where:** `entities/base.py` — `Drawable`, `Collisionable`, `Moveable`

Behavior is split into separate abstract base classes, which entities compose via Python multiple inheritance:

```python
class Player(Drawable, Collisionable): ...
class Enemy(Drawable, Collisionable): ...
class Bounds(Drawable, Collisionable): ...
```

This mirrors Unity's Component model (`Renderer`, `Collider`, `Rigidbody` as separate attachable behaviors) and is a stepping stone toward a true Entity-Component-System architecture.

---

### 7. Updateable Lifecycle Interface
**Where:** `first_level.py` — `self.__updateables`, every entity's `update_state(lag)` and `is_done()`

Every active object implements two methods: `update_state(lag)` to advance its internal state, and `is_done()` to signal when it should be removed. The level iterates `__updateables` each tick and evicts finished objects automatically.

This is the same lifecycle that Unity enforces with `Update()`, `OnDestroy()`, and `enabled`.

---

### 8. Render Interpolation
**Where:** `main.py` → `render(lag / MS_PER_UPDATE, graphics)`, `player.py` and `enemy.py` — `render(percentage, ...)`

The `percentage` value (0.0–1.0) represents how far between two physics ticks the current render frame falls. Entities apply a fractional movement delta during rendering to produce smooth visuals even when the render rate differs from the physics rate:

```python
deltas = self.__calculate_movement_deltas(0, percentage)
self.__player_box = self.__player_box.move(deltas[0], deltas[1])
```

This is the interpolation step described in the "Fix Your Timestep" article and is what separates smooth 60 fps rendering from choppy physics-tick rendering.

---

### 9. Input Event Queue
**Where:** `input.py` — `InputListener`, consumed in `internals.py` — `GameState.update_logic()`

Input events are captured on a separate thread, serialised into a `Queue` as named `Event` objects, and consumed during the logic update step. This decouples hardware input from game logic and is the same producer-consumer pattern that Unity's `Input` system and Unreal's `PlayerController` abstract over.

Key bindings map keys to semantic event pairs (press / release), e.g.:

```python
keyboard.Key.up: [Event("move-up"), Event("stop-move-up")]
```

---

### 10. Sprite Sheet Sampling
**Where:** `player.py` — `render()`, `enemy.py` — `render()`

Both player and enemy read frames from sprite atlases by computing a grid offset from the current animation frame or orientation angle. No external animation library — pure arithmetic on texture coordinates.

```python
sprite_number = self.__orientation // 15
x, y = sprite_number % 5, sprite_number // 5
size = 830 // 5
sprite_sheet_box = pygame.Rect(x * size, y * size, size, size)
```

---

### 11. Physics-based Movement (Acceleration / Friction Model)
**Where:** `player.py` — `__calculate_velocity_x/y`, `__apply_slippery_instance_x/y`

Player velocity is driven by an acceleration vector clamped to a top speed. When acceleration is zero, a configurable friction (`__natural_friction` / "slippery factor") gradually decelerates the entity. This produces the same feel as a `Rigidbody` with drag in Unity.

---

### 12. AABB Collision Detection & Resolution
**Where:** `entities/base.py` — `Collisionable.is_touching()`, `is_inside()`, `first_level.py` — `__resolve_collisions()`, `relocate_out_of_bounds_player()`

Axis-Aligned Bounding Box overlap tests are performed each tick. On boundary violations the player's position is corrected by the exact overlap amount — identical to what a physics engine's depenetration solver does.

---

### 13. Scripted Timeline (Cutscene / Director)
**Where:** `gamestates/timed_events.py` — `TimedEvents`, `scenario_events`

A list of `(seconds, Event)` tuples acts as a scripted scenario timeline. `TimedEvents.update_state()` fires events when elapsed time crosses each timestamp. This is the same concept as Unity's `Timeline` / `Playable Director` or a cinematic sequencer.

```python
scenario_events = [
    (0,  Event("spawn_enemy_lineal_wave", ["top", 15])),
    (5,  Event("spawn_enemy_lineal_wave", ["left", 15])),
    ...
    (121, Event("stage_cleared", []))
]
```

---

### 14. Enemy Spawner / Object Factory
**Where:** `entities/spawner.py` — `LinealWaveEnemySpawner`, `RandomDirectionEnemySpawner`

Spawner objects encapsulate spawn timing, quantity, and positioning logic. They produce enemies through a `get_produced_enemies()` pull interface and self-report termination via `is_terminated()`. This is the Factory + Object Pool pattern commonly used in enemy wave systems.

---

### 15. Invincibility Frames (I-frames)
**Where:** `player.py` — `__invulnerable_ms_left`

After taking damage the player enters a timed invulnerability window. The timer counts down each update tick — a ubiquitous game design mechanic implemented here with the same delta-time approach as all other timers in the codebase.

---

### 16. Renderer / Graphics Abstraction Layer
**Where:** `graphics.py` — `Graphics`, `Sprite`

All pygame-specific calls are isolated behind `Graphics.draw_entity()` and the `Sprite` wrapper. The game objects never call pygame directly — a deliberate boundary that would allow swapping the renderer without touching entity code. This is the same goal as Unity's `UnityEngine.Graphics` abstraction or Godot's `RenderingServer`.

---

### 17. Sub-state Machine
**Where:** `first_level.py` — `self.__sub_state`

Within a single game state, a string-based sub-state (`"normal"`, `"game_over"`) gates which events are processed and which systems are active. This is a simplified Finite State Machine — the foundation of almost every character controller and game flow system.

---

## Tech stack

- **Python 3** — language
- **pygame** — display, audio, input primitives
- **pynput** — raw keyboard / mouse listener (runs on a separate thread)

## Credits

Assets: [opengameart.org](https://opengameart.org) · [zapsplat.com](https://www.zapsplat.com)
