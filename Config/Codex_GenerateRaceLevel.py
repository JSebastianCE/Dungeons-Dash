import math
import unreal


SOURCE_MAP = "/Game/DungeonsDash/LvL/NewMap"
TARGET_MAP = "/Game/DungeonsDash/LvL/LVL_DungeonDash_Circuit"
CUBE = unreal.load_asset("/Engine/BasicShapes/Cube")
CHECKPOINT_BP = unreal.load_asset("/Game/DungeonsDash/Actors/CheckPoints/CheckPoint")
BOOST_BP = unreal.load_asset("/Game/DungeonsDash/Boost/BP_BoostPad")
SPLINE_TRACK_BP = unreal.load_asset("/Game/VehicleTemplate/Blueprints/Tools/BP_SplineMesh")
TRACK_MESH = unreal.load_asset("/Game/VehicleTemplate/Meshes/SM_Track_10M")
VEHICLE_BP = unreal.load_asset("/Game/DungeonsDash/Actors/Vehicles/BP_DashVehicle")
RACING_GM_BP = unreal.load_asset("/Game/DungeonsDash/_Core/GameModes/GM_RacingGame")


def spawn_cube(label, location, scale, yaw=0.0, tags=None):
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.StaticMeshActor,
        unreal.Vector(*location),
        unreal.Rotator(pitch=0.0, yaw=yaw, roll=0.0),
    )
    actor.set_actor_label(label)
    actor.static_mesh_component.set_static_mesh(CUBE)
    actor.set_actor_scale3d(unreal.Vector(*scale))
    actor.tags = ["CodexGenerated", "RaceTrack"] + list(tags or [])
    return actor


def spawn_blueprint(asset, label, location, rotation=(0.0, 0.0, 0.0), tags=None):
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        asset.generated_class(),
        unreal.Vector(*location),
        unreal.Rotator(pitch=rotation[0], yaw=rotation[1], roll=rotation[2]),
    )
    actor.set_actor_label(label)
    actor.tags = ["CodexGenerated"] + list(tags or [])
    return actor


if not all((CUBE, CHECKPOINT_BP, BOOST_BP, SPLINE_TRACK_BP, TRACK_MESH, VEHICLE_BP, RACING_GM_BP)):
    raise RuntimeError("Missing one or more required race assets")

if unreal.EditorAssetLibrary.does_asset_exist(TARGET_MAP):
    unreal.EditorAssetLibrary.delete_asset(TARGET_MAP)
if not unreal.EditorAssetLibrary.duplicate_asset(SOURCE_MAP, TARGET_MAP):
    raise RuntimeError(f"Could not duplicate {SOURCE_MAP} to {TARGET_MAP}")
if not unreal.EditorLoadingAndSavingUtils.load_map(TARGET_MAP):
    raise RuntimeError(f"Could not load {TARGET_MAP}")

# Replace the placeholder floor/track with a self-contained circuit.
for actor in unreal.EditorLevelLibrary.get_all_level_actors():
    if actor.get_actor_label() in ("Floor", "cartoon_race_track_oval"):
        unreal.EditorLevelLibrary.destroy_actor(actor)

# Large technical circuit inspired by the reference: two real straights, sweepers,
# hairpins and an S section. The duplicated first point closes the generated meshes.
track_points = [
    (-3000.0, -6000.0, 0.0),
    (0.0, -6000.0, 0.0),
    (3500.0, -6000.0, 0.0),
    (6000.0, -5200.0, 100.0),
    (7200.0, -3300.0, 180.0),
    (6200.0, -1200.0, 100.0),
    (4200.0, -1800.0, 0.0),
    (3000.0, 100.0, 100.0),
    (4800.0, 1800.0, 200.0),
    (7200.0, 3200.0, 250.0),
    (6500.0, 5400.0, 120.0),
    (3500.0, 6200.0, 0.0),
    (0.0, 6200.0, 0.0),
    (-3000.0, 6200.0, 0.0),
    (-6200.0, 5200.0, 120.0),
    (-7600.0, 3000.0, 220.0),
    (-6500.0, 800.0, 120.0),
    (-4300.0, 1700.0, 40.0),
    (-2500.0, 3600.0, 100.0),
    (-500.0, 2600.0, 40.0),
    (-1800.0, 400.0, 80.0),
    (-4200.0, -800.0, 120.0),
    (-6100.0, -3000.0, 180.0),
    (-5200.0, -5200.0, 80.0),
    (-3000.0, -6000.0, 0.0),
]
track_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
    SPLINE_TRACK_BP.generated_class(), unreal.Vector(), unreal.Rotator()
)
track_actor.set_actor_label("RaceTrack_Spline_Main")
track_actor.tags = ["CodexGenerated", "RaceTrack", "SplineTrack"]
track_actor.set_editor_property("Target", TRACK_MESH)
spline = track_actor.get_editor_property("Spline")
spline.clear_spline_points(False)
for index, point in enumerate(track_points):
    spline.add_spline_point(unreal.Vector(*point), unreal.SplineCoordinateSpace.WORLD, False)
    point_type = unreal.SplinePointType.LINEAR if index in (0, 1, 11, 12) else unreal.SplinePointType.CURVE
    spline.set_spline_point_type(index, point_type, False)
spline.set_closed_loop(False, False)
spline.update_spline()
track_actor.call_method("Update Spline Mesh")
# Remove the Blueprint's placeholder segment at the origin; keep only generated road pieces.
for component in track_actor.get_components_by_class(unreal.SplineMeshComponent):
    start = component.get_start_position()
    end = component.get_end_position()
    if start.equals(unreal.Vector(0.0, 0.0, 0.0)) and end.equals(unreal.Vector(100.0, 0.0, 0.0)):
        component.set_visibility(False, True)

# Guaranteed visible road and collision, generated directly from the editable spline.
# Dense overlapping tiles eliminate gaps while preserving the spline's curves.
road_length = spline.get_spline_length()
tile_spacing = 350.0
tile_count = int(math.ceil(road_length / tile_spacing))
for index in range(tile_count):
    distance = min(index * tile_spacing, road_length - 1.0)
    location = spline.get_location_at_distance_along_spline(distance, unreal.SplineCoordinateSpace.WORLD)
    rotation = spline.get_rotation_at_distance_along_spline(distance, unreal.SplineCoordinateSpace.WORLD)
    tile = spawn_cube(
        f"RoadTile_{index + 1:03d}",
        (location.x, location.y, location.z - 35.0),
        (4.2, 16.0, 0.65),
        rotation.yaw,
        ["Road", "SplineGenerated"],
    )
    tile.static_mesh_component.set_collision_profile_name("BlockAll")

# Continuous safety barriers on both edges. They follow the spline normal so the
# player can learn the custom vehicle physics without falling off the course.
barrier_offset = 850.0
barrier_height = 130.0
for index in range(tile_count):
    distance = min(index * tile_spacing, road_length - 1.0)
    location = spline.get_location_at_distance_along_spline(distance, unreal.SplineCoordinateSpace.WORLD)
    rotation = spline.get_rotation_at_distance_along_spline(distance, unreal.SplineCoordinateSpace.WORLD)
    yaw_radians = math.radians(rotation.yaw)
    normal_x = -math.sin(yaw_radians)
    normal_y = math.cos(yaw_radians)
    for side_name, side_sign in (("Left", 1.0), ("Right", -1.0)):
        barrier = spawn_cube(
            f"Barrier_{side_name}_{index + 1:03d}",
            (
                location.x + normal_x * barrier_offset * side_sign,
                location.y + normal_y * barrier_offset * side_sign,
                location.z + barrier_height,
            ),
            (4.2, 0.35, 2.6),
            rotation.yaw,
            ["Barrier", side_name, "SplineGenerated"],
        )
        barrier.static_mesh_component.set_collision_profile_name("BlockAll")

# Reposition the existing spawn so the default racing GameMode starts on the course.
for actor in unreal.EditorLevelLibrary.get_all_level_actors():
    if isinstance(actor, unreal.PlayerStart):
        actor.set_actor_location(unreal.Vector(-2200.0, -6000.0, 140.0), False, False)
        actor.set_actor_rotation(unreal.Rotator(pitch=0.0, yaw=0.0, roll=0.0), False)
        actor.set_actor_label("PlayerStart_Race")

# Ordered gates distributed around the full lap.
gates = [
    ((1800.0, -6000.0, 150.0), 0.0),
    ((6900.0, -3500.0, 330.0), 70.0),
    ((4200.0, -1200.0, 180.0), 125.0),
    ((6900.0, 3300.0, 400.0), 110.0),
    ((1000.0, 6200.0, 150.0), 180.0),
    ((-7000.0, 3000.0, 370.0), -100.0),
    ((-2700.0, 3300.0, 250.0), -35.0),
    ((-2500.0, 0.0, 230.0), -150.0),
    ((-6000.0, -3100.0, 330.0), -70.0),
]
for index, (location, yaw) in enumerate(gates, start=1):
    checkpoint = spawn_blueprint(
        CHECKPOINT_BP,
        f"Checkpoint_{index:02d}",
        location,
        (0.0, yaw, 0.0),
        ["Checkpoint", f"Order_{index:02d}"],
    )
    checkpoint.set_actor_scale3d(unreal.Vector(2.0, 3.0, 3.0))

finish_class = getattr(unreal, "DDOneLapFinish", None)
if not finish_class:
    raise RuntimeError("DDOneLapFinish is unavailable. Compile the DungeonsAndDash module first.")
finish_checkpoint = unreal.EditorLevelLibrary.spawn_actor_from_class(
    finish_class,
    unreal.Vector(-3000.0, -6000.0, 180.0),
    unreal.Rotator(pitch=0.0, yaw=0.0, roll=0.0),
)
finish_checkpoint.set_actor_label("META_Finish_OneLap")
finish_checkpoint.tags = ["CodexGenerated", "Finish", "Meta", "OneLap"]

# Boost pads are staggered to reward line choice without blocking the whole road.
boosts = [
    ((0.0, -6000.0, 90.0), 0.0),
    ((4200.0, -5900.0, 100.0), 15.0),
    ((6500.0, -2300.0, 210.0), 105.0),
    ((5600.0, 5000.0, 170.0), 160.0),
    ((0.0, 6200.0, 90.0), 180.0),
    ((-6000.0, 5000.0, 180.0), -155.0),
    ((-6100.0, 400.0, 170.0), -120.0),
    ((-5000.0, -4200.0, 180.0), -55.0),
]
for index, (location, yaw) in enumerate(boosts, start=1):
    spawn_blueprint(
        BOOST_BP,
        f"BoostPad_{index:02d}",
        location,
        (0.0, yaw, 0.0),
        ["BoostPad"],
    )

# A clearly readable finish arch around the final trigger.
spawn_cube("META_Arch_Left", (-3000.0, -6850.0, 380.0), (0.8, 0.8, 7.5), 0.0)
spawn_cube("META_Arch_Right", (-3000.0, -5150.0, 380.0), (0.8, 0.8, 7.5), 0.0)
spawn_cube("META_Arch_Top", (-3000.0, -6000.0, 750.0), (0.8, 17.8, 0.8), 0.0)

text_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
    unreal.TextRenderActor,
    unreal.Vector(-3050.0, -6000.0, 760.0),
    unreal.Rotator(pitch=0.0, yaw=180.0, roll=0.0),
)
text_actor.set_actor_label("META_Text")
text_actor.text_render.set_editor_property("text", "¡GANASTE!")
text_actor.text_render.set_editor_property("horizontal_alignment", unreal.HorizTextAligment.EHTA_CENTER)
text_actor.text_render.set_editor_property("world_size", 220.0)
text_actor.tags = ["CodexGenerated", "Finish", "Meta"]

# Map-specific child classes preserve the shared vehicle while making this event exactly one lap.
asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
one_lap_vehicle_path = "/Game/DungeonsDash/LvL/Race/BP_DashVehicle_OneLap"
one_lap_gm_path = "/Game/DungeonsDash/LvL/Race/GM_RacingGame_OneLap"
one_lap_vehicle = unreal.load_asset(one_lap_vehicle_path)
created_one_lap_vehicle = one_lap_vehicle is None
if not one_lap_vehicle:
    vehicle_factory = unreal.BlueprintFactory()
    vehicle_factory.set_editor_property("parent_class", VEHICLE_BP.generated_class())
    one_lap_vehicle = asset_tools.create_asset(
        "BP_DashVehicle_OneLap", "/Game/DungeonsDash/LvL/Race", unreal.Blueprint, vehicle_factory
    )
one_lap_vehicle_cdo = unreal.get_default_object(one_lap_vehicle.generated_class())
one_lap_vehicle_cdo.set_editor_property("Laps", 2)
if created_one_lap_vehicle:
    unreal.EditorAssetLibrary.save_asset(one_lap_vehicle_path, only_if_is_dirty=False)

one_lap_gm = unreal.load_asset(one_lap_gm_path)
created_one_lap_gm = one_lap_gm is None
if not one_lap_gm:
    gm_factory = unreal.BlueprintFactory()
    gm_factory.set_editor_property("parent_class", RACING_GM_BP.generated_class())
    one_lap_gm = asset_tools.create_asset(
        "GM_RacingGame_OneLap", "/Game/DungeonsDash/LvL/Race", unreal.Blueprint, gm_factory
    )
one_lap_gm_cdo = unreal.get_default_object(one_lap_gm.generated_class())
one_lap_gm_cdo.set_editor_property("default_pawn_class", one_lap_vehicle.generated_class())
if created_one_lap_gm:
    unreal.EditorAssetLibrary.save_asset(one_lap_gm_path, only_if_is_dirty=False)

world = unreal.EditorLevelLibrary.get_editor_world()
world.get_world_settings().set_editor_property("default_game_mode", one_lap_gm.generated_class())

if not unreal.EditorLevelLibrary.save_current_level():
    raise RuntimeError("Failed to save generated race level")
unreal.EditorAssetLibrary.save_asset(TARGET_MAP, only_if_is_dirty=False)
unreal.log_warning(
    "CODEX_GENERATED_LEVEL /Game/DungeonsDash/LvL/LVL_DungeonDash_Circuit "
    f"checkpoints=10 boosts=8 finish=1 spline_points=25 road_tiles={tile_count} "
    f"barriers={tile_count * 2} laps=1"
)
